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

# ---------------------------------------------------------------- Table 3 + macros: hand-written Banglish
d = pd.read_csv(T / "human_items_all_models.csv"); d = d[d.answered == 1]
p = d.pivot_table(index=["model", "dataset", "id"], columns="variant", values="ok")
acc = p.groupby("model")[["native_edit", "roman_edit", "roman_nat_edit", "human"]].mean()
cnt = p.groupby("model").size()
r = pd.read_csv(T / "human_items_paired.csv")
allr = r[r.scope == "all tasks"].set_index(["model", "comparison"])
rows = []
for m in ORDER:
    if m not in acc.index:
        continue
    x = acc.loc[m]; h = allr.loc[(m, "human - native_edit")]; hr = allr.loc[(m, "human - roman_edit")]
    star = r"$^\ddagger$" if m == "julia-1" else ""
    rows.append(f"{NAME[m]}{star} & {f3(x.native_edit)} & {f3(x.roman_edit)} & {f3(x.roman_nat_edit)} & {f3(x.human)} & {pts(h['diff'])} {ci(h.lo, h.hi)} & {pts(hr['diff'])} {ci(hr.lo, hr.hi)} \\\\")
write("tab_human.tex", "\\begin{tabular}{@{}lcccccc@{}}\\toprule\n & \\multicolumn{4}{c}{Accuracy} & \\multicolumn{2}{c}{Change in points (95\\% CI)} \\\\\\cmidrule(lr){2-5}\\cmidrule(l){6-7}\n"
      "Model & Bengali & Rule-based & Natural-style & AI Banglish & AI Banglish $-$ Bengali & AI Banglish $-$ rule-based \\\\\\midrule\n" + "\n".join(rows) + "\n\\bottomrule\\end{tabular}\n")
tag = {"jev-1.13.0": "jev", "gemma-4-E4B-it": "gemma", "d3-flash (4-bit)": "flash", "d3-mini": "mini", "d3-nano": "nano", "d3-lite": "lite", "d3-edge": "edge", "laya-bangla v2": "layabn", "laya-multilingual": "layaml", "julia-1": "julia", "kev-4b": "kevmd", "kev-0.8b": "kevsm"}
for m, k in tag.items():
    if m in acc.index:
        x = acc.loc[m]
        macro(f"{k}Bengali", f3(x.native_edit)); macro(f"{k}Rule", f3(x.roman_edit)); macro(f"{k}Nat", f3(x.roman_nat_edit)); macro(f"{k}Human", f3(x.human))
        h = allr.loc[(m, "human - native_edit")]; hr = allr.loc[(m, "human - roman_edit")]; hn = allr.loc[(m, "human - roman_nat_edit")]; rr = allr.loc[(m, "roman_edit - native_edit")]
        macro(f"{k}LossHuman", pts(h["diff"], False).lstrip("-")); macro(f"{k}LossRule", pts(rr["diff"], False).lstrip("-"))
        macro(f"{k}HumanVsRule", pts(hr["diff"])); macro(f"{k}HumanVsRuleLo", pts(hr.lo)); macro(f"{k}HumanVsRuleHi", pts(hr.hi)); macro(f"{k}HumanVsNat", pts(hn["diff"]))
macro("nHuman", int(cnt.loc["jev-1.13.0"])); macro("julianHuman", int(cnt.loc["julia-1"]))
by_task = r[(r.model == "jev-1.13.0") & (r.comparison == "human - roman_edit")].set_index("scope")
for sc, k in (("massive", "Massive"), ("sentnob", "Sentnob"), ("bnli", "Nli")):
    macro(f"jevHumanVsRule{k}", pts(by_task.loc[sc, "diff"])); macro(f"jevHumanVsRule{k}Lo", pts(by_task.loc[sc, "lo"])); macro(f"jevHumanVsRule{k}Hi", pts(by_task.loc[sc, "hi"])); macro(f"nHuman{k}", int(by_task.loc[sc, "n"]))
ne = allr.loc[("jev-1.13.0", "native_edit - native")]
macro("spellEffect", pts(ne["diff"])); macro("spellLo", pts(ne.lo)); macro("spellHi", pts(ne.hi))
spell_max = r[(r.scope == "all tasks") & (r.comparison == "native_edit - native")]["diff"].abs().max()
macro("spellMaxAny", f"{100*spell_max:.1f}")
# rank agreement between the Banglish ordering and the synthetic orderings (eight models above chance: julia-1 excluded)
from scipy.stats import kendalltau
a8 = acc.drop(index="julia-1")
macro("tauRule", f"{kendalltau(a8.human, a8.roman_edit)[0]:.2f}"); macro("tauNat", f"{kendalltau(a8.human, a8.roman_nat_edit)[0]:.2f}"); macro("nModelsRank", len(a8))
edited = pd.read_csv(ROOT / "data" / "banglish_human.csv")
macro("nSentences", len(edited)); macro("nEdited", int((edited.raw_bengali.str.split().str.join(" ") != edited.bengali.str.split().str.join(" ")).sum()))

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
hv = [allr.loc[(m, "human - roman_edit"), "diff"] for m in acc.index if m != "julia-1"]
macro("hvrMin", f"{100*min(hv):.1f}"); macro("hvrMax", f"{100*max(hv):.1f}")
macro("pctMassive", f"{100*int(by_task.loc['massive', 'n'])/int(cnt.loc['jev-1.13.0']):.0f}")
mm = re.search(r"macro-F1 (0\.\d+) \(default English\), (0\.\d+) \(options only\), (0\.\d+) \(Bengali wording\)", audit)
macro("layamlSentDefault", mm.group(1)); macro("layamlSentOpts", mm.group(2)); macro("layamlSentBn", mm.group(3))
macro("jevBelebeleZenodo", re.search(r"recomputed from the authors' Zenodo responses (0\.\d+)", audit).group(1))
macro("lossRuleVsHuman", f"{float(NUM['jevLossRule'])-float(NUM['jevLossHuman']):.0f}")

