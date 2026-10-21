"""'Natural-style' synthetic romanization: rule-based fallback tuned on natural Banglish typing + a word-level lookup of the dominant typed spelling.

Evidence base: nahidstaq/bangla-transliteration-data (natural social-media Banglish aligned with Bengali). Rule changes versus bn_roman.py
were kept only if they raised agreement with typed spellings on held-out word types (analysis/natural_banglish_stats.py, tune_rules.py).
Still synthetic: a lookup of the *most frequent* spelling removes real spelling variation; domain is social media, not formal text.
"""
import json
import re
from pathlib import Path

from jev_benchmarking.bn_roman import _WORD, romanize as base_romanize

LOOKUP_PATH = Path(__file__).resolve().parents[2] / "analysis" / "natural_banglish_lookup.json"
_LOOKUP = None

DEFAULT_FLAGS = {"v_for_bh": True, "final_conj": True, "ksh": True, "gya": True, "howa": True, "ba_fola": True, "sh_to_s": False, "ch_not_chh": True, "ekti": True}


def _lookup():
    global _LOOKUP
    if _LOOKUP is None:
        _LOOKUP = json.loads(LOOKUP_PATH.read_text()) if LOOKUP_PATH.is_file() else {}
    return _LOOKUP


def rule_word(w: str, flags=None) -> str:
    f = {**DEFAULT_FLAGS, **(flags or {})}
    pre = w
    # pre-process the Bengali before the base romanizer so conjunct rules see the original characters
    if f["final_conj"]:  # word-final C + ্য  ->  doubled consonant + o  (জন্য jonno, সত্য sotto, সাহায্য sahajjo)
        m = re.search(r"([ক-হ])্য$", pre)
        if m:
            base = base_romanize(pre[:m.start()])
            c = base_romanize(m.group(1))
            c = c[:-1] if c.endswith("o") else c
            out = base + (c[0] + c if c else "") + "o"
            return _post(out, f)
    if f["ba_fola"]:
        pre = re.sub(r"^(.)্ব", r"\1", pre)  # word-initial C + ্ব: drop the ব (স্বপ্ন -> sopno)
    out = base_romanize(pre)
    return _post(out, f)


def _post(out: str, f) -> str:
    if f["v_for_bh"]:
        out = out.replace("bh", "v")
    if f["ksh"]:
        out = re.sub(r"^kkh", "kh", out)
    if f["gya"]:
        out = re.sub(r"^gg", "gy", out)
    if f["howa"]:
        out = re.sub(r"^hooy", "how", out)
    if f["ekti"]:
        out = re.sub(r"^ekot([ia])$", r"ekt\1", out)
    if f["sh_to_s"]:
        out = out.replace("sh", "s")
    if f["ch_not_chh"]:
        out = out.replace("chh", "ch")
    return out


def romanize_nat(text: str, flags=None, use_lookup: bool = True) -> str:
    """Bengali-script runs -> natural-style Banglish; Latin letters, digits and punctuation untouched."""
    look = _lookup() if use_lookup else {}
    text = text.replace("।", ".")
    return _WORD.sub(lambda m: look.get(m.group(0)) or rule_word(m.group(0), flags), text)
