"""Option-label language ablation (Jev): English vs Bengali option names, native text, rotation 0, same items.
Reads Jev responses from the cache; run: python analysis/label_ablation.py. Writes analysis/tables/rq4_label_language.csv."""
import os, subprocess, sys, json
from pathlib import Path
import numpy as np, pandas as pd

HERE = Path(__file__).parent
CODE = r'''
import json, os, sys
sys.path.insert(0, "%s")
from jev_benchmarking.cache import ResponseCache, request_key
from jev_benchmarking.tasks import get_tasks
jev = ResponseCache(); out = []
for t in get_tasks(["bn_sentnob", "bn_bnli", "bn_sib200"]):
    lim = 1500 if t.name == "bn_bnli" else None
    for e in t.examples("eval", limit=lim):
        r = jev.get(request_key("jev-1.13.0", e.state, e.questions))
        if r is None: continue
        a = r["answers"]["answer"]; p = a["probabilities"]
        prem = e.state.get("premise", e.uid) if isinstance(e.state, dict) else e.uid
        out.append(dict(task=t.name, uid=e.uid, cluster=str(prem), ok=int(a["choice"] == e.gold["answer"]), pmax=max(p.values()), pred=a["choice"], gold=e.gold["answer"]))
print(json.dumps(out, ensure_ascii=False))
''' % str(HERE.parent / "harness")


def run(labels):
    env = dict(os.environ, BN_LABELS=labels, BN_VARIANT="native", BN_ROT="0", BN_QLANG="en", PYTHONPATH=str(HERE.parent / "harness"))
    r = subprocess.run([sys.executable, "-c", CODE], env=env, capture_output=True, text=True, cwd=str(HERE.parent / "harness"))
    return pd.DataFrame(json.loads(r.stdout.strip().splitlines()[-1]))


def main():
    rng = np.random.default_rng(0)
    en, bn, bn2 = run("en"), run("bn"), run("bn2")
    rows = []
    for t in en.task.unique():
        a = en[en.task == t].merge(bn[bn.task == t], on="uid", suffixes=("_en", "_bn"))
        if len(a) < 30:
            continue
        cl, inv = np.unique(a.cluster_en, return_inverse=True)
        members = [np.where(inv == i)[0] for i in range(len(cl))]
        d = a.ok_bn.to_numpy(float) - a.ok_en.to_numpy(float)
        vals = [d[np.concatenate([members[c] for c in rng.integers(0, len(cl), len(cl))])].mean() for _ in range(500)]
        rows.append(dict(task=t, n=len(a), acc_en_labels=a.ok_en.mean(), acc_bn_labels=a.ok_bn.mean(), diff_bn_minus_en=d.mean(),
                         ci_lo=np.percentile(vals, 2.5), ci_hi=np.percentile(vals, 97.5),
                         mean_conf_en=a.pmax_en.mean(), mean_conf_bn=a.pmax_bn.mean(),
                         same_correctness_rate=float(np.mean(a.ok_en == a.ok_bn))))
    # sensitivity: alternative Bengali wording for the NLI labels
    a = en[en.task == "bn_bnli"].merge(bn2[bn2.task == "bn_bnli"], on="uid", suffixes=("_en", "_bn2")).merge(bn[bn.task == "bn_bnli"][["uid", "ok"]].rename(columns={"ok": "ok_bn"}), on="uid")
    if len(a):
        rows.append(dict(task="bn_bnli (alt. wording নিহিত/বিরোধ)", n=len(a), acc_en_labels=a.ok_en.mean(), acc_bn_labels=a.ok_bn2.mean(), diff_bn_minus_en=(a.ok_bn2 - a.ok_en).mean(),
                         ci_lo=np.nan, ci_hi=np.nan, mean_conf_en=a.pmax_en.mean(), mean_conf_bn=a.pmax_bn2.mean(), same_correctness_rate=float(np.mean(a.ok_en == a.ok_bn2))))
    out = pd.DataFrame(rows); out.to_csv(HERE / "tables" / "rq4_label_language.csv", index=False)
    print(out.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
