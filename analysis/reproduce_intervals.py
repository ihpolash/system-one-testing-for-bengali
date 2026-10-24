"""Recompute the reported intervals from the RELEASED predictions only (results/*.csv.gz), without analysis/items.csv or any Jev response.
It re-implements the cluster bootstrap independently of metrics.py/dakshina.py, with its own random stream and 3,000 draws, and compares with the committed tables:
  * test-set accuracy / macro-F1 with 95% cluster-bootstrap intervals          vs analysis/tables/rq1_accuracy.csv
  * paired differences to Jev (cluster bootstrap)                             vs the paired table, when present
  * Dakshina agreement and the native-speaker minus rule-based difference     vs analysis/tables/dak_agreement.csv, dak_paired.csv
Point estimates must match exactly; interval endpoints must agree within the Monte-Carlo noise of two independent bootstraps (tolerances below).
Not reproducible from released data: calibration (needs Jev's full probability vectors for Jev) and the temperature-scaled results of Jev.   python analysis/reproduce_intervals.py"""
import sys
from pathlib import Path

import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore", category=pd.errors.PerformanceWarning)

A = Path(__file__).parent
R = A.parent / "results"
B = 3000
rng = np.random.default_rng(123)
TOL_ACC, TOL_F1 = 0.012, 0.02
bad, worst = [], {"point": 0.0, "acc_ci": 0.0, "f1_ci": 0.0, "dak_ci": 0.0}
NAME = {"bn_sentnob": "SentNoB", "bn_bnli": "XNLI-bn", "bn_massive": "MASSIVE", "bn_belebele": "Belebele", "bn_sib200": "SIB-200"}

def boot_metric(gold, pred, cluster, macro_f1):
    cl, idx = np.unique(cluster, return_inverse=True); k = len(cl)
    if not macro_f1:
        corr = np.bincount(idx, weights=(gold == pred).astype(float), minlength=k); n = np.bincount(idx, minlength=k).astype(float)
        est = corr.sum() / n.sum(); d = rng.integers(0, k, (B, k)); v = corr[d].sum(1) / n[d].sum(1)
        return est, *np.percentile(v, [2.5, 97.5])
    classes = np.unique(gold)
    tp = np.stack([np.bincount(idx, weights=((gold == c) & (pred == c)).astype(float), minlength=k) for c in classes])
    fp = np.stack([np.bincount(idx, weights=((gold != c) & (pred == c)).astype(float), minlength=k) for c in classes])
    fn = np.stack([np.bincount(idx, weights=((gold == c) & (pred != c)).astype(float), minlength=k) for c in classes])
    def f1(T, F, N):
        den = 2 * T + F + N; return np.where(den > 0, 2 * T / np.where(den > 0, den, 1), 0).mean(0)
    est = f1(tp.sum(1, keepdims=True), fp.sum(1, keepdims=True), fn.sum(1, keepdims=True))[0]
    d = rng.integers(0, k, (B, k)); v = f1(tp[:, d].sum(2), fp[:, d].sum(2), fn[:, d].sum(2))
    return est, *np.percentile(v, [2.5, 97.5])

# ---- test sets
t = pd.read_csv(R / "predictions_test_sets.csv.gz", usecols=["model", "task", "split", "variant", "rot", "uid", "subset", "cluster", "gold_id", "pred_id"])
t = t[(t.split == "eval") & (t.rot == 0)].copy()
t["vlabel"] = np.where((t.task == "bn_belebele") & (t.subset == "ben_Latn"), "human_roman", t.variant)
rq1 = pd.read_csv(A / "tables" / "rq1_accuracy.csv").set_index(["task", "variant", "model"])
n_checked = 0
for (task, v, m), d in t.groupby(["task", "vlabel", "model"]):
    key = (NAME[task], v, m)
    if key not in rq1.index:
        continue
    ref = rq1.loc[key]; f1 = task == "bn_sentnob"
    est, lo, hi = boot_metric(d.gold_id.to_numpy(), d.pred_id.to_numpy(), d.cluster.to_numpy(), f1)
    worst["point"] = max(worst["point"], abs(est - ref.value))
    e = max(abs(lo - ref.ci_lo), abs(hi - ref.ci_hi)); worst["f1_ci" if f1 else "acc_ci"] = max(worst["f1_ci" if f1 else "acc_ci"], e)
    if abs(est - ref.value) > 1e-9: bad.append(f"point estimate differs: {key}: {est:.6f} vs {ref.value:.6f}")
    if e > (TOL_F1 if f1 else TOL_ACC): bad.append(f"interval differs by {e:.4f}: {key}")
    n_checked += 1
