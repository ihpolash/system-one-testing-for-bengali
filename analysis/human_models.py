"""Every model on the items the author romanized by hand, under seven conditions (see human_roman_eval.py).

Reads Kaggle outputs runs/<model>_human/ (round 1: native, roman, roman_nat) and runs/<model>_human2/ (round 2: human, native_edit, roman_edit, roman_nat_edit),
and the Jev cache. Requests are content-keyed, so a corrected-text condition that equals the original on an unedited sentence reuses the stored response.
Primary comparisons use the author's CORRECTED Bengali as the reference (native_edit), because the Banglish was written from it.
The earlier tool-assisted version of file 3 is archived in analysis/archive/ and is not used here.
    python analysis/human_models.py"""
import json, os, sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "harness"))
os.environ["BN_ROWS_JSON"] = str(ROOT / "data" / "human_rows.json")
os.environ["BN_HUMAN_CSV"] = str(ROOT / "data" / "banglish_human.csv")
os.environ.setdefault("BN_QLANG", "en"); os.environ.setdefault("BN_ROT", "0")
from jev_benchmarking import bn_text  # noqa: E402
from jev_benchmarking.cache import ResponseCache, request_key  # noqa: E402
from jev_benchmarking.config import MODEL as JEV  # noqa: E402
from jev_benchmarking.tasks import get_tasks  # noqa: E402

MODELS = {  # label -> (cache tag, run-folder stems)
    "jev-1.13.0": (JEV, None),
    "d3-flash (4-bit)": ("hf:vllm-sr/d3-flash@521525effa", ["d3_flash_human", "d3_flash_human2"]),
    "d3-mini": ("hf:vllm-sr/d3-mini@a475367de0", ["d3_mini_human", "d3_mini_human2"]),
    "gemma-4-E4B-it": ("hf:google/gemma-4-E4B-it", ["gemma4_e4b_human", "gemma4_e4b_human2"]),
    "d3-nano": ("hf:vllm-sr/d3-nano@3aeb1c22a5", ["d3_nano_human", "d3_nano_human2"]),
    "d3-lite": ("hf:vllm-sr/d3-lite@a8d25a91ef", ["d3_lite_human", "d3_lite_human2"]),
    "d3-edge": ("hf:vllm-sr/d3-edge@18d61df786", ["d3_edge_human", "d3_edge_human2"]),
    "laya-multilingual": ("hf:convaiinnovations/laya-multilingual", ["laya_ml_human", "laya_ml_human2"]),
    "laya-bangla v2": ("hf:algolyzer/laya-bangla@4c5eb48932", ["laya_bangla_human"]),
    "julia-1": ("hf:SupersonicLabs/Julia-1", ["julia1_human", "julia1_human2"]),
    "kev-4b": ("hf:jaredpalmer/kev-4b@v1.0", ["kev_4b_human"]),
    "kev-0.8b": ("hf:jaredpalmer/kev-0.8b@v1.0", ["kev_08b_human"]),
}
TASK = {"sentnob": "bn_sentnob", "massive": "bn_massive", "bnli": "bn_bnli"}
VARIANTS = ["native", "native_edit", "roman", "roman_edit", "roman_nat", "roman_nat_edit", "human"]
PRIMARY = [("human", "native_edit"), ("roman_edit", "native_edit"), ("roman_nat_edit", "native_edit"), ("human", "roman_edit"), ("human", "roman_nat_edit"), ("native_edit", "native")]

# raw row -> (unit id, source file), from the sources maps (premise row stands for an NLI pair)
src = {}
for p in ("banglish_gold_sources.json", "banglish_gold2_sources.json", "banglish_gold3_sources.json"):
    f = ROOT / "analysis" / p
    if f.exists():
        for k, v in json.load(open(f)).items():
            if v["dataset"] in TASK and v.get("part", "bnli_premise") != "bnli_hypothesis":
                src[(v["dataset"], v["raw_row"])] = (int(k), "files 1-2" if int(k) <= 220 else "file 3")


