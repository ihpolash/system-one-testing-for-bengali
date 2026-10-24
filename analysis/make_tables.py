"""Generate paper/tables/*.tex and paper/numbers.tex from the stored results.   python analysis/make_tables.py
Nothing in the paper's results is typed by hand: tables are written here, and the prose quotes numbers through the macros in numbers.tex.
Inputs: analysis/tables/*.csv, analysis/items.csv, harness/cache/responses.db (spend), kaggle/out_*.txt (GPU time), data/split_hashes.json."""
import glob, json, re, sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).parent
ROOT = HERE.parent
T = HERE / "tables"
OUT = ROOT / "paper" / "tables"
OUT.mkdir(parents=True, exist_ok=True)
NUM = {}   # macro name -> text

NAME = {"jev-1.13.0": "Jev", "d3-flash (4-bit)": r"d3-flash (4-bit)$^\dagger$", "gemma-4-E4B-it": "Gemma-4-E4B", "d3-mini": "d3-mini", "d3-nano": "d3-nano", "d3-lite": "d3-lite",
        "d3-edge": "d3-edge", "laya-bangla v2": "laya-bangla", "laya-multilingual": "Laya-multilingual", "julia-1": "Julia-1", "kev-4b": "Kev-4B", "kev-0.8b": "Kev-0.8B"}
ORDER = ["jev-1.13.0", "d3-flash (4-bit)", "gemma-4-E4B-it", "d3-mini", "d3-nano", "kev-4b", "d3-lite", "laya-bangla v2", "d3-edge", "kev-0.8b", "laya-multilingual", "julia-1"]
TASKS = [("Belebele", "Belebele"), ("SIB-200", "SIB-200"), ("XNLI-bn", "XNLI-bn"), ("MASSIVE", "MASSIVE"), ("SentNoB", "SentNoB")]


def f3(x):
    return "--" if pd.isna(x) else f"{x:.3f}"


def pts(x, signed=True):
    return "--" if pd.isna(x) else (f"{100*x:+.1f}" if signed else f"{100*x:.1f}")


def ci(lo, hi):
    return f"[{100*lo:+.1f}, {100*hi:+.1f}]"


def write(name, text):
    (OUT / name).write_text(text)


def macro(name, value):
    NUM[name] = str(value)


# ---------------------------------------------------------------- Table 1: tasks and splits
split = json.load(open(ROOT / "data" / "split_hashes.json"))
tasks_rows = [
    ("Belebele", "reading comprehension", "4 options", "accuracy", "human translation (FLORES-200)", f"{split['belebele']['n']} / 900"),
    ("SIB-200", "topic", "7 options", "accuracy", "human translation (FLORES-200)", f"{split['sib200']['n']} / 204"),
    ("XNLI-bn", "natural language inference", "3 options", "accuracy", "machine translation of XNLI", f"{split['bnli']['n']:,} / 1,500"),
    ("MASSIVE bn-BD", "intent", "60 options", "accuracy", "human translation", f"{split['massive']['n']:,} / 1,500"),
    ("SentNoB", "sentiment", "3 options", "macro-F1", "native social-media comments", f"{split['sentnob']['n']:,} / 1,586"),
]
write("tab_tasks.tex", "\\begin{tabular}{@{}llllll@{}}\\toprule\nDataset & Task & Options & Metric & Text origin & Test items (all / used) \\\\\\midrule\n" +
      "\n".join(" & ".join(r) + " \\\\" for r in tasks_rows) + "\n\\bottomrule\\end{tabular}\n")
for k in ("belebele", "sib200", "massive", "bnli", "sentnob"):
    macro(f"n{k.replace('sib200', 'sib')}", split[k]["n"])

# ---------------------------------------------------------------- Table 2: native (and romanized) accuracy on the test sets
a = pd.read_csv(T / "rq1_accuracy.csv")
rows = []
for m in [x for x in ORDER if not x.startswith("d3-flash")]:   # d3-flash ran a subset: see tab_flash_subset
    cells = []
    for t, _ in TASKS:
        nat = a[(a.model == m) & (a.task == t) & (a.variant == "native")]
        rom = a[(a.model == m) & (a.task == t) & (a.variant == "roman")]
        if nat.empty:
            cells.append("--"); continue
        s = f3(nat.value.iloc[0])
        s += f" ({f3(rom.value.iloc[0])})" if not rom.empty else ""
        if m == "laya-bangla v2" and t in ("MASSIVE", "SIB-200"):
            s += r"$^\ddagger$"
        cells.append(s)
    rows.append(f"{NAME[m]} & " + " & ".join(cells) + " \\\\")
# baselines: majority-class and uniform-random, separately (SentNoB is macro-F1, so both are macro-F1 there)
maj = a[(a.model == "jev-1.13.0") & (a.variant == "native")].set_index("task")
_g = pd.read_csv(HERE / "items.csv", usecols=["model", "task", "split", "variant", "rot", "gold_id"])
_g = _g[(_g.model == "jev-1.13.0") & (_g.task == "bn_sentnob") & (_g.split == "eval") & (_g.variant == "native") & (_g.rot == 0)]
_p = _g.gold_id.value_counts(normalize=True).to_numpy(); _K = len(_p)
sent_major = (2 * _p.max() / (1 + _p.max())) / _K                                   # always the majority class: F1 = 2p/(1+p) on that class, 0 on the others
sent_uniform = float(np.mean(2 * _p * (1 / _K) / (_p + 1 / _K)))                    # uniform random guess: precision p_i, recall 1/K for each class
macro("sentMajorityFone", f3(sent_major)); macro("sentUniformFone", f3(sent_uniform))
rows_major, rows_chance = [], []
for t, _ in TASKS:
    rows_major.append("--" if t == "Belebele" else (f3(sent_major) if t == "SentNoB" else f3(maj.loc[t, "majority"])))
    rows_chance.append(f3(sent_uniform) if t == "SentNoB" else f3(maj.loc[t, "chance"]))
