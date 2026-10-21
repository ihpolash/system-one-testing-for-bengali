"""Rule-based synthetic romanization of Bengali into casual 'Banglish' (no diacritics).

Deliberately lossy, like real typing: থ/ঠ -> th, ত/ট -> t, শ/ষ -> sh, inherent vowel 'o' kept inside a word but
dropped word-finally. Known weaknesses (reported in the paper): no medial schwa deletion, conjunct
pronunciation is approximated (e.g. য-ফলা is spelled out), no loan-word spelling conventions.
"""

import re

CONS = {
    "ক": "k", "খ": "kh", "গ": "g", "ঘ": "gh", "ঙ": "ng",
    "চ": "ch", "ছ": "chh", "জ": "j", "ঝ": "jh", "ঞ": "n",
    "ট": "t", "ঠ": "th", "ড": "d", "ঢ": "dh", "ণ": "n",
    "ত": "t", "থ": "th", "দ": "d", "ধ": "dh", "ন": "n",
    "প": "p", "ফ": "f", "ব": "b", "ভ": "bh", "ম": "m",
    "য": "j", "র": "r", "ল": "l", "শ": "sh", "ষ": "sh", "স": "s", "হ": "h",
    "\u09dc": "r", "\u09dd": "rh", "\u09df": "y", "ৎ": "t",  # ড়  ঢ়  য়
}
INDEP = {"অ": "o", "আ": "a", "ই": "i", "ঈ": "i", "উ": "u", "ঊ": "u", "ঋ": "ri", "এ": "e", "ঐ": "oi", "ও": "o", "ঔ": "ou"}
SIGNS = {"া": "a", "ি": "i", "ী": "i", "ু": "u", "ূ": "u", "ৃ": "ri", "ে": "e", "ৈ": "oi", "ো": "o", "ৌ": "ou"}
OTHER = {"ং": "ng", "ঁ": "", "ঃ": "", "।": ".", "॥": ".", "়": "", "‌": "", "‍": ""}
DIGITS = str.maketrans("০১২৩৪৫৬৭৮৯", "0123456789")
HASANTA = "্"

_WORD = re.compile(r"[ঀ-৿]+")


def _normalise(s: str) -> str:
    """Compose nukta letters (ড়, ঢ়, য়) and split-form o/ou vowel signs."""
    for a, b in (("ড়", "ড়"), ("ঢ়", "ঢ়"), ("য়", "য়"),
                 ("ো", "ো"), ("ৌ", "ৌ")):
        s = s.replace(a, b)
    return s


def _word(w: str) -> str:
    w = _normalise(w)
    out, i, n = [], 0, len(w)
    while i < n:
        c = w[i]
        if c == "ক" and w[i + 1:i + 3] == HASANTA + "ষ":  # ক্ষ
            out.append("kkh")
            i += 3
            nxt = w[i] if i < n else ""
            if nxt not in SIGNS and nxt != HASANTA and i < n:
                out.append("o")
            elif i >= n:
                pass
            continue
        if c == "জ" and w[i + 1:i + 3] == HASANTA + "ঞ":  # জ্ঞ
            out.append("gg")
            i += 3
            if i < n and w[i] not in SIGNS and w[i] != HASANTA:
                out.append("o")
            continue
        if c in CONS:
            out.append("y" if c == "\u09af" and i > 0 and w[i - 1] == HASANTA else CONS[c])  # য-ফলা -> y
            nxt = w[i + 1] if i + 1 < n else ""
            if nxt == HASANTA:
                i += 2  # conjunct / explicit halant: no vowel
                continue
            if nxt in SIGNS:
                pass  # vowel sign supplies the vowel
            elif i + 1 < n and nxt not in OTHER:
                out.append("o")  # inherent vowel inside the word
            elif nxt in ("ং", "ঁ", "ঃ"):
                out.append("o")
            # word-final inherent vowel is dropped
            i += 1
            continue
        if c in INDEP:
            out.append(INDEP[c])
        elif c in SIGNS:
            out.append(SIGNS[c])
        elif c in OTHER:
            out.append(OTHER[c])
        elif c == HASANTA:
            pass
        else:
            out.append(c.translate(DIGITS))
        i += 1
    return "".join(out)


def romanize(text: str) -> str:
    """Romanize Bengali-script runs; leave Latin letters, digits and punctuation untouched."""
    return _WORD.sub(lambda m: _word(m.group(0)), text.translate(DIGITS)).replace("।", ".")
