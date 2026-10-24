"""Script variants for Bengali text. `native` is identity; `roman` is a synthetic Banglish romanization."""

import os

VARIANT = os.environ.get("BN_VARIANT", "native")  # native | roman | roman_nat | dakshina


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
    if variant == "dakshina":  # the romanization native speakers wrote for this exact sentence (Dakshina, CC BY-SA 4.0); only defined for the bn_dakshina sentences
        entry = _dakshina().get(" ".join(text.split()))
        if entry is None:
            raise KeyError(f"no Dakshina romanization for: {text[:40]!r}")
        return entry
    raise ValueError(f"unknown BN_VARIANT {variant!r}")


_DAK = None


def _dakshina() -> dict:
    global _DAK
    if _DAK is None:
        import json
        from pathlib import Path

        f = Path(__file__).resolve().parents[2] / "data" / "raw" / "dakshina_bn.jsonl"
        _DAK = {r["text"]: r["roman_human"] for r in map(json.loads, open(f, encoding="utf-8"))}
    return _DAK


ROT = int(os.environ.get("BN_ROT", "0"))  # option rotation 0|1|2 (cyclic shift of r*K//3 positions)


def rot_items(items: list, rot: int | None = None) -> list:
    """Cyclically rotate an option list. r in {0,1,2} shifts by r*K//3, so even a 59-way choice moves a lot."""
    r = ROT if rot is None else rot
    k = len(items)
    s = (r * k) // 3 % k if k else 0
    return items[s:] + items[:s]