rows = rows + ["Majority class & " + " & ".join(rows_major) + " \\\\", "Uniform random & " + " & ".join(rows_chance) + " \\\\"]
write("tab_main.tex", "\\begin{tabular}{@{}lccccc@{}}\\toprule\nModel & Belebele & SIB-200 & XNLI-bn & MASSIVE & SentNoB \\\\\\midrule\n" + "\n".join(rows[:-2]) + "\n\\midrule\n" + "\n".join(rows[-2:]) + "\n\\bottomrule\\end{tabular}\n")

# d3-flash subset comparison (flash ran a 400-item-per-task hash-ordered subset): same items for Jev
it = pd.read_csv(HERE / "items.csv", usecols=["model", "task", "split", "variant", "rot", "uid", "gold_id", "pred_id", "correct"])
it = it[(it.split == "eval") & (it.rot == 0) & it.variant.isin(["native", "roman"])]
fl = it[it.model == "d3-flash (4/8-bit)"][["task", "variant", "uid"]].drop_duplicates()
sub = it.merge(fl, on=["task", "variant", "uid"])


def score(g, task):
    if task == "bn_sentnob":
        fs = []
        for c in g.gold_id.unique():
            tp = ((g.gold_id == c) & (g.pred_id == c)).sum(); fp = ((g.gold_id != c) & (g.pred_id == c)).sum(); fn = ((g.gold_id == c) & (g.pred_id != c)).sum()
            fs.append(0 if tp == 0 else 2 * tp / (2 * tp + fp + fn))
        return float(np.mean(fs))
    return float(g.correct.mean())


names = {"bn_belebele": "Belebele", "bn_sib200": "SIB-200", "bn_bnli": "XNLI-bn", "bn_massive": "MASSIVE", "bn_sentnob": "SentNoB"}
srows = []
for m, lab in (("jev-1.13.0", "Jev"), ("d3-flash (4/8-bit)", "d3-flash (4-bit)")):
    cells = []
    for t, tn in (("bn_belebele", "Belebele"), ("bn_sib200", "SIB-200"), ("bn_bnli", "XNLI-bn"), ("bn_massive", "MASSIVE"), ("bn_sentnob", "SentNoB")):
        g_n = sub[(sub.model == m) & (sub.task == t) & (sub.variant == "native")]; g_r = sub[(sub.model == m) & (sub.task == t) & (sub.variant == "roman")]
        s = f3(score(g_n, t)) if len(g_n) else "--"
        s += f" ({f3(score(g_r, t))})" if len(g_r) else ""
        cells.append(s)
    srows.append(f"{lab} & " + " & ".join(cells) + " \\\\")
nflash = sub[(sub.model == "d3-flash (4/8-bit)") & (sub.variant == "native")].groupby("task").size()
macro("flashNmin", int(nflash.min())); macro("flashNmax", int(nflash.max()))
write("tab_flash_subset.tex", "\\begin{tabular}{@{}lccccc@{}}\\toprule\nOn the d3-flash subset & Belebele & SIB-200 & XNLI-bn & MASSIVE & SentNoB \\\\\\midrule\n" + "\n".join(srows) + "\n\\bottomrule\\end{tabular}\n")

tag = {"jev-1.13.0": "jev", "gemma-4-E4B-it": "gemma", "d3-flash (4-bit)": "flash", "d3-mini": "mini", "d3-nano": "nano", "d3-lite": "lite", "d3-edge": "edge", "laya-bangla v2": "layabn", "laya-multilingual": "layaml", "julia-1": "julia", "kev-4b": "kevmd", "kev-0.8b": "kevsm"}

# ---------------------------------------------------------------- Table 4: calibration (mean over XNLI-bn, MASSIVE, SentNoB; those with a dev split)
c = pd.read_csv(T / "rq2_calibration.csv"); ts = pd.read_csv(T / "rq2_temperature_scaling.csv")
rows = []
for m in ORDER:
    if m == "d3-flash (4-bit)":
        continue
    cs = c[(c.model == m) & c.task.isin(["XNLI-bn", "MASSIVE", "SentNoB"])]
    tt = ts[(ts.model == m)]
    if cs.empty or tt.empty:
        continue
    def mean_ece(df, var, col):
        s = df[df.variant == var] if "variant" in df else df
        return s[col].mean()
    nat_raw = cs[cs.variant == "native"].ece15.mean(); rom_raw = cs[cs.variant == "roman"].ece15.mean()
    nat_ts = tt[tt.test_variant == "native"].ece15_after.mean(); rom_ts = tt[tt.test_variant == "roman"].ece15_after.mean()
    rows.append(f"{NAME[m]} & {f3(nat_raw)} & {f3(nat_ts)} & {f3(rom_raw)} & {f3(rom_ts)} \\\\")
    macro(f"ece{tag[m]}NatRaw", f3(nat_raw)); macro(f"ece{tag[m]}NatTs", f3(nat_ts)); macro(f"ece{tag[m]}RomRaw", f3(rom_raw)); macro(f"ece{tag[m]}RomTs", f3(rom_ts))