def load(stems):
    out = {}
    for stem in stems or []:
        d = ROOT / "runs" / stem
        if not d.exists():
            continue
        for f in d.rglob("*.jsonl"):
            if f.name == "failures.jsonl":
                continue
            for line in f.read_text().splitlines():
                try:
                    r = json.loads(line); out[r["key"]] = r["response"]
                except (json.JSONDecodeError, KeyError):
                    pass
    return out


jev_cache = ResponseCache()
recs = []
for label, (tag, stems) in MODELS.items():
    store = load(stems)
    if stems and not store:
        continue
    for variant in VARIANTS:
        bn_text.VARIANT = variant
        for ds, tname in TASK.items():
            for e in get_tasks([tname])[0].examples("eval"):
                ri = int(e.uid.split("/")[-1])
                if (ds, ri) not in src:
                    continue
                key = request_key(tag, e.state, e.questions)
                resp = jev_cache.get(key) if stems is None else store.get(key)
                uid, fl = src[(ds, ri)]
                if resp is None:
                    recs.append(dict(model=label, variant=variant, dataset=ds, id=uid, file=fl, answered=0, ok=np.nan, pmax=np.nan)); continue
                a = resp["answers"]["answer"]
                recs.append(dict(model=label, variant=variant, dataset=ds, id=uid, file=fl, answered=1, ok=float(a["choice"] == e.gold["answer"]), pmax=max(a["probabilities"].values())))
df = pd.DataFrame(recs)
df.to_csv(ROOT / "analysis" / "tables" / "human_items_all_models.csv", index=False)

# ---- coverage of each condition (a condition missing for a model means that job has not finished or the model cannot answer)
cov = df.groupby(["model", "variant"]).answered.mean().unstack()[VARIANTS].round(2)
print("COVERAGE (share of items with a stored response)"); print(cov.to_string())

g = df.groupby(["dataset", "model", "variant"]).agg(acc=("ok", "mean")).reset_index()
acc = g.pivot_table(index=["dataset", "model"], columns="variant", values="acc")[VARIANTS].round(3)
print("\nACCURACY on answered items"); print(acc.to_string())

# A comparison is reported only if both conditions are essentially complete for that model (>= 90% of the coverage the model has on the original text);
# otherwise a job is unfinished and the few stored responses are coincidental matches, which would be a biased subset of easy items.
complete = {(m, v): cov.loc[m, v] >= 0.9 * cov.loc[m, "native"] for m in cov.index for v in VARIANTS}
pending = sorted({(m, v) for (m, v), ok in complete.items() if not ok and cov.loc[m, "native"] > 0})
if pending:
    print("\nINCOMPLETE conditions (excluded from comparisons): " + ", ".join(f"{m}:{v}" for m, v in pending))
rng = np.random.default_rng(0)
rows = []
for m in MODELS:
    s = df[df.model == m]
    if s.empty or s.answered.sum() == 0:
        continue
    for scope in ("all tasks", "sentnob", "massive", "bnli"):
        t = s if scope == "all tasks" else s[s.dataset == scope]
        p = t.pivot_table(index=["dataset", "id"], columns="variant", values="ok")
        for a, b in PRIMARY:
            if a not in p or b not in p or not complete.get((m, a), False) or not complete.get((m, b), False):
                continue
            q = p[[a, b]].dropna()
            if len(q) < 25:
                continue
            x = (q[a] - q[b]).to_numpy(float); bs = [rng.choice(x, len(x)).mean() for _ in range(1000)]
            rows.append(dict(model=m, scope=scope, comparison=f"{a} - {b}", n=len(x), diff=x.mean(), lo=np.percentile(bs, 2.5), hi=np.percentile(bs, 97.5)))
res = pd.DataFrame(rows); res.to_csv(ROOT / "analysis" / "tables" / "human_items_paired.csv", index=False)
show = res[res.scope == "all tasks"].pivot_table(index="model", columns="comparison", values="diff").round(3)
print("\nPAIRED DIFFERENCES, all tasks pooled (accuracy points; bootstrap CIs in tables/human_items_paired.csv)")
print(show[[f"{a} - {b}" for a, b in PRIMARY if f"{a} - {b}" in show]].reindex([m for m in MODELS if m in show.index]).to_string())
