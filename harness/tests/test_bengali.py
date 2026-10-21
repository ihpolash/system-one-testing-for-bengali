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
