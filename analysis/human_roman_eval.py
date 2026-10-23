"""End-to-end Jev check on the AI-generated Banglish (ChatGPT output, corrected with Grok and Claude, reviewed by the author; internal variant name "human"). Supplied as three CSV files.

Inputs: analysis/banglish_gold{,2,3}_completed.csv. The author corrected spellings in the Bengali column before writing the Banglish, so items are matched to
the dataset by their ORIGINAL text (read from data/raw via the sources JSON), never by the edited column. Whole inputs only: SentNoB and MASSIVE rows, and
XNLI-bn pairs with both sentences filled (single sentences cut from longer SIB-200 / Belebele / BNLI inputs in file 1 are ignored).

Conditions on the SAME items:
  native            original dataset text
  native_edit       the author's corrected Bengali (isolates the effect of spelling correction alone)
  roman / roman_nat rule-based / natural-style romanization of the original text
  roman_edit / roman_nat_edit   the same romanizers applied to the corrected text (the fair comparators for the Banglish)
  human             the AI-generated Banglish (made from the corrected text)
The user's files are never edited. Sends only uncached Jev requests (about $0.0001 per request).
    python analysis/human_roman_eval.py"""
import asyncio, csv, json, os, re, shutil, sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "harness"))
A = ROOT / "analysis"
GOLD = [A / "banglish_gold_completed.csv", A / "banglish_gold2_completed.csv", A / "banglish_gold3_completed.csv"]
SRCS = [A / "banglish_gold_sources.json", A / "banglish_gold2_sources.json", A / "banglish_gold3_sources.json"]
VARIANTS = ["native", "native_edit", "roman", "roman_edit", "roman_nat", "roman_nat_edit", "human"]
norm = lambda s: " ".join(s.split())
TASK = {"sentnob": "bn_sentnob", "massive": "bn_massive", "bnli": "bn_bnli"}

src = {k: v for p in SRCS if p.exists() for k, v in json.load(open(p)).items()}
raw = {d: [json.loads(l) for l in open(ROOT / "data" / "raw" / f"{d}.jsonl")] for d in TASK}
RAWTEXT = {"sentnob": lambda r: r["Data"], "massive": lambda r: r["text"]}

rows = []
for g in GOLD:
    if not g.exists():
        continue
    for r in csv.DictReader(open(g, encoding="utf-8-sig")):
        if not (r.get("banglish") or "").strip():
            continue
        if re.search(r"[ঀ-৿]", r["banglish"]):
            print(f"WARNING: row {r['id']} has Bengali script in the Banglish column; skipped"); continue
        r["file"] = GOLD.index(g) + 1
        rows.append(r)
by_id = {int(r["id"]): r for r in rows}

# ---- scorable units and the merged mapping (original text -> corrected text, Banglish)
units, entries = [], []
for i, r in by_id.items():
    d = r["dataset"]
    if d in ("sentnob", "massive"):
        ri = src[str(i)]["raw_row"]
        entries.append(dict(id=i, dataset=d, raw_bengali=RAWTEXT[d](raw[d][ri]), bengali=r["bengali"], banglish=r["banglish"], file=r["file"]))
        units.append((i, d, ri, r["file"]))
pairs = {}
for i, r in by_id.items():
    if r["dataset"] in ("bnli_premise", "bnli_hypothesis"):
        pairs.setdefault(r["pair"], {})[r["dataset"]] = i
for pid, p in pairs.items():
    if len(p) == 2:
        ri = src[str(p["bnli_premise"])]["raw_row"]
        row = raw["bnli"][ri]
        for part, key in (("bnli_premise", "sentence1"), ("bnli_hypothesis", "sentence2")):
            r = by_id[p[part]]
            entries.append(dict(id=p[part], dataset="bnli", raw_bengali=row[key], bengali=r["bengali"], banglish=r["banglish"], file=r["file"]))
        units.append((p["bnli_premise"], "bnli", ri, by_id[p["bnli_premise"]]["file"]))
edited = sum(1 for e in entries if norm(e["raw_bengali"]) != norm(e["bengali"]))
print(f"scorable units: {len(units)} -> " + ", ".join(f"{d}={sum(1 for u in units if u[1]==d)}" for d in TASK) + f" | sentences with corrected Bengali: {edited}/{len(entries)}")

