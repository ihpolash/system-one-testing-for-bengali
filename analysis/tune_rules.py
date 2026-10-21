"""Held-out evaluation of rule-fallback variants against natural typing (word types unseen in the lookup training split)."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "harness"))
from jev_benchmarking.bn_roman import romanize as base
from jev_benchmarking.bn_roman2 import rule_word, DEFAULT_FLAGS

unseen = json.load(open(Path(__file__).parent / "_unseen.json"))
tot = sum(sum(c.values()) for c in unseen.values())

def score(fn):
    hit = sum(sum(n for r, n in c.items() if r == fn(w)) for w, c in unseen.items())
    return hit / tot

none = {k: False for k in DEFAULT_FLAGS}
print(f"unseen tokens: {tot}")
print(f"{'variant':34} match-rate")
print(f"{'base rules (bn_roman.py)':34} {score(base):.3%}")
print(f"{'all flags off':34} {score(lambda w: rule_word(w, none)):.3%}")
for k in DEFAULT_FLAGS:
    print(f"{'only '+k:34} {score(lambda w, k=k: rule_word(w, {**none, k: True})):.3%}")
kept = {k: True for k in DEFAULT_FLAGS if k not in ("sh_to_s", "ch_not_chh")}
print(f"{'default (proposed) flags':34} {score(lambda w: rule_word(w, kept)):.3%}")
for k in ("sh_to_s", "ch_not_chh"):
    print(f"{'default + '+k:34} {score(lambda w, k=k: rule_word(w, {**kept, k: True})):.3%}")
print(f"{'all flags on':34} {score(lambda w: rule_word(w, {k: True for k in DEFAULT_FLAGS})):.3%}")

# ---- character error rate to the closest / most frequent typed form (more informative than exact match)
def lev(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]

def cer(fn, mode):
    num = den = 0
    for w, c in unseen.items():
        out = fn(w); n = sum(c.values())
        if mode == "closest":
            d = min(lev(out, r) / max(len(r), 1) for r in c)
        else:
            top = max(c, key=c.get); d = lev(out, top) / max(len(top), 1)
        num += d * n; den += n
    return num / den

print("\nmean char error rate vs typed spelling (lower is better)")
print(f"{'variant':34} {'closest form':>13} {'most frequent':>14}")
cands = {"base rules": base, "all flags off": lambda w: rule_word(w, none), "default flags": lambda w: rule_word(w, kept),
         "default + ch_not_chh": lambda w: rule_word(w, {**kept, "ch_not_chh": True}), "default + sh_to_s": lambda w: rule_word(w, {**kept, "sh_to_s": True}),
         "default + both": lambda w: rule_word(w, {**kept, "ch_not_chh": True, "sh_to_s": True})}
for name, fn in cands.items():
    print(f"{name:34} {cer(fn,'closest'):13.3f} {cer(fn,'top'):14.3f}")