write("tab_calibration.tex", "\\begin{tabular}{@{}lcccc@{}}\\toprule\n & \\multicolumn{2}{c}{Bengali script} & \\multicolumn{2}{c}{Rule-based romanization} \\\\\\cmidrule(lr){2-3}\\cmidrule(l){4-5}\n"
      "Model & ECE raw & ECE scaled & ECE raw & ECE scaled \\\\\\midrule\n" + "\n".join(rows) + "\n\\bottomrule\\end{tabular}\n")
x = ts[(ts.model == "julia-1") & (ts.task == "XNLI-bn") & (ts.test_variant == "native")].iloc[0]
macro("juliaXnliEceRaw", f3(x.ece15_before)); macro("juliaXnliEceTs", f3(x.ece15_after))

# ---------------------------------------------------------------- rotation consistency (Fig. 6) and per-task table (appendix)
rot = pd.read_csv(T / "rq4_rotation.csv"); rot = rot[rot.model != "d3-flash (4/8-bit)"]
cons = rot.groupby("model").apply(lambda g: np.average(g.same_answer_all_rotations, weights=g.n), include_groups=False)
for m, k in tag.items():
    if m in cons.index:
        macro(f"cons{k}", f"{100*cons.loc[m]:.0f}")
rows = []
for m in ORDER:
    g = rot[rot.model == m].set_index("task")
    if g.empty:
        continue
    rows.append(f"{NAME[m]} & " + " & ".join(f"{100*g.loc[t, 'range']:.1f} / {100*g.loc[t, 'same_answer_all_rotations']:.0f}\\%" if t in g.index else "--" for t, _ in TASKS) + " \\\\")
write("tab_rotation.tex", "\\begin{tabular}{@{}lccccc@{}}\\toprule\nModel & Belebele & SIB-200 & XNLI-bn & MASSIVE & SentNoB \\\\\\midrule\n" + "\n".join(rows) + "\n\\bottomrule\\end{tabular}\n")

# ---------------------------------------------------------------- Table (appendix): accuracy with 95% cluster-bootstrap CI
rows = []
for m in [x for x in ORDER if not x.startswith("d3-flash")]:
    cells = []
    for t, _ in TASKS:
        g = a[(a.model == m) & (a.task == t) & (a.variant == "native")]
        cells.append("--" if g.empty else f"{g.value.iloc[0]:.3f} [{g.ci_lo.iloc[0]:.3f}, {g.ci_hi.iloc[0]:.3f}]")
    rows.append(f"{NAME[m]} & " + " & ".join(cells) + " \\\\")
write("tab_main_ci.tex", "\\begin{tabular}{@{}lccccc@{}}\\toprule\nModel & Belebele & SIB-200 & XNLI-bn & MASSIVE & SentNoB \\\\\\midrule\n" + "\n".join(rows) + "\n\\bottomrule\\end{tabular}\n")

# ---------------------------------------------------------------- reproduction / audit numbers
bel = a[(a.model == "jev-1.13.0") & (a.task == "Belebele") & (a.variant == "native")].iloc[0]
macro("jevBelebele", f3(bel.value)); macro("jevBelebeleLo", f3(bel.ci_lo)); macro("jevBelebeleHi", f3(bel.ci_hi))
for m, k in (("laya-multilingual", "layaml"), ("laya-bangla v2", "layabn")):
    for t, kk in (("MASSIVE", "Massive"), ("SIB-200", "Sib"), ("SentNoB", "Sentnob"), ("XNLI-bn", "Xnli")):
        g = a[(a.model == m) & (a.task == t) & (a.variant == "native")]
        if not g.empty:
            macro(f"{k}Native{kk}", f3(g.value.iloc[0]))
# Jev retest and wording checks are measured by scripts that print them; the values are recorded here from RESULTS_AUDIT.md
audit = (HERE / "RESULTS_AUDIT.md").read_text()
macro("jevRetestSame", re.search(r"same answer (\d+)%", audit).group(1))

# ---------------------------------------------------------------- cost: Jev spend for this study and GPU hours (from run logs)
con = sqlite3.connect(ROOT / "harness" / "cache" / "responses.db")
tok, n = con.execute("select coalesce(sum(input_tokens),0), count(*) from responses where task like 'bn_%' and model like 'jev-%'").fetchone()
macro("jevRequests", f"{n:,}".replace(",", "{,}")); macro("jevTokensM", f"{tok/1e6:.1f}"); macro("jevUsd", f"{tok*0.042/1e6:.2f}")
hours = 0.0
for f in glob.glob(str(ROOT / "kaggle" / "out_*.txt")):
    mm = re.findall(r"ALL DONE ([0-9.]+)", open(f, errors="ignore").read())
    hours += sum(float(x) for x in mm)
for f in glob.glob(str(ROOT / "kaggle" / "out_k*" / "bn-s1-main-k.log")):   # Kev runs, including the attempts that failed and were rerun
    hours += sum(float(x) for x in re.findall(r"ALL DONE ([0-9.]+)", " ".join(d.get("data", "") for d in json.load(open(f)))))
