"""Build data/raw/dakshina_bn.jsonl from the Dakshina dataset (Roark et al. 2020, CC BY-SA 4.0):
10,000 Bengali Wikipedia sentences that native speakers romanized by hand (no transliteration tool), shipped as parallel native/Latin lines.
    python data/make_dakshina.py            (expects data/dakshina/dakshina_dataset_v1.0/bn/romanized/*, see README)
Keeps sentences of 6-40 words whose romanization contains no Bengali script, drops duplicates, and records the original dev/test side."""
import hashlib, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "dakshina" / "dakshina_dataset_v1.0" / "bn" / "romanized"
OUT = ROOT / "raw" / "dakshina_bn.jsonl"
BN = re.compile(r"[ঀ-৿]")
rows, seen = [], set()
for side in ("dev", "test"):
    native = (SRC / f"bn.romanized.rejoined.{side}.native.txt").read_text(encoding="utf-8").splitlines()
    roman = (SRC / f"bn.romanized.rejoined.{side}.roman.txt").read_text(encoding="utf-8").splitlines()
    assert len(native) == len(roman), (side, len(native), len(roman))
    for n, r in zip(native, roman):
        n, r = " ".join(n.split()), " ".join(r.split())
        if not (6 <= len(n.split()) <= 40) or not r or BN.search(r) or n in seen:
            continue
        seen.add(n)
        rows.append({"id": hashlib.sha256(n.encode()).hexdigest()[:12], "text": n, "roman_human": r, "category": "science/technology", "dakshina_side": side})
OUT.parent.mkdir(exist_ok=True)
OUT.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in rows), encoding="utf-8")
print(f"wrote {len(rows)} sentences to {OUT.relative_to(ROOT.parent)}; sha256 {hashlib.sha256(OUT.read_bytes()).hexdigest()}")
