"""Script variants for Bengali text. `native` is identity; `roman` is a synthetic Banglish romanization."""

import os

VARIANT = os.environ.get("BN_VARIANT", "native")  # native | roman | roman_nat


def transform(text: str, variant: str | None = None) -> str:
    variant = variant or VARIANT
    if variant == "native":
        return text
    if variant == "roman":
        from jev_benchmarking.bn_roman import romanize

        return romanize(text)
    if variant == "roman_nat":  # natural-style: dominant typed spelling per word + rules tuned on natural Banglish
        from jev_benchmarking.bn_roman2 import romanize_nat

        return romanize_nat(text)
    if variant in ("native_edit", "roman_edit", "roman_nat_edit", "human"):
        # The author corrected spellings in the Bengali text before writing Banglish. Items are matched by the ORIGINAL dataset text;
        # *_edit variants use the corrected Bengali (alone, or romanized by our rule-based / natural-style romanizers); "human" is the author's Banglish.
        entry = _human_map().get(_norm_key(text))
        if entry is None:
            raise KeyError(f"no human entry for: {text[:40]!r}")
        edited, banglish = entry
        if variant == "human":
            return banglish
        if variant == "native_edit":
            return edited
        if variant == "roman_edit":
            from jev_benchmarking.bn_roman import romanize

            return romanize(edited)
        from jev_benchmarking.bn_roman2 import romanize_nat

        return romanize_nat(edited)
    raise ValueError(f"unknown BN_VARIANT {variant!r}")


ROT = int(os.environ.get("BN_ROT", "0"))  # option rotation 0|1|2 (cyclic shift of r*K//3 positions)


def rot_items(items: list, rot: int | None = None) -> list:
    """Cyclically rotate an option list. r in {0,1,2} shifts by r*K//3, so even a 59-way choice moves a lot."""
    r = ROT if rot is None else rot
    k = len(items)
    s = (r * k) // 3 % k if k else 0
    return items[s:] + items[:s]


_HUMAN = None


def _norm_key(text: str) -> str:
    return " ".join(text.split())


def _human_map() -> dict:
    global _HUMAN
    if _HUMAN is None:
        import csv

        path = os.environ.get("BN_HUMAN_CSV", "")
        _HUMAN = {_norm_key(r["raw_bengali"]): (r["bengali"].strip(), r["banglish"].strip()) for r in csv.DictReader(open(path, encoding="utf-8-sig"))} if path else {}
    return _HUMAN
