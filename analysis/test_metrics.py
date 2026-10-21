"""Sanity tests for the metrics used in the paper (run: pytest analysis/test_metrics.py)."""
import numpy as np
import pytest

from metrics import Clusters, aurc, acc_at_coverage, ece_fixed, ece_mass, fit_temperature, macro_f1_from_counts, row_stats


def test_perfectly_calibrated_has_zero_ece():
    conf = np.array([0.9] * 10 + [0.5] * 10)
    ok = np.array([1] * 9 + [0] + [1] * 5 + [0] * 5, float)
    assert ece_fixed(conf, ok) == pytest.approx(0.0, abs=1e-9)
    assert ece_mass(conf, ok, n=2) == pytest.approx(0.0, abs=1e-9)  # 2 equal-mass bins separate the two levels


def test_overconfident_ece_equals_gap():
    conf = np.full(100, 0.95); ok = np.r_[np.ones(60), np.zeros(40)]
    assert ece_fixed(conf, ok) == pytest.approx(0.35)


def test_aurc_perfect_ranking_beats_reversed():
    conf = np.linspace(0.5, 1, 50); ok = (conf > 0.8).astype(float)
    assert aurc(conf, ok) < aurc(-conf, ok)
    assert acc_at_coverage(conf, ok, 0.3) == 1.0


def test_macro_f1_ignores_absent_classes():
    tp = np.array([5, 0, 0]); fp = np.array([0, 0, 0]); fn = np.array([5, 0, 0])
    assert macro_f1_from_counts(tp, fp, fn) == pytest.approx(2 * 5 / (2 * 5 + 5))


def test_clusters_resample_whole_groups():
    cl = Clusters(np.array(["a", "a", "b", "c", "c", "c"]))
    assert cl.k == 3
    rows = cl.rows(np.array([0, 0, 2]))  # cluster a twice, c once
    assert sorted(rows) == [0, 0, 1, 1, 3, 4, 5]


def test_temperature_recovers_overconfidence():
    rng = np.random.default_rng(0)
    p = [{"a": 0.99, "b": 0.01} if rng.random() < 0.5 else {"a": 0.01, "b": 0.99} for _ in range(400)]
    gold = [("a" if max(d, key=d.get) == "a" else "b") if rng.random() < 0.7 else ("b" if max(d, key=d.get) == "a" else "a") for d in p]
    assert fit_temperature(p, gold) > 1.5  # model is overconfident (70% accurate at 0.99) -> soften


def test_row_stats_brier_and_nll_for_perfect_prediction():
    pm, ok, br, nl = row_stats([{"a": 1.0, "b": 0.0}], ["a"])
    assert ok[0] == 1 and br[0] == pytest.approx(0.0, abs=1e-6) and nl[0] == pytest.approx(0.0, abs=1e-5)
