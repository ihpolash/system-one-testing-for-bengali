"""Model-assisted review of the 100-sample romanization check (analysis/romanization_handcheck.csv).

Reviewer: Claude (a language model; reads Bengali but is not a native speaker). This is NOT native-speaker verification and must be
reported as such. Mechanical patterns are tagged by regex on the Bengali source; loanword rows were identified by reading every sample.
Columns written: ok(y/n) = readable and meaning-preserving; natural(y/n) = no feature that differs from how people usually type Banglish.
"""
import csv, re, collections
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE / "romanization_handcheck.csv"

# Rows (0-based) containing English loanwords, foreign names or acronyms that were romanized *phonetically from the Bengali
# spelling* (e.g. "imeil", "trabhel", "oyarld oyaid oyeb") where real Banglish users usually write the original Latin spelling.
LOAN = {0, 2, 3, 5, 6, 9, 12, 13, 14, 15, 20, 21, 23, 24, 28, 30, 31, 35, 36, 38, 43, 44, 45, 46, 48, 50, 51, 53, 54, 58, 59, 61, 63, 67, 69,
        71, 72, 73, 74, 75, 76, 77, 79, 81, 82, 83, 84, 87, 89, 90, 91, 93, 95, 96, 99}
HAND = {40: "garbled: সংজ্ঞা -> 'songgga' (ng+gya cluster); a reader may not recover the word"}

WORD = re.compile(r"[ঀ-৿]+")
RULES = [  # tag, regex on a single Bengali word, explanation
    ("FINAL_CONJ", r"[ক-হ]্[ক-হ]$", "word-final conjunct loses its vowel (e.g. জন্য -> 'jony'; people type 'jonno')"),
    ("BA_FOLA", r"্ব", "ব-ফলা rendered as 'b' (স্বপ্ন -> 'sbopn', তত্ত্ব -> 'tattb'); people type 'sw'/'w' or double the consonant"),
    ("KSH", r"ক্ষ", "ক্ষ rendered 'kkh' (ক্ষেত্র -> 'kkhetr'); people type 'khet', 'kkh' varies"),
    ("GYA", r"জ্ঞ", "জ্ঞ rendered 'gg' (জ্ঞান -> 'ggan'); people type 'gyan'"),
    ("NASAL", r"ঁ", "chandrabindu (ঁ) dropped"),
    ("HOYA", r"^হওয়|^হওয়", "হওয়া rendered 'hooya'; people type 'howa'/'hoya'"),
]


def review(i, row):
    bn = row["bengali"]; tags = {}
    for w in WORD.findall(bn):
        for tag, rx, why in RULES:
            if re.search(rx, w):
                tags.setdefault(tag, why)
    if i in LOAN:
        tags["LOAN"] = "English loanword/name/acronym romanized phonetically from its Bengali spelling instead of its Latin original"
    if '"""' in bn:
        tags["SRC_NOISE"] = "escaped-quote artifact in the source passage (not a romanizer issue)"
    tags_for_natural = {k: v for k, v in tags.items() if k != "SRC_NOISE"}
    ok = "n" if i in HAND else "y"
    return ok, ("y" if not tags_for_natural else "n"), sorted(tags), HAND.get(i, "")


def main():
    rows = list(csv.DictReader(SRC.open(encoding="utf-8")))
    out = []
    for i, r in enumerate(rows):
        ok, nat, tags, note = review(i, r)
        r["ok(y/n)"], r["natural(y/n)"], r["issue"], r["note"] = ok, nat, ";".join(tags), note
        out.append(r)
    cols = ["dataset", "bengali", "romanized", "ok(y/n)", "natural(y/n)", "issue", "note"]
    with SRC.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, cols); w.writeheader(); w.writerows({c: r.get(c, "") for c in cols} for r in out)
    n = len(out)
    cnt = collections.Counter(t for r in out for t in r["issue"].split(";") if t)
    by_ds = collections.defaultdict(lambda: [0, 0, 0])
    for r in out:
        d = by_ds[r["dataset"]]; d[0] += 1; d[1] += r["ok(y/n)"] == "y"; d[2] += r["natural(y/n)"] == "y"
    lines = ["# Romanization review (model-assisted, not native-speaker verified)", "",
             f"Reviewer: Claude (language model). 100 samples, 20 per dataset. Readable and meaning-preserving: **{sum(r['ok(y/n)']=='y' for r in out)}/{n}**. "
             f"Free of any non-natural feature: **{sum(r['natural(y/n)']=='y' for r in out)}/{n}**.", "", "| tag | rows | meaning |", "|---|---|---|"]
    expl = {**{t: w for t, _, w in RULES}, "LOAN": "English loanword/name/acronym romanized from the Bengali spelling instead of the Latin original", "SRC_NOISE": "source artifact"}
    for t, c in cnt.most_common():
        lines.append(f"| {t} | {c} | {expl[t]} |")
    lines += ["", "| dataset | rows | readable | natural |", "|---|---|---|---|"] + [f"| {k} | {v[0]} | {v[1]} | {v[2]} |" for k, v in sorted(by_ds.items())]
    lines += ["", "Global properties of the rule-based romanizer (not row-specific): one deterministic spelling per word (no spelling variation, unlike real Banglish);",
              "no schwa deletion (e.g. 'pasona' for পাসনা); consonant-final inherent vowel always dropped; no English-origin word restoration."]
    (HERE / "romanization_review.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
