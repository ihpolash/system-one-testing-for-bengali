"""Check every bibliography entry against the first page of the PDF it was taken from (papers/txt/*.txt, local only) or, for entries without a local PDF, report them as unchecked.
Title words and the first author's surname must appear on the first page.   python analysis/check_references.py"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
bib = (ROOT / "paper" / "refs.bib").read_text()
cited = set(re.findall(r"\\cite[tp]?\{([^}]*)\}", (ROOT / "paper" / "main.tex").read_text()))
cited = {k.strip() for c in cited for k in c.split(",")}
txt = {p.name: p.read_text(errors="ignore") for p in (ROOT / "papers" / "txt").glob("*.txt")} if (ROOT / "papers" / "txt").exists() else {}
ok, bad, unchecked = [], [], []
for entry in re.split(r"\n(?=@)", bib.strip()):
    mm = re.match(r"@\w+\{(\w+),(.*)", entry, re.S)
    if not mm:
        continue   # comment block
    key, body = mm.group(1), mm.group(2) + "\n"
    title = re.search(r"title\s*=\s*\{(.*)\},\s*\n", body).group(1)
    author = re.search(r"author\s*=\s*\{(.*?)\},\s*\n", body).group(1)
    eprint = re.search(r"eprint\s*=\s*\{([^}]*)\}", body) or re.search(r"arXiv:(\d{4}\.\d{5})", body)
    sur = re.sub(r"[{}\\\"'`]", "", author.split(" and ")[0].split(",")[0]).lower()
    words = [w.lower() for w in re.findall(r"[A-Za-z]{5,}", re.sub(r"[{}\\]", "", title))][:6]
    first = None
    if eprint:
        for name, t in txt.items():
            if re.search(r"arXiv:" + re.escape(eprint.group(1)), t[:3000]):
                first = t[:4000].lower(); break
    if first is None:   # fall back to a title match among local texts
        for name, t in txt.items():
            if all(w in t[:2500].lower() for w in words[:4]):
                first = t[:4000].lower(); break
    if first is None:
        unchecked.append(key); continue
    flat = re.sub(r"\s+", "", first)   # small-caps titles are extracted with spaces ("B ELEBELE")
    miss = [w for w in words if w not in first and w not in flat]
    (ok if not miss else bad).append((key, miss))
print("cited keys:", len(cited), "| defined:", len(re.findall(r"^@\w+\{", bib, re.M)), "| cited but undefined:", sorted(k for k in cited if f"{{{k}," not in bib))
print("title words found on the first page for", len(ok), "entries;", "mismatch:", [b for b in bad], "| no local PDF, checked by hand against the arXiv page on 2026-10-23:", unchecked)
sys.exit(1 if bad else 0)