macro("gpuHours", f"{hours:.0f}")


# ---------------------------------------------------------------- single cells quoted in the prose
TK = {"Belebele": "Bel", "SIB-200": "Sib", "XNLI-bn": "Xnli", "MASSIVE": "Mas", "SentNoB": "Sent"}
for m, k in tag.items():
    for t, tk in TK.items():
        for v, vk in (("native", "Nat"), ("roman", "Rom")):
            g = a[(a.model == m) & (a.task == t) & (a.variant == v)]
            if not g.empty:
                macro(f"acc{k}{tk}{vk}", f3(g.value.iloc[0]))
for m, k in (("jev-1.13.0", "jev"), ("d3-flash (4/8-bit)", "flash")):
    for t, tk in (("bn_xnli", "Xnli"),):
        pass
for tname, tk in (("bn_bnli", "Xnli"),):
    for m, k in (("jev-1.13.0", "jev"), ("d3-flash (4/8-bit)", "flash")):
        macro(f"sub{k}{tk}", f3(score(sub[(sub.model == m) & (sub.task == tname) & (sub.variant == "native")], tname)))
mm = re.search(r"macro-F1 (0\.\d+) \(default English\), (0\.\d+) \(options only\), (0\.\d+) \(Bengali wording\)", audit)
macro("layamlSentDefault", mm.group(1)); macro("layamlSentOpts", mm.group(2)); macro("layamlSentBn", mm.group(3))
macro("jevBelebeleZenodo", re.search(r"recomputed from the authors' Zenodo responses (0\.\d+)", audit).group(1))

# ---------------------------------------------------------------- confidence gate fitted on native dev text, applied to romanized text (MASSIVE)
gt = pd.read_csv(T / "rq2_gate_transfer.csv")
for m, k in (("jev-1.13.0", "jev"), ("d3-mini", "mini"), ("d3-lite", "lite"), ("laya-bangla v2", "layabn")):
    for v, vk in (("native", "Nat"), ("roman", "Rom")):
        g = gt[(gt.model == m) & (gt.task == "MASSIVE") & (gt.test_variant == v)].iloc[0]
        macro(f"gate{k}{vk}Cov", f"{100*g.coverage:.0f}"); macro(f"gate{k}{vk}Acc", f"{100*g.accepted_acc:.0f}")
macro("gateTarget", "90")
ll = pd.read_csv(T / "rq4_label_language.csv").iloc[:3]
macro("labelMaxDiff", f"{100*ll.diff_bn_minus_en.abs().max():.1f}")

# ---------------------------------------------------------------- accepted-item counts behind the gate rows
for m, k in (("jev-1.13.0", "jev"), ("d3-mini", "mini"), ("laya-bangla v2", "layabn")):
    for v, vk in (("native", "Nat"), ("roman", "Rom")):
        g = gt[(gt.model == m) & (gt.task == "MASSIVE") & (gt.test_variant == v)].iloc[0]
        macro(f"gate{k}{vk}N", f"{int(g.n_accepted):,}".replace(",", "{,}"))

# ---------------------------------------------------------------- Brier score and signed gap (confidence minus accuracy), Bengali vs rule-based, mean over XNLI-bn, MASSIVE, SentNoB
brow = []
for m in ORDER:
    if m == "d3-flash (4-bit)":
        continue
    cs = c[(c.model == m) & c.task.isin(["XNLI-bn", "MASSIVE", "SentNoB"])]
    if cs.empty or cs[cs.variant == "roman"].empty:
        continue
    f = lambda var, col: cs[cs.variant == var][col].mean()
    brow.append(f"{NAME[m]} & {f3(f('native', 'brier'))} & {f3(f('roman', 'brier'))} & {f('native', 'signed_gap'):+.3f} & {f('roman', 'signed_gap'):+.3f} \\\\")
write("tab_cal_brier.tex", "\\begin{tabular}{@{}lcccc@{}}\\toprule\n & \\multicolumn{2}{c}{Brier score} & \\multicolumn{2}{c}{Confidence $-$ accuracy} \\\\\\cmidrule(lr){2-3}\\cmidrule(l){4-5}\nModel & Bengali & Rule-based & Bengali & Rule-based \\\\\\midrule\n" + "\n".join(brow) + "\n\\bottomrule\\end{tabular}\n")

# ---------------------------------------------------------------- task-level ECE (the primary calibration measure)
trow = []
for m in ORDER:
    if m == "d3-flash (4-bit)":
        continue
    cs = c[(c.model == m)]
    cells = []
    for t in ("XNLI-bn", "MASSIVE", "SentNoB"):
        for var in ("native", "roman"):
            g = cs[(cs.task == t) & (cs.variant == var)]
            cells.append(f3(g.ece15.iloc[0]) if len(g) else "--")
    if all(x == "--" for x in cells):
        continue
    trow.append(f"{NAME[m]} & " + " & ".join(cells) + " \\\\")
write("tab_cal_tasks.tex", "\\begin{tabular}{@{}lcccccc@{}}\\toprule\n & \\multicolumn{2}{c}{XNLI-bn} & \\multicolumn{2}{c}{MASSIVE} & \\multicolumn{2}{c}{SentNoB} \\\\\\cmidrule(lr){2-3}\\cmidrule(lr){4-5}\\cmidrule(l){6-7}\nModel & Bengali & Rule & Bengali & Rule & Bengali & Rule \\\\\\midrule\n" + "\n".join(trow) + "\n\\bottomrule\\end{tabular}\n")

