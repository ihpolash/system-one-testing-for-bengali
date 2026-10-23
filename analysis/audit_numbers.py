"""Independent check of the headline numbers in paper/numbers.tex against the committed item-level correctness table
(analysis/tables/human_items_all_models.csv) and the accuracy table (analysis/tables/rq1_accuracy.csv).
Recomputes each number from scratch (and verifies results/MANIFEST.sha256), without importing make_tables.py, and exits non-zero on any mismatch.   python analysis/audit_numbers.py"""
import re, sys
from pathlib import Path
import pandas as pd
from scipy.stats import kendalltau

A = Path(__file__).parent
N = dict(re.findall(r"\\newcommand\{\\(\w+)\}\{(.*?)\}$", (A.parent / "paper" / "numbers.tex").read_text(), re.M))
d = pd.read_csv(A / "tables" / "human_items_all_models.csv"); d = d[d.answered == 1]
p = d.pivot_table(index=["model", "dataset", "id"], columns="variant", values="ok")
acc = p.groupby("model").mean()
r1 = pd.read_csv(A / "tables" / "rq1_accuracy.csv")
bad = []

def check(name, value, fmt="{:.3f}"):
    got = fmt.format(value)
    if got != N[name].lstrip("+"):
        bad.append(f"{name}: numbers.tex {N[name]} vs recomputed {got}")

J = "jev-1.13.0"
for var, key in (("native_edit", "jevBengali"), ("roman_edit", "jevRule"), ("roman_nat_edit", "jevNat"), ("human", "jevHuman")):
    check(key, acc.loc[J, var])
check("jevLossHuman", 100 * (acc.loc[J, "native_edit"] - acc.loc[J, "human"]), "{:.1f}")
check("jevLossRule", 100 * (acc.loc[J, "native_edit"] - acc.loc[J, "roman_edit"]), "{:.1f}")
check("jevHumanVsRule", 100 * (acc.loc[J, "human"] - acc.loc[J, "roman_edit"]), "{:.1f}")
check("nHuman", p.loc[J].shape[0], "{:d}")
a8 = acc.drop(index="julia-1")
check("tauRule", kendalltau(a8.human, a8.roman_edit)[0], "{:.2f}")
check("tauNat", kendalltau(a8.human, a8.roman_nat_edit)[0], "{:.2f}")
x = r1[(r1.model == J) & (r1.task == "Belebele") & (r1.variant == "native")].iloc[0]
check("jevBelebele", x.value)
for t, k in (("Belebele", "Bel"), ("SIB-200", "Sib"), ("XNLI-bn", "Xnli"), ("MASSIVE", "Mas"), ("SentNoB", "Sent")):  # Jev tops every full-set model on all five tasks
    full = r1[(r1.task == t) & (r1.variant == "native") & (~r1.model.str.contains("flash"))]
    assert full.loc[full.value.idxmax(), "model"] == J, f"Jev is not top on {t}"
# common-item rank agreement: items every system answered (recomputed here, not imported)
wide = d.pivot_table(index=["dataset", "id"], columns=["model", "variant"], values="ok")
ms = sorted(acc.index); need = [(m, v) for m in ms for v in ("human", "roman_edit", "roman_nat_edit")]
com = wide.dropna(subset=need)
accs = pd.DataFrame({v: [com[(m, v)].mean() for m in ms] for v in ("human", "roman_edit", "roman_nat_edit")}, index=ms)
check("nCommon", len(com), "{:d}")
check("tauComRule", kendalltau(accs.human, accs.roman_edit)[0], "{:.2f}")
check("tauComNat", kendalltau(accs.human, accs.roman_nat_edit)[0], "{:.2f}")
# released files match their recorded checksums
import hashlib
for line in (A.parent / "results" / "MANIFEST.sha256").read_text().splitlines():
    h, f = line.split("  ", 1)
    if hashlib.sha256((A.parent / f).read_bytes()).hexdigest() != h:
        bad.append(f"checksum mismatch: {f}")
print("AUDIT FAILED:\n" + "\n".join(bad) if bad else "audit ok: headline numbers match an independent recomputation")
sys.exit(1 if bad else 0)