# ---- paired differences to Jev (cluster bootstrap over the clusters of the other system's items)
pj = pd.read_csv(A / "tables" / "rq1_paired_vs_jev.csv").set_index(["task", "variant", "model"])
npair = 0
jev = t[t.model == "jev-1.13.0"].set_index(["task", "vlabel", "uid"])
for (task, v, m), d in t.groupby(["task", "vlabel", "model"]):
    key = (NAME[task], v, m)
    if m == "jev-1.13.0" or key not in pj.index:
        continue
    j = jev.loc[(task, v)] if (task, v) in jev.index.droplevel(2) else None
    if j is None:
        continue
    mg = d.set_index("uid").join(j[["gold_id", "pred_id"]], rsuffix="_j", how="inner")
    if len(mg) < 30:
        continue
    diff = ((mg.gold_id == mg.pred_id).astype(float) - (mg.gold_id_j == mg.pred_id_j).astype(float)).to_numpy()
    cl, idx = np.unique(mg.cluster.to_numpy(), return_inverse=True); k = len(cl)
    sm = np.bincount(idx, weights=diff, minlength=k); n = np.bincount(idx, minlength=k).astype(float)
    dd = rng.integers(0, k, (B, k)); lo, hi = np.percentile(sm[dd].sum(1) / n[dd].sum(1), [2.5, 97.5]); ref = pj.loc[key]
    if abs(diff.mean() - ref.acc_diff) > 1e-9 and task != "bn_sentnob":   # SentNoB's pair is accuracy here, as in the table
        bad.append(f"paired point estimate differs: {key}")
    if max(abs(lo - ref.ci_lo), abs(hi - ref.ci_hi)) > TOL_ACC:
        bad.append(f"paired interval differs by {max(abs(lo - ref.ci_lo), abs(hi - ref.ci_hi)):.4f}: {key}")
    npair += 1
# ---- Dakshina
dk = pd.read_csv(R / "predictions_dakshina.csv.gz", usecols=["model", "variant", "id", "choice"])
da = pd.read_csv(A / "tables" / "dak_agreement.csv").set_index(["model", "variant"]); dp = pd.read_csv(A / "tables" / "dak_paired.csv")
dp = dp[(dp.metric == "agreement") & (dp.comparison == "dakshina - roman")].set_index("model")
nd = 0
for m, g in dk.groupby("model"):
    w = g.pivot(index="id", columns="variant", values="choice").dropna()
    a = {v: (w[v] == w["native"]).to_numpy(float) for v in ("dakshina", "roman", "roman_nat")}
    for v in a:
        b = [a[v][rng.integers(0, len(w), len(w))].mean() for _ in range(B)]; lo, hi = np.percentile(b, [2.5, 97.5]); ref = da.loc[(m, v)]
        worst["point"] = max(worst["point"], abs(a[v].mean() - ref.agreement)); e = max(abs(lo - ref.ci_lo), abs(hi - ref.ci_hi)); worst["dak_ci"] = max(worst["dak_ci"], e)
        if abs(a[v].mean() - ref.agreement) > 1e-9: bad.append(f"Dakshina agreement differs: {m} {v}")
        if e > TOL_ACC: bad.append(f"Dakshina interval differs by {e:.4f}: {m} {v}")
    x = a["dakshina"] - a["roman"]; b = [x[rng.integers(0, len(x), len(x))].mean() for _ in range(B)]; lo, hi = np.percentile(b, [2.5, 97.5]); ref = dp.loc[m]
    if abs(x.mean() - ref["diff"]) > 1e-9 or max(abs(lo - ref.lo), abs(hi - ref.hi)) > TOL_ACC: bad.append(f"paired Dakshina difference differs: {m}")
    nd += 1
print(f"checked {n_checked} test-set intervals, {npair} paired differences to Jev and {nd} Dakshina systems; largest deviations: point {worst['point']:.2e}, accuracy interval {worst['acc_ci']:.4f}, macro-F1 interval {worst['f1_ci']:.4f}, Dakshina interval {worst['dak_ci']:.4f}")
print("INTERVALS FAILED:\n" + "\n".join(bad) if bad else "intervals ok: every checked interval reproduces from the released predictions")
sys.exit(1 if bad else 0)