# ---------------------------------------------------------------- accuracy lost under rule-based romanization: mean over the tasks where both were run (points)
_pv = a.pivot_table(index=["model", "task"], columns="variant", values="value").dropna(subset=["native", "roman"])
_drop = (100 * (_pv.native - _pv.roman)).groupby("model").mean()
for m, k in tag.items():
    if m in _drop.index:
        macro(f"drop{k}", f"{_drop.loc[m]:.1f}")
macro("dropMaxVal", f"{_drop.max():.1f}"); macro("dropMinVal", f"{_drop.min():.1f}")

# ---------------------------------------------------------------- Dakshina-bn: agreement with the Bengali-script answer, native-speaker romanization vs the two synthetic ones
da = pd.read_csv(T / "dak_agreement.csv"); dp = pd.read_csv(T / "dak_paired.csv")
DORDER = [m for m in ORDER if m in set(da.model)] + [m for m in ("d3-flash (4/8-bit)",) if m in set(da.model)]
def dlab(m):
    return NAME.get(m, NAME.get("d3-flash (4-bit)")) if m != "d3-flash (4/8-bit)" else NAME["d3-flash (4-bit)"]
drows, tvrows = [], []
for m in ORDER:
    mm = "d3-flash (4/8-bit)" if m == "d3-flash (4-bit)" else m
    g = da[da.model == mm].set_index("variant")
    if g.empty:
        continue
    pr = dp[(dp.model == mm) & (dp.metric == "agreement")].set_index("comparison")
    tr = dp[(dp.model == mm) & (dp.metric == "tv")].set_index("comparison")
    nn = int(g.n.iloc[0])
    drows.append(f"{NAME[m]} & {nn:,} & {f3(g.loc['dakshina','agreement'])} & {f3(g.loc['roman_nat','agreement'])} & {f3(g.loc['roman','agreement'])} & "
                 f"{pts(pr.loc['dakshina - roman','diff'])} {ci(pr.loc['dakshina - roman','lo'], pr.loc['dakshina - roman','hi'])} & {pts(pr.loc['dakshina - roman_nat','diff'])} {ci(pr.loc['dakshina - roman_nat','lo'], pr.loc['dakshina - roman_nat','hi'])} \\\\")
    tvrows.append(f"{NAME[m]} & {f3(g.loc['dakshina','tv'])} & {f3(g.loc['roman_nat','tv'])} & {f3(g.loc['roman','tv'])} & {f3(g.loc['dakshina','conf_variant'])} & {f3(g.loc['roman','conf_variant'])} & {f3(g.loc['dakshina','conf_native'])} \\\\")
    k = tag.get(m)
    if k:
        for v, vn in (("dakshina", "Ns"), ("roman_nat", "Nat"), ("roman", "Rule")):
            macro(f"dak{k}{vn}", f3(g.loc[v, "agreement"]))
        macro(f"dak{k}NsVsRule", pts(pr.loc["dakshina - roman", "diff"])); macro(f"dak{k}NsVsRuleLo", pts(pr.loc["dakshina - roman", "lo"])); macro(f"dak{k}NsVsRuleHi", pts(pr.loc["dakshina - roman", "hi"]))
        macro(f"dak{k}NsVsNat", pts(pr.loc["dakshina - roman_nat", "diff"])); macro(f"dak{k}NsVsNatLo", pts(pr.loc["dakshina - roman_nat", "lo"])); macro(f"dak{k}NsVsNatHi", pts(pr.loc["dakshina - roman_nat", "hi"]))
write("tab_dak.tex", "\\begin{tabular}{@{}lrccccc@{}}\\toprule\n & & \\multicolumn{3}{c}{Agreement with own Bengali answer} & \\multicolumn{2}{c}{Difference in points (95\\% CI)} \\\\\\cmidrule(lr){3-5}\\cmidrule(l){6-7}\n"
      "Model & Sentences & Native-speaker & Natural-style & Rule-based & Native-speaker $-$ rule-based & Native-speaker $-$ natural-style \\\\\\midrule\n" + "\n".join(drows) + "\n\\bottomrule\\end{tabular}\n")
write("tab_dak_tv.tex", "\\begin{tabular}{@{}lcccccc@{}}\\toprule\n & \\multicolumn{3}{c}{Probability shift (TV)} & \\multicolumn{3}{c}{Mean top-option confidence} \\\\\\cmidrule(lr){2-4}\\cmidrule(l){5-7}\n"
      "Model & Native-speaker & Natural-style & Rule-based & Native-speaker & Rule-based & Bengali \\\\\\midrule\n" + "\n".join(tvrows) + "\n\\bottomrule\\end{tabular}\n")