# ---------------------------------------------------------------- confidence gate fitted on native dev text, applied to romanized text (MASSIVE)
gt = pd.read_csv(T / "rq2_gate_transfer.csv")
for m, k in (("jev-1.13.0", "jev"), ("d3-mini", "mini"), ("d3-lite", "lite"), ("laya-bangla v2", "layabn")):
    for v, vk in (("native", "Nat"), ("roman", "Rom")):
        g = gt[(gt.model == m) & (gt.task == "MASSIVE") & (gt.test_variant == v)].iloc[0]
        macro(f"gate{k}{vk}Cov", f"{100*g.coverage:.0f}"); macro(f"gate{k}{vk}Acc", f"{100*g.accepted_acc:.0f}")
macro("gateTarget", "90")
ll = pd.read_csv(T / "rq4_label_language.csv").iloc[:3]
macro("labelMaxDiff", f"{100*ll.diff_bn_minus_en.abs().max():.1f}")

# ---------------------------------------------------------------- sample flow: sentences -> scorable items (nothing is excluded; an XNLI-bn item is a premise-hypothesis pair)
hb = pd.read_csv(ROOT / "data" / "banglish_human.csv", encoding="utf-8-sig")
hb["edited"] = hb.raw_bengali.str.split().str.join(" ") != hb.bengali.str.split().str.join(" ")
frows = []
for ds, name, unit in (("massive", "MASSIVE", "utterance"), ("sentnob", "SentNoB", "comment"), ("bnli", "XNLI-bn", "premise--hypothesis pair")):
    g = hb[hb.dataset == ds]; n_items = len(g) // (2 if ds == "bnli" else 1)
    frows.append(f"{name} & {len(g)} & {int(g.edited.sum())} & {n_items} ({unit}) \\\\")
frows.append(f"Total & {len(hb)} & {int(hb.edited.sum())} & {int(NUM['nHuman'])} \\\\")
write("tab_flow.tex", "\\begin{tabular}{@{}lccl@{}}\\toprule\nDataset & Sentences romanized & of which spelling corrected & Scored items \\\\\\midrule\n" + "\n".join(frows[:-1]) + "\n\\midrule\n" + frows[-1] + "\n\\bottomrule\\end{tabular}\n")

# ---------------------------------------------------------------- per-task differences (the pooled set is 56% MASSIVE) and a task-balanced mean
def task_row(m, comp):
    out, vals = [], []
    for sc in ("massive", "sentnob", "bnli"):
        q = r[(r.model == m) & (r.scope == sc) & (r.comparison == comp)]
        if q.empty:
            out.append("--"); continue
        q = q.iloc[0]; vals.append(q["diff"]); out.append(f"{pts(q['diff'])} [{100*q.lo:+.1f}, {100*q.hi:+.1f}]")
    out.append(pts(float(np.mean(vals))) if len(vals) == 3 else "--")
    return out
trows = []
for m in ORDER:
    if m not in acc.index:
        continue
    trows.append(f"{NAME[m]} & " + " & ".join(task_row(m, "human - roman_edit")) + " & " + " & ".join(task_row(m, "human - native_edit")) + " \\\\")
write("tab_human_tasks.tex", "\\begin{tabular}{@{}lcccccccc@{}}\\toprule\n & \\multicolumn{4}{c}{AI Banglish $-$ rule-based} & \\multicolumn{4}{c}{AI Banglish $-$ Bengali} \\\\\\cmidrule(lr){2-5}\\cmidrule(l){6-9}\n"
      "Model & MASSIVE & SentNoB & XNLI-bn & task mean & MASSIVE & SentNoB & XNLI-bn & task mean \\\\\\midrule\n" + "\n".join(trows) + "\n\\bottomrule\\end{tabular}\n")
bal = [np.mean([r[(r.model == m) & (r.scope == sc) & (r.comparison == "human - roman_edit")]["diff"].iloc[0] for sc in ("massive", "sentnob", "bnli")]) for m in ORDER if m in acc.index and m != "julia-1"]
macro("sentGainMax", f"{100*max(r[(r.model == m) & (r.scope == 'sentnob') & (r.comparison == 'human - roman_edit')]['diff'].iloc[0] for m in ORDER if m in acc.index):.1f}")
macro("balMin", f"{100*min(bal):.1f}"); macro("balMax", f"{100*max(bal):.1f}")
macro("balJev", f"{100*np.mean([r[(r.model == 'jev-1.13.0') & (r.scope == sc) & (r.comparison == 'human - roman_edit')]['diff'].iloc[0] for sc in ('massive', 'sentnob', 'bnli')]):.1f}")

