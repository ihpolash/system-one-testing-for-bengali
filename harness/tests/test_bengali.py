"""Rotation must reorder options without breaking gold labels."""

import pytest

from jev_benchmarking import bn_text
from jev_benchmarking.bn_roman import romanize
from jev_benchmarking.tasks.bengali import BnBelebele


@pytest.mark.parametrize("k", [3, 4, 7, 59])
def test_rotations_are_distinct_permutations(k):
    items = list(range(k))
    rots = [bn_text.rot_items(items, r) for r in range(3)]
    assert all(sorted(r) == items for r in rots)
    assert len({tuple(r) for r in rots}) == 3


@pytest.mark.parametrize("rot", [0, 1, 2])
def test_belebele_gold_follows_option_text(monkeypatch, rot):
    monkeypatch.setattr(bn_text, "ROT", rot)
    row = {"flores_passage": "p", "question": "q", "correct_answer_num": "3",
           "mc_answer1": "a", "mc_answer2": "b", "mc_answer3": "c", "mc_answer4": "d"}
    e = BnBelebele().build(row, "ben_Beng")
    assert e.questions["answer"]["criteria"][e.gold["answer"]] == "c"


def test_romanize_keeps_latin_and_digits():
    assert romanize("COVID-19 এর ২০২৪") == "COVID-19 er 2024"


def test_dakshina_spellings():
    """bn_dakshina: the four spellings of one sentence are different texts for the same item, and 'dakshina' returns the native-speaker romanization."""
    import json
    from pathlib import Path

    import pytest

    f = Path(__file__).resolve().parents[2] / "data" / "raw" / "dakshina_bn.jsonl"
    if not f.exists():
        pytest.skip("data/raw/dakshina_bn.jsonl not built (data/make_dakshina.py)")
    from jev_benchmarking import bn_text
    from jev_benchmarking.tasks import get_tasks

    rows = [json.loads(line) for line in open(f, encoding="utf-8")]
    by_text = {r["text"]: r["roman_human"] for r in rows}
    task = get_tasks(["bn_dakshina"])[0]
    seen = {}
    for v in ("native", "dakshina", "roman", "roman_nat"):
        bn_text.VARIANT = v
        e = task.examples("eval", limit=1)[0]
        seen[v] = e.state["text"]
    bn_text.VARIANT = "native"
    assert seen["dakshina"] == by_text[seen["native"]]
    assert len({seen["native"], seen["dakshina"], seen["roman"], seen["roman_nat"]}) == 4