# summary counts over the systems with the full 1,500 sentences plus d3-flash on its subset
pivot = dp[dp.metric == "agreement"].pivot_table(index="model", columns="comparison", values=["diff", "lo", "hi"])
nsys = len(pivot)
pos_rule = int(((pivot[("lo", "dakshina - roman")] > 0)).sum()); pos_nat = int(((pivot[("lo", "dakshina - roman_nat")] > 0)).sum())
macro("dakSystems", nsys); macro("dakNsBeatsRule", pos_rule); macro("dakNsBeatsNat", pos_nat)
macro("dakRuleDiffMin", pts(pivot[("diff", "dakshina - roman")].min())); macro("dakRuleDiffMax", pts(pivot[("diff", "dakshina - roman")].max()))
full_models = da[da.n == da.n.max()].model.unique()
ag = da[da.model.isin(full_models)].pivot_table(index="model", columns="variant", values="agreement")
from scipy.stats import kendalltau
macro("dakTauRule", f"{kendalltau(ag.dakshina, ag.roman)[0]:.2f}"); macro("dakTauNat", f"{kendalltau(ag.dakshina, ag.roman_nat)[0]:.2f}"); macro("dakNTau", len(ag))
# natural-style (rebuilt lookup) against rule-based, paired, per system
nr = dp[(dp.metric == "agreement") & (dp.comparison == "roman_nat - roman")].set_index("model")
macro("dakNatBeatsRule", int((nr.lo > 0).sum())); macro("dakNatLosesRule", int((nr.hi < 0).sum())); macro("dakNatTied", int(((nr.lo <= 0) & (nr.hi >= 0)).sum()))
macro("dakNatDiffMin", pts(nr["diff"].min())); macro("dakNatDiffMax", pts(nr["diff"].max()))
macro("dakNsNatMin", pts(pivot[("diff", "dakshina - roman_nat")].min())); macro("dakNsNatMax", pts(pivot[("diff", "dakshina - roman_nat")].max()))
for m, k in tag.items():
    mm = "d3-flash (4/8-bit)" if m == "d3-flash (4-bit)" else m
    if mm in nr.index:
        macro(f"dak{k}NatVsRule", pts(nr.loc[mm, "diff"])); macro(f"dak{k}NatVsRuleLo", pts(nr.loc[mm, "lo"])); macro(f"dak{k}NatVsRuleHi", pts(nr.loc[mm, "hi"]))

macro("dakN", f"{int(da.n.max()):,}".replace(",", "{,}")); macro("dakChance", f3(da.chance.mean()))

# ---------------------------------------------------------------- natural-style lookup: corpus pairs removed because they are Dakshina sentences, and what the leak did before the fix
flt = json.load(open(T / "natural_lookup_filter.json")); macro("lookupRemoved", f"{flt['removed_pairs']:,}".replace(",", "{,}")); macro("lookupKept", f"{flt['kept_sentences']:,}".replace(",", "{,}"))
_old = pd.read_csv(T / "dak_agreement_natural_style_leaked.csv")
_o = _old[(_old.model == "jev-1.13.0") & (_old.variant == "roman_nat")].iloc[0]
macro("dakLeakJevNat", f3(_o.agreement))

# ---------------------------------------------------------------- paired differences to Jev: the closest full-set open system per task, and d3-flash on its subset
pj = pd.read_csv(T / "rq1_paired_vs_jev.csv"); pj = pj[pj.variant == "native"]
TK2 = {"Belebele": "Bel", "SIB-200": "Sib", "XNLI-bn": "Xnli", "MASSIVE": "Mas", "SentNoB": "Sent"}
nm = {**{k: v for k, v in NAME.items()}, "d3-flash (4/8-bit)": "d3-flash (4-bit)"}
prow = []
for t, tk in TK2.items():
    q = pj[(pj.task == t)]
    full = q[(~q.model.str.contains("flash")) & (q.n_common >= 0.9 * q.n_common.max())].sort_values("acc_diff", ascending=False).iloc[0]
    fl = q[q.model.str.contains("flash")]
    fl = fl.iloc[0] if len(fl) else None
    macro(f"pd{tk}", pts(full.acc_diff)); macro(f"pd{tk}Lo", pts(full.ci_lo)); macro(f"pd{tk}Hi", pts(full.ci_hi))
    cell_f = "--" if fl is None else f"{pts(fl.acc_diff)} {ci(fl.ci_lo, fl.ci_hi)} ({int(fl.n_common)})"
    if fl is not None:
        macro(f"pdFlash{tk}", pts(fl.acc_diff)); macro(f"pdFlash{tk}Lo", pts(fl.ci_lo)); macro(f"pdFlash{tk}Hi", pts(fl.ci_hi))
    prow.append(f"{t} & {NAME.get(full.model, full.model)} & {pts(full.acc_diff)} {ci(full.ci_lo, full.ci_hi)} & {cell_f} \\\\")
write("tab_vs_jev.tex", "\\begin{tabular}{@{}llcc@{}}\\toprule\nTask & Closest open system & System $-$ Jev, points (95\\% CI) & d3-flash $-$ Jev on its subset (items) \\\\\\midrule\n" + "\n".join(prow) + "\n\\bottomrule\\end{tabular}\n")

# ---------------------------------------------------------------- scope of the calibration evidence
cn = c[(c.variant == "native") & c.task.isin(["XNLI-bn", "MASSIVE", "SentNoB"]) & (~c.model.str.contains("flash"))]
gap = cn.groupby("model").signed_gap.mean()
macro("calFull", len(gap)); macro("calOverAvg", int((gap > 0).sum()))
under = cn[cn.signed_gap < 0]
macro("calUnderCells", len(under)); macro("calCells", len(cn))
names = sorted({NAME[m] for m in under.model if m in NAME})
macro("calUnderNames", ", ".join(names[:-1]) + (" and " if len(names) > 1 else "") + names[-1] if names else "none")
_t = ts[ts.test_variant == "native"]
macro("tsSystems", _t.model.nunique()); macro("tsCells", len(_t)); macro("tsLowered", int((_t.ece15_after < _t.ece15_before).sum()))

