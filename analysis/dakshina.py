"""Cross-script agreement on the Dakshina Bengali sentences (native-speaker romanization), for every system.   python analysis/dakshina.py [--limit N]

There are no task labels, so accuracy is not measured. Every system answers one 7-way topic question about each sentence in four spellings:
native Bengali (reference), the native-speaker romanization (Dakshina), rule-based romanization, natural-style romanization.
Metrics, all relative to the system's OWN answer on the Bengali-script sentence:
  agreement   share of sentences whose top option is unchanged
  tv          mean total-variation distance between the two probability vectors (0 = identical, 1 = disjoint)
  chance      agreement expected if the romanized answers were unrelated to the Bengali ones (sum_c p_native(c) * p_variant(c))
Comparisons between spellings are paired bootstrap differences over sentences (1,000 draws, seed 0), on the sentences every spelling answered.
Writes analysis/tables/dak_agreement.csv and dak_paired.csv."""
import json, os, sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "harness")); sys.path.insert(0, str(ROOT / "analysis"))
os.environ.setdefault("BN_ROT", "0"); os.environ.setdefault("BN_QLANG", "en")
from jev_benchmarking import bn_text  # noqa: E402
from jev_benchmarking.cache import ResponseCache, request_key  # noqa: E402
from jev_benchmarking.tasks import get_tasks  # noqa: E402
from collect import MODELS, load_jsonl  # noqa: E402

LIMIT = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else 1500
VARIANTS = ["native", "dakshina", "roman", "roman_nat"]
SUFFIX = "_dak"
task = get_tasks(["bn_dakshina"])[0]
ids = [json.loads(l)["id"] for l in open(ROOT / "data" / "raw" / "dakshina_bn.jsonl", encoding="utf-8")]   # row index -> stable sentence id
jev = ResponseCache()
recs = []
for label, (tag, src) in MODELS.items():
    store = None
    if src != "jev":
        d = ROOT / "runs" / (src + SUFFIX)
        if not d.exists():
            continue
        store = load_jsonl(d)
    for v in VARIANTS:
        bn_text.VARIANT = v
        for e in task.examples("eval", limit=LIMIT):
            key = request_key(tag, e.state, e.questions)
            if store is None:
                resp = jev.get(key)
            else:
                hit = store.get(key); resp = hit[0] if hit else None
            if resp is None:
                continue
            a = resp["answers"]["answer"]
            recs.append(dict(model=label, variant=v, uid=e.uid, id=ids[int(e.uid.split("/")[-1])], choice=a["choice"], probs=json.dumps(a["probabilities"])))
df = pd.DataFrame(recs)
if df.empty:
    sys.exit("no responses found")
df.to_csv(ROOT / "analysis" / "dak_items.csv", index=False)   # every response used below (gitignored; the release script derives results/predictions_dakshina.csv.gz from it)
rng = np.random.default_rng(0)
agree_rows, paired_rows = [], []
for m, g in df.groupby("model"):
    wide = g.pivot(index="uid", columns="variant", values="choice")
    pw = g.pivot(index="uid", columns="variant", values="probs")
    if not set(VARIANTS) <= set(wide.columns):
        print(f"{m}: missing variants {set(VARIANTS) - set(wide.columns)}; skipped"); continue
    ok = wide.dropna(subset=VARIANTS).index
    wide, pw = wide.loc[ok], pw.loc[ok]
    P = {v: pd.DataFrame([json.loads(x) for x in pw[v]], index=ok) for v in VARIANTS}
    opts = P["native"].columns
    agree, tv = {}, {}
    for v in VARIANTS[1:]:
        agree[v] = (wide[v] == wide["native"]).to_numpy(float)
        tv[v] = 0.5 * (P[v][opts] - P["native"][opts]).abs().sum(axis=1).to_numpy()
        chance = float((P["native"][opts].mean() * P[v][opts].mean()).sum())
        b = [agree[v][rng.integers(0, len(ok), len(ok))].mean() for _ in range(1000)]
        agree_rows.append(dict(model=m, variant=v, n=len(ok), agreement=agree[v].mean(), ci_lo=np.percentile(b, 2.5), ci_hi=np.percentile(b, 97.5), tv=tv[v].mean(), chance=chance,
                               conf_native=P["native"][opts].max(axis=1).mean(), conf_variant=P[v][opts].max(axis=1).mean()))
    for a_, b_ in (("dakshina", "roman"), ("dakshina", "roman_nat"), ("roman_nat", "roman")):
        for name, arr in (("agreement", agree), ("tv", tv)):
            x = arr[a_] - arr[b_]; bs = [x[rng.integers(0, len(x), len(x))].mean() for _ in range(1000)]
            paired_rows.append(dict(model=m, metric=name, comparison=f"{a_} - {b_}", n=len(x), diff=x.mean(), lo=np.percentile(bs, 2.5), hi=np.percentile(bs, 97.5)))
out = ROOT / "analysis" / "tables"
A, Pd = pd.DataFrame(agree_rows), pd.DataFrame(paired_rows)
A.to_csv(out / "dak_agreement.csv", index=False); Pd.to_csv(out / "dak_paired.csv", index=False)
print(A.pivot_table(index="model", columns="variant", values="agreement").round(3).to_string())
print(Pd[Pd.metric == "agreement"].pivot_table(index="model", columns="comparison", values="diff").round(3).to_string())