merged = A / "_banglish_merged.csv"
with open(merged, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, ["id", "dataset", "raw_bengali", "bengali", "banglish", "file"]); w.writeheader(); w.writerows(entries)
(ROOT / "data").mkdir(exist_ok=True)
json.dump({TASK[d]: sorted({ri for _, dd, ri, _ in units if dd == d}) for d in TASK}, open(ROOT / "data" / "human_rows.json", "w"))
shutil.copy(merged, ROOT / "data" / "banglish_human.csv")
# rows whose Bengali the author corrected: the *_edit conditions differ from the originals only there (identical requests share one stored response)
_ed = {}
for _i, _d, _ri, _ in units:
    _ids = [_i] if _d != "bnli" else [e_id for e_id in (by_id[_i]["id"],)]
    _changed = [e for e in entries if e["id"] in ([_i] if _d != "bnli" else [_i, _i + 1]) and norm(e["raw_bengali"]) != norm(e["bengali"])]
    if _changed:
        _ed.setdefault(TASK[_d], []).append(_ri)
json.dump({k: sorted(set(v)) for k, v in _ed.items()}, open(ROOT / "data" / "human_rows_edited.json", "w"))
print("edited units per task:", {k: len(set(v)) for k, v in _ed.items()})
os.environ["BN_HUMAN_CSV"] = str(merged)
for line in (ROOT / ".env").read_text().splitlines():
    if "=" in line and not line.startswith("#"):
        k, v = line.split("=", 1); os.environ.setdefault(k.strip(), v.strip().strip('"'))
os.environ.setdefault("JEV_TOTAL_BUDGET_USD", "14")

from jev_benchmarking import bn_text  # noqa: E402
from jev_benchmarking.cache import ResponseCache, request_key  # noqa: E402
from jev_benchmarking.config import MODEL  # noqa: E402
from jev_benchmarking.runner import run_examples  # noqa: E402
from jev_benchmarking.tasks import get_tasks  # noqa: E402

cache = ResponseCache()
out = []
for variant in VARIANTS:
    bn_text.VARIANT = variant
    for d in TASK:
        sel = [u for u in units if u[1] == d]
        if not sel:
            continue
        task = get_tasks([TASK[d]])[0]
        exs = [task.build(raw[d][ri], "bn") for _, _, ri, _ in sel]
        asyncio.run(run_examples(TASK[d], exs, cache, max_cost_usd=0.5, rpm=600, concurrency=8))
        for (uid, _, _, fl), ex in zip(sel, exs):
            resp = cache.get(request_key(MODEL, ex.state, ex.questions))
            if resp is None:
                print(f"missing response: unit {uid} {d} {variant}"); continue
            a = resp["answers"]["answer"]; p = a["probabilities"]
            out.append(dict(id=uid, dataset=d, file=fl, variant=variant, gold=ex.gold["answer"], pred=a["choice"], ok=int(a["choice"] == ex.gold["answer"]), pmax=max(p.values())))
df = pd.DataFrame(out)
df.to_csv(A / "tables" / "human_roman_jev.csv", index=False)

print(df.groupby(["dataset", "variant"]).agg(n=("ok", "size"), acc=("ok", "mean")).round(3).unstack("variant")["acc"][VARIANTS].to_string())
piv_all = df.pivot_table(index=["dataset", "id"], columns="variant", values="ok").dropna()
print(f"\npaired, all {len(piv_all)} items (accuracy): " + ", ".join(f"{v}={piv_all[v].mean():.3f}" for v in VARIANTS))

rng = np.random.default_rng(0)
COMPARE = [("native_edit", "native"), ("human", "native"), ("human", "native_edit"), ("roman", "native"), ("roman_edit", "native_edit"),
           ("roman_nat_edit", "native_edit"), ("human", "roman_edit"), ("human", "roman_nat_edit")]
print("\npaired differences in accuracy, 95% bootstrap CI over items")
for d in list(TASK) + ["ALL"]:
    sub = piv_all if d == "ALL" else (piv_all.xs(d, level="dataset") if d in piv_all.index.get_level_values("dataset") else None)
    if sub is None or len(sub) < 20:
        continue
    for a, b in COMPARE:
        x = (sub[a] - sub[b]).to_numpy(float)
        bs = [rng.choice(x, len(x)).mean() for _ in range(2000)]
        print(f"{d:8} n={len(x):4}  {a:14} - {b:12}: {x.mean():+.3f}  [{np.percentile(bs,2.5):+.3f}, {np.percentile(bs,97.5):+.3f}]")
