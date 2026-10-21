"""Collect per-item predictions for every model/setting into analysis/items.csv.

Run one setting per process (BN_VARIANT / BN_ROT are read at import):
    BN_VARIANT=native BN_ROT=0 python analysis/collect.py
or all settings: python analysis/collect.py --all
Models: Jev from harness/cache/responses.db; open models from runs/<dir>/**/*.jsonl (Kaggle outputs).
"""
import csv, hashlib, json, os, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "harness"))
OUT = ROOT / "analysis" / "items.csv"
FIELDS = ["model", "task", "split", "variant", "rot", "uid", "cluster", "gold_id", "pred_id", "probs", "subset", "gold", "pred", "pmax", "vendor_conf", "correct", "K", "brier",
          "pos_pred", "pos_gold", "latency_s", "input_tokens"]
SETTINGS = [("native", 0), ("roman", 0), ("roman_nat", 0), ("native", 1), ("native", 2), ("roman", 1), ("roman", 2)]
TASKS = ["bn_sentnob", "bn_bnli", "bn_massive", "bn_belebele", "bn_sib200"]
DEV_LIMIT = 1500
LIMIT_LARGE = {"bn_bnli": 1500, "bn_massive": 1500}  # open models ran a hash-ordered subset; Jev ran all (restricted to the same items)
# label -> (cache tag, source). source "jev" = SQLite cache; otherwise a runs/ subdirectory of JSONL files.
MODELS = {
    "jev-1.13.0": ("jev-1.13.0", "jev"),
    "laya-multilingual": ("hf:convaiinnovations/laya-multilingual", "laya_ml"),
    "julia-1": ("hf:SupersonicLabs/Julia-1", "julia1"),
    "gemma-4-E4B-it": ("hf:google/gemma-4-E4B-it", "gemma4_e4b"),
    "d3-flash (4/8-bit)": ("hf:vllm-sr/d3-flash@521525effa", "d3_flash"),
    "laya-bangla v2": ("hf:algolyzer/laya-bangla@4c5eb48932", "laya_bangla"),
    "d3-edge": ("hf:vllm-sr/d3-edge@18d61df786", "d3_edge"),
    "d3-lite": ("hf:vllm-sr/d3-lite@a8d25a91ef", "d3_lite"),
    "d3-nano": ("hf:vllm-sr/d3-nano@3aeb1c22a5", "d3_nano"),
    "d3-mini": ("hf:vllm-sr/d3-mini@a475367de0", "d3_mini"),
}


def load_jsonl(d: Path) -> dict:
    out = {}
    for f in d.rglob("*.jsonl"):
        for line in f.read_text().splitlines():
            try:
                r = json.loads(line)
                out[r["key"]] = (r["response"], r.get("latency_s", 0.0))
            except (json.JSONDecodeError, KeyError):
                pass
    return out


def collect_setting(variant: str, rot: int, split: str = "eval") -> list[dict]:
    from jev_benchmarking.cache import ResponseCache, request_key
    from jev_benchmarking.tasks import get_tasks

    rows = []
    jev = ResponseCache()
    jev_rows = {}
    sources = {}
    for label, (tag, src) in MODELS.items():
        if src != "jev" and (ROOT / "runs" / src).exists():
            sources[label] = load_jsonl(ROOT / "runs" / src)
    for task in get_tasks(TASKS):
        if variant in ("roman", "roman_nat") and task.name == "bn_belebele":
            continue  # human romanization (ben_Latn) is inside bn_belebele under native
        if task.splits.get(split) is None:
            continue  # e.g. Belebele has no dev split
        exs = task.examples(split, limit=DEV_LIMIT if split == "dev" else None)
        for label, (tag, src) in MODELS.items():
            if src != "jev" and label not in sources:
                continue
            if variant == "roman_nat" and src != "jev":
                continue  # only Jev was run on roman_nat; other models would match only where both romanizations coincide (cache artifact)
            limit = LIMIT_LARGE.get(task.name) if split == "eval" else None
            use = exs
            keep = {e.uid for e in task.examples("eval", limit=limit)} if limit else None
            for e in (exs if src == "jev" else use):
                if keep is not None and e.uid not in keep:
                    continue  # compare all models on the same subset
                key = request_key(tag, e.state, e.questions)
                if src == "jev":
                    resp = jev.get(key); lat = 0.0
                    if resp is None:
                        continue
                    lat = jev.db.execute("SELECT latency_s FROM responses WHERE key=?", (key,)).fetchone()[0]
                else:
                    hit = sources[label].get(key)
                    if hit is None:
                        continue
                    resp, lat = hit
                a = resp["answers"]["answer"]
                probs = a["probabilities"]
                crit = e.questions["answer"]["criteria"]
                order = list(crit.keys())
                ident = (lambda k: crit[k]) if task.name == "bn_belebele" else (lambda k: k)  # Belebele letters rotate; identify options by text
                probs_id = {ident(k): v for k, v in probs.items() if k in crit}
                cluster = e.state.get("passage") if task.name == "bn_belebele" else (e.state.get("premise") if task.name == "bn_bnli" else e.uid)
                pred = a["choice"]
                gold = e.gold["answer"]
                rows.append(dict(model=label, task=task.name, split=split, variant=variant, cluster=hashlib.md5(str(cluster).encode()).hexdigest()[:10],
                                 gold_id=ident(gold), pred_id=ident(pred), probs=json.dumps(probs_id, ensure_ascii=False), rot=rot, uid=e.uid, subset=e.subset, gold=gold, pred=pred,
                                 pmax=max(probs.values()), vendor_conf=a.get("confidence", ""), correct=int(pred == gold), K=len(order),
                                 brier=sum((probs.get(k, 0.0) - (k == gold)) ** 2 for k in set(probs) | {gold}),
                                 pos_pred=order.index(pred) if pred in order else -1, pos_gold=order.index(gold),
                                 latency_s=lat, input_tokens=(resp.get("usage") or {}).get("input_tokens", 0)))
    return rows


def main():
    if "--all" in sys.argv:
        jobs = [(v, r, "eval") for v, r in SETTINGS] + [("native", 0, "dev"), ("roman", 0, "dev")]
        for i, (v, r, sp) in enumerate(jobs):
            args = [sys.executable, __file__] + (["--append"] if i else [])
            subprocess.run(args, env=dict(os.environ, BN_VARIANT=v, BN_ROT=str(r), BN_SPLIT=sp), check=True)
        return
    split = os.environ.get("BN_SPLIT", "eval")
    rows = collect_setting(os.environ.get("BN_VARIANT", "native"), int(os.environ.get("BN_ROT", "0")), split)
    new = not OUT.exists() or "--append" not in sys.argv
    with OUT.open("w" if new else "a", newline="") as f:
        w = csv.DictWriter(f, FIELDS)
        if new:
            w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} rows ({split} {os.environ.get('BN_VARIANT','native')} rot{os.environ.get('BN_ROT','0')})")


if __name__ == "__main__":
    main()