# ---------------------------------------------------------------- Bonferroni check, dataset provenance, model revisions
bf = pd.read_csv(T / "dak_bonferroni.csv")
_bf = bf[bf.comparison == "dakshina - roman"]
_fail = sorted({NAME.get(m, NAME.get("d3-flash (4-bit)")) if m != "d3-flash (4/8-bit)" else NAME["d3-flash (4-bit)"] for m in _bf[_bf.lo_bonf <= 0].model})
macro("dakBonfFail", ", ".join(_fail[:-1]) + (" and " if len(_fail) > 1 else "") + _fail[-1] if _fail else "none")
macro("dakBonfRule", int((bf[bf.comparison == "dakshina - roman"].lo_bonf > 0).sum())); macro("dakBonfNat", int((bf[bf.comparison == "dakshina - roman_nat"].lo_bonf > 0).sum()))
import hashlib
sh_ = json.load(open(ROOT / "data" / "split_hashes.json"))
dsha = hashlib.sha256((ROOT / "data" / "raw" / "dakshina_bn.jsonl").read_bytes()).hexdigest()
LIC = {"belebele": "CC BY-SA 4.0 (dataset card)", "sib200": "CC BY-SA 4.0 (dataset card)", "massive": "CC BY 4.0 (original release; the mirror's card gives none)",
       "bnli": "CC BY-NC-SA 4.0 (dataset card)", "sentnob": "none stated by the authors; not confirmed"}
SRC = {"belebele": "facebook/belebele, ben\\_Beng, test", "sib200": "Davlan/sib200, ben\\_Beng, test", "massive": "SetFit/\\allowbreak amazon\\_massive\\_intent\\_bn-BD, test (mirror of MASSIVE bn-BD)",
       "bnli": "csebuetnlp/xnli\\_bn, test", "sentnob": "sadi2oo3q/SentNoB, test (third-party mirror; 1,586 items, against 1,567 in BLUB and 1,564 in the laya-bangla card)"}
NM = {"belebele": "Belebele", "sib200": "SIB-200", "massive": "MASSIVE bn-BD", "bnli": "XNLI-bn", "sentnob": "SentNoB"}
prow = [f"{NM[k]} & {SRC[k]} & {sh_[k]['n']:,} & {sh_[k]['sha256'][:12]} & {LIC[k]} \\\\" for k in ("belebele", "sib200", "massive", "bnli", "sentnob")]
prow.append(f"Dakshina-bn & google-research-datasets/\\allowbreak dakshina, bn romanized, dev and test (filtered to 8,244) & 8,244 & {dsha[:12]} & CC BY-SA 4.0 (repository) \\\\")
write("tab_prov.tex", "\\begin{tabular}{@{}lp{4.6cm}rlp{3.4cm}@{}}\\toprule\nDataset & Source and split & Items & SHA-256 (first 12) & Licence \\\\\\midrule\n" + "\n".join(prow) + "\n\\bottomrule\\end{tabular}\n")
MOD = [("Jev", "jev-1.13.0 (TypeSafe API)", "hosted, accessed October 2026"), ("d3-edge", "vllm-sr/d3-edge", "18d61df786"), ("d3-lite", "vllm-sr/d3-lite", "a8d25a91ef"), ("d3-nano", "vllm-sr/d3-nano", "3aeb1c22a5"),
       ("d3-mini", "vllm-sr/d3-mini", "a475367de0"), ("d3-flash", "vllm-sr/d3-flash", "521525effa; 4-bit NF4"), ("Laya-multilingual", "convaiinnovations/laya-multilingual", "not pinned; package laya 0.4.3"),
       ("laya-bangla", "algolyzer/laya-bangla", "v2, 4c5eb48932; package laya 0.4.11"), ("Julia-1", "SupersonicLabs/Julia-1", "a85b127321"), ("Kev-0.8B, Kev-4B", "jaredpalmer/kev-0.8b, kev-4b", "tag v1.0; code 2ecafc49fe"),
       ("Gemma-4-E4B", "google/gemma-4-E4B-it", "not pinned")]
write("tab_models.tex", "\\begin{tabular}{@{}lll@{}}\\toprule\nSystem & Identifier & Revision or version \\\\\\midrule\n" + "\n".join(f"{a} & \\texttt{{{b.replace('_', chr(92)+'_')}}} & {c} \\\\" for a, b, c in MOD) + "\n\\bottomrule\\end{tabular}\n")

# ---------------------------------------------------------------- SentNoB: the mirror's test split overlaps its training split; macro-F1 on all items vs on the non-overlapping items (from the released predictions)
au = json.load(open(T / "sentnob_split_audit.json"))
for k_, v_ in au.items():
    macro("sn" + "".join(w.capitalize() for w in k_.split("_")), f"{v_:,}".replace(",", "{,}"))
