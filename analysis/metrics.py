"""RQ1-RQ5 tables from analysis/items.csv (one row per model x task x split x variant x rotation x item).

    python analysis/metrics.py            # writes analysis/tables/*.csv and analysis/report.md

Statistics (following Deusser et al. 2026 and Nandakishore 2026):
  * every CI is a *cluster* bootstrap (1000 resamples): items sharing a premise (XNLI-bn) or passage (Belebele) are resampled together;
  * calibration uses the top-label probability `pmax` for every model, because vendors define `confidence` differently;
  * ECE: 15 equal-width bins and 15 equal-mass bins, plus the signed gap (mean confidence - accuracy), Brier and NLL;
  * temperature scaling is fitted on the disjoint DEV split (native text) and applied unchanged to test, native and romanized;
  * rotation averaging ("permutation marginalisation") averages label probabilities over the three option rotations;
  * confidence-gate transfer: a threshold chosen on native DEV is applied to romanized test.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).parent
OUT = HERE / "tables"
OUT.mkdir(exist_ok=True)
B = 1000
SEED = 0
USD_PER_TOKEN = 0.042 / 1e6
PRIMARY = {"bn_sentnob": "macro_f1", "bn_bnli": "accuracy", "bn_massive": "accuracy", "bn_belebele": "accuracy", "bn_sib200": "accuracy"}
NAME = {"bn_sentnob": "SentNoB", "bn_bnli": "XNLI-bn", "bn_massive": "MASSIVE", "bn_belebele": "Belebele", "bn_sib200": "SIB-200"}
GATE_TARGET = 0.90  # accepted-set accuracy the gate is tuned for on native dev


# ----------------------------------------------------------------------------- basic metrics
def macro_f1_from_counts(tp, fp, fn):
    d = 2 * tp + fp + fn
    f = np.where(d > 0, 2 * tp / np.maximum(d, 1), 0.0)
    present = (tp + fn) > 0  # classes that occur in gold
    return f[present].mean()


def ece_fixed(conf, ok, n=15):
    b = np.minimum((conf * n).astype(int), n - 1)
    return float(sum(abs(ok[b == k].mean() - conf[b == k].mean()) * (b == k).mean() for k in range(n) if (b == k).any()))


def ece_mass(conf, ok, n=15):
    idx = np.array_split(np.argsort(conf, kind="stable"), n)
    return float(sum(abs(ok[i].mean() - conf[i].mean()) * len(i) / len(conf) for i in idx if len(i)))


def aurc(conf, ok):
    o = np.argsort(-conf, kind="stable")
    return float((1 - np.cumsum(ok[o]) / np.arange(1, len(ok) + 1)).mean())


def acc_at_coverage(conf, ok, cov):
    o = np.argsort(-conf, kind="stable")[: max(1, int(round(cov * len(ok))))]
    return float(ok[o].mean())


def parse(df):
    """Attach numpy probability dicts once."""
    df = df.copy()
    df["pd"] = df.probs.map(json.loads)
    return df


def row_stats(pdicts, gold, T=1.0):
    """Per-row (pmax, correct, brier, nll) under temperature T (T=1: as returned)."""
    pm, ok, br, nl = [], [], [], []
    for p, g in zip(pdicts, gold):
        keys = list(p)
        v = np.clip(np.array([p[k] for k in keys], float), 1e-6, 1.0)
        if T != 1.0:
            v = v ** (1.0 / T)
        v = v / v.sum()
        j = int(v.argmax())
        pm.append(v[j])
        ok.append(keys[j] == g)
        y = np.array([k == g for k in keys], float)
        br.append(((v - y) ** 2).sum() + (0.0 if g in p else 1.0))
        nl.append(-np.log(v[keys.index(g)]) if g in p else -np.log(1e-6))
    return np.array(pm), np.array(ok, float), np.array(br), np.array(nl)


def fit_temperature(pdicts, gold):
    grid = np.exp(np.linspace(np.log(0.2), np.log(6), 41))
    nll = [row_stats(pdicts, gold, T)[3].mean() for T in grid]
    return float(grid[int(np.argmin(nll))])


# ----------------------------------------------------------------------------- cluster bootstrap
class Clusters:
    def __init__(self, cluster_ids):
        self.u, self.inv = np.unique(cluster_ids, return_inverse=True)
        self.k = len(self.u)
        order = np.argsort(self.inv, kind="stable")
        self.rows_of = np.split(order, np.cumsum(np.bincount(self.inv))[:-1])

    def draws(self, rng, b=B):
        return rng.integers(0, self.k, (b, self.k))

    def rows(self, draw):
        return np.concatenate([self.rows_of[c] for c in draw])


def headline(task, d, rng):
    """Primary metric with 95% cluster-bootstrap CI."""
    g, p = d.gold_id.to_numpy(), d.pred_id.to_numpy()
    cl = Clusters(d.cluster.to_numpy())
    classes = np.unique(g)

    def metric(rows):
        gg, pp = g[rows], p[rows]
        if PRIMARY[task] == "accuracy":
            return float((gg == pp).mean())
        tp = np.array([((gg == c) & (pp == c)).sum() for c in classes]); fp = np.array([((gg != c) & (pp == c)).sum() for c in classes])
        fn = np.array([((gg == c) & (pp != c)).sum() for c in classes])
        return macro_f1_from_counts(tp, fp, fn)

    est = metric(np.arange(len(d)))
    vals = [metric(cl.rows(dr)) for dr in cl.draws(rng, 400 if PRIMARY[task] == "macro_f1" else B)]
    lo, hi = np.percentile(vals, [2.5, 97.5])
    return est, lo, hi, cl.k


def paired_diff(task, a, b, rng):
    """metric(a) - metric(b) on items both models answered; cluster bootstrap CI."""
    m = a.merge(b, on="uid", suffixes=("_a", "_b"))
    if len(m) < 30:
        return None
    ca = (m.pred_id_a == m.gold_id_a).to_numpy(float); cb = (m.pred_id_b == m.gold_id_b).to_numpy(float)
    cl = Clusters(m.cluster_a.to_numpy())
    est = ca.mean() - cb.mean()
    vals = [(ca[r].mean() - cb[r].mean()) for r in (cl.rows(dr) for dr in cl.draws(rng, 500))]
    return len(m), est, *np.percentile(vals, [2.5, 97.5])


# ----------------------------------------------------------------------------- main
def main():
    rng = np.random.default_rng(SEED)
    df = parse(pd.read_csv(HERE / "items.csv"))
    # Belebele ben_Latn is a *human* romanization (separate parallel items); keep it apart from the synthetic one.
    df["vlabel"] = np.where((df.task == "bn_belebele") & (df.subset == "ben_Latn"), "human_roman", df.variant)
    ev = df[(df.split == "eval")]
    dev = df[(df.split == "dev")]

    # ---- coverage: share of the items Jev answered that each model also answered (Julia-1 rejects >20 options / >48-token options)
    cov = []
    for (t, v, sp, r), g in df[df.rot.notna()].groupby(["task", "variant", "split", "rot"]):
        ref = set(g[g.model == "jev-1.13.0"].uid)
        for m, d in g.groupby("model"):
            if ref:
                cov.append(dict(task=NAME[t], variant=v, split=sp, rot=r, model=m, answered=len(set(d.uid) & ref), expected=len(ref), coverage=len(set(d.uid) & ref) / len(ref)))
    pd.DataFrame(cov).to_csv(OUT / "coverage.csv", index=False)

    # ---- RQ1 accuracy / macro-F1 with cluster CIs, baselines, and paired differences vs Jev
    rows, paired = [], []
    for (t, v), g in ev[ev.rot == 0].groupby(["task", "vlabel"]):
        for m, d in g.groupby("model"):
            est, lo, hi, k = headline(t, d, rng)
            rows.append(dict(task=NAME[t], variant=v, model=m, n=len(d), clusters=k, metric=PRIMARY[t], value=est, ci_lo=lo, ci_hi=hi,
                             majority=np.nan if t == "bn_belebele" else d.gold_id.value_counts(normalize=True).iloc[0], chance=float(np.mean(1 / d.K))))
        ref = g[g.model == "jev-1.13.0"]
        for m, d in g.groupby("model"):
            if m != "jev-1.13.0" and len(ref):
                r = paired_diff(t, d, ref, rng)
                if r:
                    paired.append(dict(task=NAME[t], variant=v, model=m, vs="jev-1.13.0", n_common=r[0], acc_diff=r[1], ci_lo=r[2], ci_hi=r[3]))
    acc = pd.DataFrame(rows); acc.to_csv(OUT / "rq1_accuracy.csv", index=False)
    pd.DataFrame(paired).to_csv(OUT / "rq1_paired_vs_jev.csv", index=False)

    # ---- RQ2 calibration family (rot 0, as returned)
    cal = []
    for (t, v, m), d in ev[ev.rot == 0].groupby(["task", "vlabel", "model"]):
        pm, ok, br, nl = row_stats(d.pd, d.gold_id)
        cal.append(dict(task=NAME[t], variant=v, model=m, n=len(d), acc=ok.mean(), mean_conf=pm.mean(), signed_gap=pm.mean() - ok.mean(),
                        ece15=ece_fixed(pm, ok), ece15_mass=ece_mass(pm, ok), brier=br.mean(), nll=nl.mean(), aurc=aurc(pm, ok),
                        acc_at_80=acc_at_coverage(pm, ok, .8), acc_at_50=acc_at_coverage(pm, ok, .5)))
    calt = pd.DataFrame(cal); calt.to_csv(OUT / "rq2_calibration.csv", index=False)

    # ---- RQ2b temperature scaling fitted on native DEV, applied to test (native and romanized)
    ts, gate = [], []
    for (t, m), d in dev[dev.variant == "native"].groupby(["task", "model"]):
        if len(d) < 200:
            continue
        T = fit_temperature(d.pd, d.gold_id)
        pm_d, ok_d, _, _ = row_stats(d.pd, d.gold_id, T)
        # gate: smallest threshold whose accepted dev accuracy >= target (native dev, after scaling)
        taus = np.unique(pm_d); tau = next((x for x in taus if ok_d[pm_d >= x].mean() >= GATE_TARGET and (pm_d >= x).mean() >= .05), None)
        for v in ["native", "roman"]:
            e = ev[(ev.task == t) & (ev.model == m) & (ev.variant == v) & (ev.rot == 0)]
            if not len(e):
                continue
            b0 = row_stats(e.pd, e.gold_id); b1 = row_stats(e.pd, e.gold_id, T)
            ts.append(dict(task=NAME[t], model=m, test_variant=v, T=T, ece15_before=ece_fixed(b0[0], b0[1]), ece15_after=ece_fixed(b1[0], b1[1]),
                           brier_before=b0[2].mean(), brier_after=b1[2].mean(), nll_before=b0[3].mean(), nll_after=b1[3].mean()))
            if tau is not None:
                acc_mask = b1[0] >= tau
                gate.append(dict(task=NAME[t], model=m, test_variant=v, tau=tau, dev_target=GATE_TARGET, coverage=acc_mask.mean(), n_accepted=int(acc_mask.sum()), n=len(acc_mask),
                                 accepted_acc=b1[1][acc_mask].mean() if acc_mask.any() else np.nan, overall_acc=b1[1].mean()))
    tst = pd.DataFrame(ts); gt = pd.DataFrame(gate)
    tst.to_csv(OUT / "rq2_temperature_scaling.csv", index=False); gt.to_csv(OUT / "rq2_gate_transfer.csv", index=False)

    # ---- RQ3 script gap with paired CI (same items under native vs roman)
    gaps = []
    for (t, m), d in ev[ev.rot == 0].groupby(["task", "model"]):
        a = d[d.variant == "native"]; r = d[d.variant == "roman"]
        mm = a.merge(r, on="uid", suffixes=("_n", "_r"))
        if len(mm) < 30 or t == "bn_belebele":
            continue
        cn = (mm.pred_id_n == mm.gold_id_n).to_numpy(float); cr = (mm.pred_id_r == mm.gold_id_r).to_numpy(float)
        cl = Clusters(mm.cluster_n.to_numpy())
        vals = [cn[x].mean() - cr[x].mean() for x in (cl.rows(dr) for dr in cl.draws(rng, 500))]
        gaps.append(dict(task=NAME[t], model=m, n=len(mm), acc_native=cn.mean(), acc_roman=cr.mean(), gap=cn.mean() - cr.mean(),
                         ci_lo=np.percentile(vals, 2.5), ci_hi=np.percentile(vals, 97.5)))
    # Belebele: human romanization (ben_Beng vs ben_Latn, parallel items by position in the two configs)
    for m, d in ev[(ev.task == "bn_belebele") & (ev.rot == 0) & (ev.variant == "native")].groupby("model"):
        s = d.groupby("subset").correct.agg(["mean", "size"])
        if {"ben_Beng", "ben_Latn"} <= set(s.index):
            gaps.append(dict(task="Belebele (human roman.)", model=m, n=int(s["size"].min()), acc_native=s.loc["ben_Beng", "mean"],
                             acc_roman=s.loc["ben_Latn", "mean"], gap=s.loc["ben_Beng", "mean"] - s.loc["ben_Latn", "mean"], ci_lo=np.nan, ci_hi=np.nan))
    gap = pd.DataFrame(gaps); gap.to_csv(OUT / "rq3_script_gap.csv", index=False)

    # ---- RQ4 position bias: per-rotation accuracy, rotation-averaged accuracy, consistency, pick-vs-gold position shares
    nat = ev[ev.variant == "native"]
    rot_rows, pos_rows = [], []
    for (t, m), d in nat.groupby(["task", "model"]):
        per = d.groupby("rot").apply(lambda x: (x.pred_id == x.gold_id).mean(), include_groups=False)
        if set(per.index) != {0, 1, 2}:
            continue
        piv = {r: d[d.rot == r].set_index("uid") for r in (0, 1, 2)}
        common = piv[0].index.intersection(piv[1].index).intersection(piv[2].index)
        marg_ok, cons = [], []
        for u in common:
            ps = [piv[r].at[u, "pd"] for r in (0, 1, 2)]
            ids = set().union(*ps)
            mean = {k: np.mean([p.get(k, 0.0) for p in ps]) for k in ids}
            g = piv[0].at[u, "gold_id"]
            marg_ok.append(max(mean, key=mean.get) == g)
            cons.append(len({piv[r].at[u, "pred_id"] for r in (0, 1, 2)}) == 1)
        rot_rows.append(dict(task=NAME[t], model=m, n=len(common), acc_rot0=per[0], acc_rot1=per[1], acc_rot2=per[2], range=per.max() - per.min(),
                             acc_mean_of_rotations=per.mean(), acc_rotation_averaged=float(np.mean(marg_ok)), same_answer_all_rotations=float(np.mean(cons))))
        K = int(d.K.iloc[0])
        if K <= 7:
            sh_p = d.pos_pred.value_counts(normalize=True).reindex(range(K), fill_value=0); sh_g = d.pos_gold.value_counts(normalize=True).reindex(range(K), fill_value=0)
            pos_rows.append(dict(task=NAME[t], model=m, K=K, **{f"pick_pos{j}": sh_p[j] for j in range(K)}, max_abs_pick_minus_gold=float((sh_p - sh_g).abs().max())))
    rot = pd.DataFrame(rot_rows); rot.to_csv(OUT / "rq4_rotation.csv", index=False)
    pos = pd.DataFrame(pos_rows); pos.to_csv(OUT / "rq4_position_shares.csv", index=False)

    # ---- RQ5 cost / latency (Jev latency is client-side incl. network; open models: GPU kernel time per item on Kaggle T4)
    lat = ev[ev.rot == 0].groupby("model").agg(median_latency_s=("latency_s", "median"), mean_input_tokens=("input_tokens", "mean"), items=("uid", "size"))
    lat["usd_per_1k_decisions"] = np.where(lat.index.str.startswith("jev"), lat.mean_input_tokens * USD_PER_TOKEN * 1000, 0.0)
    lat.to_csv(OUT / "rq5_cost_latency.csv")

    with (HERE / "report.md").open("w") as f:
        def put(title, t, idx=False):
            f.write(f"## {title}\n\n{t.round(3).to_markdown(index=idx)}\n\n")
        put("RQ1 accuracy / macro-F1, rot0, 95% cluster-bootstrap CI", acc)
        put("RQ1 paired difference vs Jev (accuracy, cluster CI)", pd.DataFrame(paired))
        put("RQ2 calibration, rot0 (pmax)", calt)
        put("RQ2b temperature scaling (T fitted on native dev)", tst)
        put("RQ2c confidence-gate transfer (threshold tuned on native dev for 90% accepted accuracy)", gt)
        put("RQ3 script gap (same items, paired cluster CI)", gap)
        put("RQ4 rotation", rot)
        put("RQ4 pick positions (K<=7)", pos)
        put("RQ5 cost / latency", lat.reset_index())
    print((HERE / "report.md").read_text()[:6000])


if __name__ == "__main__":
    main()
