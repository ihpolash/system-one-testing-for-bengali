"""Independent check of the headline numbers in paper/numbers.tex against the accuracy table (analysis/tables/rq1_accuracy.csv) and the released predictions.
Recomputes each number from scratch, without importing make_tables.py, verifies results/MANIFEST.sha256, and exits non-zero on any mismatch.   python analysis/audit_numbers.py"""
import hashlib, re, sys
from pathlib import Path
import pandas as pd

A = Path(__file__).parent
N = dict(re.findall(r"\\newcommand\{\\(\w+)\}\{(.*?)\}$", (A.parent / "paper" / "numbers.tex").read_text(), re.M))
r1 = pd.read_csv(A / "tables" / "rq1_accuracy.csv")
bad = []

def check(name, value, fmt="{:.3f}"):
    got = fmt.format(value)
    if got != N[name].lstrip("+"):
        bad.append(f"{name}: numbers.tex {N[name]} vs recomputed {got}")

J = "jev-1.13.0"
x = r1[(r1.model == J) & (r1.task == "Belebele") & (r1.variant == "native")].iloc[0]
check("jevBelebele", x.value); check("jevBelebeleLo", x.ci_lo); check("jevBelebeleHi", x.ci_hi)
# Jev has the highest point estimate on every task among the systems run on the full test sets
for t in ("Belebele", "SIB-200", "XNLI-bn", "MASSIVE", "SentNoB"):
    full = r1[(r1.task == t) & (r1.variant == "native") & (~r1.model.str.contains("flash"))]
    assert full.loc[full.value.idxmax(), "model"] == J, f"Jev is not top on {t}"
# every system is less accurate on rule-based romanization than on Bengali, on every task where both were run
p = r1.pivot_table(index=["model", "task"], columns="variant", values="value").dropna(subset=["native", "roman"])
if (p.roman >= p.native).any():
    bad.append("some system scores at least as high on rule-based romanization as on Bengali: " + ", ".join(f"{m}/{t}" for (m, t) in p[p.roman >= p.native].index))
# per-model accuracy cells quoted in the text
tags = {"jev-1.13.0": "jev", "gemma-4-E4B-it": "gemma", "d3-mini": "mini", "d3-nano": "nano", "d3-lite": "lite", "laya-bangla v2": "layabn", "laya-multilingual": "layaml", "kev-4b": "kevmd", "kev-0.8b": "kevsm"}
TK = {"Belebele": "Bel", "SIB-200": "Sib", "XNLI-bn": "Xnli", "MASSIVE": "Mas", "SentNoB": "Sent"}
for m, k in tags.items():
    for t, tk in TK.items():
        for v, vk in (("native", "Nat"), ("roman", "Rom")):
            g = r1[(r1.model == m) & (r1.task == t) & (r1.variant == v)]
            if not g.empty and f"acc{k}{tk}{vk}" in N:
                check(f"acc{k}{tk}{vk}", g.value.iloc[0])
# Dakshina cross-script agreement, recomputed from the released per-sentence predictions (not from analysis/dak_items.csv)
dk = pd.read_csv(A.parent / "results" / "predictions_dakshina.csv.gz")
dtag = {"jev-1.13.0": "jev", "gemma-4-E4B-it": "gemma", "d3-flash (4/8-bit)": "flash", "d3-mini": "mini", "d3-nano": "nano", "d3-lite": "lite", "d3-edge": "edge", "laya-bangla v2": "layabn", "laya-multilingual": "layaml", "julia-1": "julia", "kev-4b": "kevmd", "kev-0.8b": "kevsm"}
n_ns_beats_rule = 0
for m, g in dk.groupby("model"):
    w = g.pivot(index="id", columns="variant", values="choice").dropna()
    ag = {v: (w[v] == w["native"]).mean() for v in ("dakshina", "roman_nat", "roman")}
    n_ns_beats_rule += ag["dakshina"] > ag["roman"]
    for v, vn in (("dakshina", "Ns"), ("roman_nat", "Nat"), ("roman", "Rule")):
        check(f"dak{dtag[m]}{vn}", ag[v])
assert dk.model.nunique() == int(N["dakSystems"]), "number of systems differs from numbers.tex"
check("dakNsBeatsRule", n_ns_beats_rule, "{:d}") if int(N["dakNsBeatsRule"]) == int(n_ns_beats_rule) else bad.append(f"native-speaker beats rule-based for {n_ns_beats_rule} systems by point estimate vs {N['dakNsBeatsRule']} with CI excluding 0")
# released files match their recorded checksums
for line in (A.parent / "results" / "MANIFEST.sha256").read_text().splitlines():
    h, f = line.split("  ", 1)
    if hashlib.sha256((A.parent / f).read_bytes()).hexdigest() != h:
        bad.append(f"checksum mismatch: {f}")
print("AUDIT FAILED:\n" + "\n".join(bad) if bad else "audit ok: headline numbers match an independent recomputation")
sys.exit(1 if bad else 0)