fl = pd.read_csv(ROOT / "results" / "sentnob_overlap_flags.csv")
pr = pd.read_csv(ROOT / "results" / "predictions_test_sets.csv.gz", usecols=["model", "task", "split", "variant", "rot", "uid", "gold_id", "pred_id"])
sn = pr[(pr.task == "bn_sentnob") & (pr.split == "eval") & (pr.variant == "native") & (pr.rot == 0)].merge(fl, on="uid")
def macro_f1(g):
    f = []
    for c in sorted(g.gold_id.unique()):
        tp = ((g.gold_id == c) & (g.pred_id == c)).sum(); fp = ((g.gold_id != c) & (g.pred_id == c)).sum(); fn = ((g.gold_id == c) & (g.pred_id != c)).sum()
        f.append(0 if tp == 0 else 2 * tp / (2 * tp + fp + fn))
    return float(np.mean(f))
srows, full_f, sub_f = [], {}, {}
for m in ORDER:
    mm = "d3-flash (4/8-bit)" if m == "d3-flash (4-bit)" else m
    g = sn[sn.model == mm]
    if m == "d3-flash (4-bit)" or len(g) < 1000:
        continue
    full_f[m], sub_f[m] = macro_f1(g), macro_f1(g[g.overlap == 0])
    srows.append(f"{NAME[m]} & {f3(full_f[m])} & {f3(sub_f[m])} & {pts(sub_f[m] - full_f[m])} \\\\")
write("tab_sentnob_overlap.tex", "\\begin{tabular}{@{}lccc@{}}\\toprule\nSystem & All \\sntestN{} items & Items not in train, validation or repeated & Change (points) \\\\\\midrule\n".replace("\\sntestN{}", f"{len(fl):,}") + "\n".join(srows) + "\n\\bottomrule\\end{tabular}\n")
macro("snSubsetN", f"{int((fl.overlap == 0).sum()):,}".replace(",", "{,}")); macro("snFullN", f"{len(fl):,}".replace(",", "{,}"))
macro("snMaxShift", f"{100*max(abs(sub_f[m] - full_f[m]) for m in full_f):.1f}")
from scipy.stats import kendalltau as _kt
macro("snTau", f"{_kt([full_f[m] for m in full_f], [sub_f[m] for m in full_f])[0]:.2f}")
macro("snJevFull", f3(full_f["jev-1.13.0"])); macro("snJevSub", f3(sub_f["jev-1.13.0"]))
macro("snOverlapPct", f"{100*au['test_overlap_any']/au['mirror_test']:.0f}"); macro("snTrainPct", f"{100*au['test_in_train']/au['mirror_test']:.0f}")

# ---------------------------------------------------------------- Brier score: per-item sum over the options of (p - one-hot)^2, averaged over items; per task here, and a uniform-guess reference 1 - 1/K
KT = {"XNLI-bn": 3, "MASSIVE": 60, "SentNoB": 3}
for t_, k_ in KT.items():
    macro("brierUni" + {"XNLI-bn": "Xnli", "MASSIVE": "Mas", "SentNoB": "Sent"}[t_], f3(1 - 1 / k_))
macro("brierUniMean", f3(np.mean([1 - 1 / k for k in KT.values()]))); macro("brierUniMeanTwo", f3(np.mean([1 - 1 / 3, 1 - 1 / 3])))
brow = []
for m in ORDER:
    if m == "d3-flash (4-bit)":
        continue
    cs = c[(c.model == m)]
    cells = []
    for t_ in ("XNLI-bn", "MASSIVE", "SentNoB"):
        for var in ("native", "roman"):
            g = cs[(cs.task == t_) & (cs.variant == var)]
            cells.append(f3(g.brier.iloc[0]) if len(g) else "--")
    if all(x == "--" for x in cells):
        continue
    brow.append(f"{NAME[m]} & " + " & ".join(cells) + " \\\\")
_cb = c[c.task.isin(KT) & (~c.model.str.contains("flash")) & c.variant.isin(["native", "roman"])].copy()
_cb["uni"] = _cb.task.map(lambda t_: 1 - 1 / KT[t_]); _cb["worse"] = _cb.brier > _cb.uni
for var, nm in (("native", "Bn"), ("roman", "Rule")):
    q_ = _cb[_cb.variant == var]; macro(f"brierWorse{nm}", int(q_.worse.sum())); macro(f"brierCells{nm}", len(q_))
write("tab_brier_tasks.tex", "\\begin{tabular}{@{}lcccccc@{}}\\toprule\n & \\multicolumn{2}{c}{XNLI-bn} & \\multicolumn{2}{c}{MASSIVE} & \\multicolumn{2}{c}{SentNoB} \\\\\\cmidrule(lr){2-3}\\cmidrule(lr){4-5}\\cmidrule(l){6-7}\nModel & Bengali & Rule & Bengali & Rule & Bengali & Rule \\\\\\midrule\n" + "\n".join(brow) + "\n\\midrule\nUniform guess & \\multicolumn{2}{c}{" + f3(1 - 1 / 3) + "} & \\multicolumn{2}{c}{" + f3(1 - 1 / 60) + "} & \\multicolumn{2}{c}{" + f3(1 - 1 / 3) + "} \\\\\n\\bottomrule\\end{tabular}\n")

(ROOT / "paper" / "numbers.tex").write_text("% generated by analysis/make_tables.py; do not edit\n" + "\n".join(f"\\newcommand{{\\{k}}}{{{v}}}" for k, v in sorted(NUM.items())) + "\n")
print(f"{len(NUM)} macros; tables:", ", ".join(sorted(p.name for p in OUT.glob('*.tex'))))
