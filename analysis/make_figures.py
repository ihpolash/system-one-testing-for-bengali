"""Paper figures (static PDF + PNG) from analysis/tables/*.csv and analysis/items.csv.   python analysis/make_figures.py

Design rules (dataviz method): colour encodes the CONDITION, never the model (models are named on the axis); three categorical colours that validate
for all pairs (blue #2a78d6, orange #eb6834, aqua #1baf7a on white; aqua is below 3:1 so every figure also uses marker shape, a legend and direct labels,
and the paper carries the numbers in tables); thin marks, recessive grid, one axis, no dual axes; sorted by the message.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D

HERE = Path(__file__).parent
OUT = HERE.parent / "paper" / "figures"
OUT.mkdir(parents=True, exist_ok=True)
INK, INK2, GRID, SURFACE = "#0b0b0b", "#52514e", "#e4e3df", "#ffffff"
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
plt.rcParams.update({"font.size": 8, "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2, "ytick.color": INK2, "text.color": INK,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": 0.6, "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
                     "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.5, "axes.axisbelow": True, "legend.frameon": False, "pdf.fonttype": 42})
NAME = {"jev-1.13.0": "Jev", "gemma-4-E4B-it": "Gemma-4-E4B", "d3-flash (4-bit)": "d3-flash (4-bit)", "d3-mini": "d3-mini", "d3-nano": "d3-nano", "d3-lite": "d3-lite",
        "d3-edge": "d3-edge", "laya-multilingual": "Laya-multilingual", "laya-bangla v2": "laya-bangla", "julia-1": "Julia-1", "kev-4b": "Kev-4B", "kev-0.8b": "Kev-0.8B"}


def save(fig, name):
    fig.savefig(OUT / f"{name}.pdf", bbox_inches="tight"); fig.savefig(OUT / f"{name}.png", dpi=200, bbox_inches="tight"); plt.close(fig)
    print("wrote", name)


# ------------------------------------------------------------------ Fig D: agreement with the Bengali-script answer, by spelling of the same Dakshina sentences
def fig_dakshina():
    a = pd.read_csv(HERE / "tables" / "dak_agreement.csv"); a = a[~a.model.str.contains("flash")]
    w = a.pivot_table(index="model", columns="variant", values="agreement").sort_values("dakshina")
    lo = a.pivot_table(index="model", columns="variant", values="ci_lo").reindex(w.index); hi = a.pivot_table(index="model", columns="variant", values="ci_hi").reindex(w.index)
    fig, ax = plt.subplots(figsize=(6.6, 3.5)); y = np.arange(len(w))
    for i, (m, r) in enumerate(w.iterrows()):
        ax.plot([r.roman, r.dakshina], [i, i], color=GRID, lw=1.2, zorder=1)
    for col, c, mk, lab, face in (("roman", ORANGE, "s", "Rule-based romanization (synthetic)", ORANGE), ("roman_nat", ORANGE, "D", "Natural-style romanization (synthetic)", "white"), ("dakshina", AQUA, "^", "Native-speaker romanization (Dakshina)", AQUA)):
        ax.scatter(w[col], y, s=30, marker=mk, facecolor=face, edgecolor=c, linewidth=1.2, zorder=4, label=lab)
    ax.axvline(a.chance.mean(), color=INK2, lw=0.6, ls=(0, (3, 3)), zorder=1); ax.text(a.chance.mean() + 0.005, len(w) - 0.55, "chance", fontsize=6.5, color=INK2)
    ax.set_yticks(y, [NAME[m] for m in w.index]); ax.set_xlim(0.1, 0.8); ax.grid(axis="y", visible=False)
    ax.legend(loc="lower right", fontsize=6.8, labelcolor=INK2)
    ax.set_xlabel("Share of 1,500 sentences whose topic answer matches the system's own answer on the Bengali-script sentence")
    save(fig, "fig1_dakshina")


def fig_script_gap():
    a = pd.read_csv(HERE / "tables" / "rq1_accuracy.csv"); a = a[a.variant.isin(["native", "roman"]) & ~a.model.str.startswith("d3-flash")]
    order = ["jev-1.13.0", "gemma-4-E4B-it", "d3-mini", "d3-nano", "kev-4b", "d3-lite", "laya-bangla v2", "d3-edge", "kev-0.8b", "laya-multilingual", "julia-1"]
    tasks = [("XNLI-bn", "XNLI-bn (accuracy)"), ("SIB-200", "SIB-200 (accuracy)"), ("MASSIVE", "MASSIVE (accuracy)"), ("SentNoB", "SentNoB (macro-F1)")]
    fig, axes = plt.subplots(1, 4, figsize=(6.8, 3.0), sharey=True)
    for ax, (t, title) in zip(axes, tasks):
        s = a[a.task == t].pivot_table(index="model", columns="variant", values="value")
        for i, m in enumerate(order[::-1]):
            if m in s.index and not np.isnan(s.loc[m].get("roman", np.nan)):
                n, r = s.loc[m, "native"], s.loc[m, "roman"]
                ax.plot([r, n], [i, i], color=GRID, lw=1.2, zorder=1); ax.scatter(n, i, s=20, color=BLUE, marker="o", zorder=3); ax.scatter(r, i, s=20, color=ORANGE, marker="s", zorder=3)
        ax.set_title(title, fontsize=7.5); ax.set_xlim(0, 1); ax.grid(axis="y", visible=False)
    axes[0].set_yticks(range(len(order)), [NAME[m] for m in order[::-1]])
    handles = [Line2D([], [], marker="o", color=BLUE, ls="", ms=5, label="Bengali script"), Line2D([], [], marker="s", color=ORANGE, ls="", ms=5, label="Rule-based romanization")]
    fig.legend(handles=handles, loc="lower center", ncol=2, bbox_to_anchor=(0.5, -0.06), fontsize=7.5, labelcolor=INK2)
    save(fig, "fig2_script_gap")


# ------------------------------------------------------------------ helpers for Fig 3-4: pooled items on identical requests across the plotted models
def pooled_items(models):
    it = pd.read_csv(HERE / "items.csv", usecols=["model", "task", "split", "variant", "rot", "uid", "pmax", "correct"])
    it = it[(it.split == "eval") & (it.rot == 0) & it.variant.isin(["native", "roman"]) & it.model.isin(models) & (it.task != "bn_belebele")]
    key = it.pivot_table(index=["task", "variant", "uid"], columns="model", values="correct").dropna().index   # identical items for all plotted models
    return it.set_index(["task", "variant", "uid"]).loc[key].reset_index()


def fig_calibration_and_gating():
    models = ["jev-1.13.0", "gemma-4-E4B-it", "d3-mini", "laya-bangla v2"]
    it = pooled_items(models)
    fig, axes = plt.subplots(1, 4, figsize=(6.8, 1.9), sharey=True)
    for ax, m in zip(axes, models):
        ax.plot([0, 1], [0, 1], color=INK2, lw=0.6, ls=(0, (3, 3)), zorder=1)
        for v, c, mk in (("native", BLUE, "o"), ("roman", ORANGE, "s")):
            s = it[(it.model == m) & (it.variant == v)]
            b = np.minimum((s.pmax * 10).astype(int), 9); g = s.groupby(b).agg(conf=("pmax", "mean"), acc=("correct", "mean"), n=("correct", "size")); g = g[g.n >= 30]
            ax.plot(g.conf, g.acc, color=c, lw=1.0, marker=mk, ms=3.2, zorder=3)
        ax.set_title(NAME[m], fontsize=7.5); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_xlabel("Top-option probability", fontsize=7)
    axes[0].set_ylabel("Observed accuracy", fontsize=7)
    handles = [Line2D([], [], marker="o", color=BLUE, ms=4, lw=1, label="Bengali script"), Line2D([], [], marker="s", color=ORANGE, ms=4, lw=1, label="Rule-based romanization")]
    fig.legend(handles=handles, loc="upper center", ncol=2, bbox_to_anchor=(0.5, 1.16), fontsize=7.5, labelcolor=INK2)
    save(fig, "fig3_reliability")

    fig, axes = plt.subplots(1, 4, figsize=(6.8, 1.9), sharey=True); cov = np.linspace(0.05, 1, 40)
    for ax, m in zip(axes, models):
        for v, c, mk in (("native", BLUE, "o"), ("roman", ORANGE, "s")):
            s = it[(it.model == m) & (it.variant == v)].sort_values("pmax", ascending=False)
            ok = s.correct.to_numpy(float); cum = np.cumsum(ok) / np.arange(1, len(ok) + 1)
            ax.plot(cov, [cum[max(0, int(round(c_ * len(ok))) - 1)] for c_ in cov], color=c, lw=1.0)
        ax.set_title(NAME[m], fontsize=7.5); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_xlabel("Coverage", fontsize=7)
    axes[0].set_ylabel("Accuracy on covered items", fontsize=7)
    fig.legend(handles=handles, loc="upper center", ncol=2, bbox_to_anchor=(0.5, 1.16), fontsize=7.5, labelcolor=INK2)
    save(fig, "fig4_risk_coverage")


# ------------------------------------------------------------------ Fig 6: how often the answer survives rotating the options
def fig_rotation():
    r = pd.read_csv(HERE / "tables" / "rq4_rotation.csv"); r = r[r.model != "d3-flash (4/8-bit)"]
    g = r.groupby("model").apply(lambda x: np.average(x.same_answer_all_rotations, weights=x.n), include_groups=False).sort_values()
    fig, ax = plt.subplots(figsize=(4.4, 2.6)); y = np.arange(len(g))
    ax.barh(y, g.values, color=BLUE, height=0.55, zorder=3)
    for i, v in enumerate(g.values):
        ax.text(v + 0.012, i, f"{v:.0%}", va="center", fontsize=7, color=INK2)
    ax.set_yticks(y, [NAME[m] for m in g.index]); ax.set_xlim(0, 1.08); ax.grid(axis="y", visible=False)
    ax.set_xlabel("Share of items answered identically under all three option rotations")
    save(fig, "fig5_rotation")


if __name__ == "__main__":
    fig_dakshina(); fig_script_gap(); fig_calibration_and_gating(); fig_rotation()