# ---------------------------------------------------------------- accepted-item counts behind the gate rows
for m, k in (("jev-1.13.0", "jev"), ("d3-mini", "mini"), ("laya-bangla v2", "layabn")):
    for v, vk in (("native", "Nat"), ("roman", "Rom")):
        g = gt[(gt.model == m) & (gt.task == "MASSIVE") & (gt.test_variant == v)].iloc[0]
        macro(f"gate{k}{vk}N", f"{int(g.n_accepted)}")

# ---------------------------------------------------------------- calibration on the 877 items in all three Latin-script/Bengali conditions (raw confidence: no temperature is fitted for these items)
def ece15(ok, conf, bins=15):
    ok, conf = np.asarray(ok, float), np.asarray(conf, float); idx = np.minimum((conf * bins).astype(int), bins - 1); e = 0.0
    for b in range(bins):
        m = idx == b
        if m.any():
            e += m.mean() * abs(ok[m].mean() - conf[m].mean())
    return e
crow = []
for m in ORDER:
    if m not in acc.index or m == "d3-flash (4-bit)":
        continue
    g = d[d.model == m]; vals = [ece15(g[g.variant == v].ok, g[g.variant == v].pmax) for v in ("native_edit", "roman_edit", "human")]
    crow.append(f"{NAME[m]} & " + " & ".join(f3(v) for v in vals) + " \\\\")
    if m in tag:
        for v, vn in zip(vals, ("Bn", "Rule", "Ai")):
            macro(f"eceItems{tag[m]}{vn}", f3(v))
write("tab_cal_items.tex", "\\begin{tabular}{@{}lccc@{}}\\toprule\nModel & Bengali & Rule-based & AI-generated Banglish \\\\\\midrule\n" + "\n".join(crow) + "\n\\bottomrule\\end{tabular}\n")

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

# ---------------------------------------------------------------- ranking agreement on the items EVERY system answered (Julia-1 cannot take MASSIVE, so this is the SentNoB and XNLI-bn items only)
wide = d.pivot_table(index=["dataset", "id"], columns=["model", "variant"], values="ok")
need = [(m, v) for m in acc.index for v in ("human", "roman_edit", "roman_nat_edit")]
common = wide.dropna(subset=need)
ca = pd.DataFrame({v: {m: common[(m, v)].mean() for m in acc.index} for v in ("human", "roman_edit", "roman_nat_edit")})
macro("nCommon", len(common)); macro("nSystemsCommon", len(ca))
macro("tauComRule", f"{kendalltau(ca.human, ca.roman_edit)[0]:.2f}"); macro("tauComNat", f"{kendalltau(ca.human, ca.roman_nat_edit)[0]:.2f}")

# ---------------------------------------------------------------- uncertainty on the rank agreement: resample ITEMS, recompute every model's accuracy, recompute tau (1,000 draws, seed 0)
def tau_ci(df_items, models, va, vb, draws=1000, seed=0):
    rng_t = np.random.default_rng(seed)
    A = np.stack([df_items[(m, va)].to_numpy(float) for m in models]); Bm = np.stack([df_items[(m, vb)].to_numpy(float) for m in models])
    pt = kendalltau(A.mean(1), Bm.mean(1))[0]; n = A.shape[1]; out = []
    for _ in range(draws):
        ix = rng_t.integers(0, n, n); out.append(kendalltau(A[:, ix].mean(1), Bm[:, ix].mean(1))[0])
    return pt, np.nanpercentile(out, 2.5), np.nanpercentile(out, 97.5)
m11 = [m for m in acc.index if m != "julia-1"]; m12 = list(acc.index)
full = wide.dropna(subset=[(m, v) for m in m11 for v in ("human", "roman_edit", "roman_nat_edit")])
for tag_, items_, ms_ in (("Full", full, m11), ("Com", common, m12)):
    for vb, nm in (("roman_edit", "Rule"), ("roman_nat_edit", "Nat")):
        pt, lo, hi = tau_ci(items_, ms_, "human", vb)
        macro(f"tau{tag_}{nm}", f"{pt:.2f}"); macro(f"tau{tag_}{nm}Lo", f"{lo:.2f}"); macro(f"tau{tag_}{nm}Hi", f"{hi:.2f}")
macro("nFull", len(full))

# ---------------------------------------------------------------- task-level ECE (the primary calibration measure) next to the pooled-item ECE of tab_cal_items
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

(ROOT / "paper" / "numbers.tex").write_text("% generated by analysis/make_tables.py; do not edit\n" + "\n".join(f"\\newcommand{{\\{k}}}{{{v}}}" for k, v in sorted(NUM.items())) + "\n")
print(f"{len(NUM)} macros; tables:", ", ".join(sorted(p.name for p in OUT.glob('*.tex'))))
