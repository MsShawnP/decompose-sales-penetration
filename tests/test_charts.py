"""Shared chart-template tests (Slice 5).

The dollar y-axis is the one place that enforces the non-negotiable chart rule:
currency ticks show each tick's TRUE value, evenly spaced, with NO duplicates. These
tests pin that invariant and the degenerate guards so a regression can't ship silently.
"""

import pytest

from app.charts import _nice_dollar_dtick, dollar_yaxis


def _ticks(dtick, range_max):
    """The tick sequence Plotly draws: 0, dtick, 2·dtick, … ≤ range_max."""
    ticks, t = [], 0.0
    while t <= range_max + 1e-9:
        ticks.append(t)
        t += dtick
    return ticks


class TestNiceDollarDtick:
    @pytest.mark.parametrize("bad", [0, -5, -1_000_000])
    def test_nonpositive_returns_safe_step(self, bad):
        # Guards against div-by-zero / log10 of a non-positive max.
        assert _nice_dollar_dtick(bad) == 1.0

    @pytest.mark.parametrize("max_value", [1, 137, 2_400, 49_285, 1_950_000, 24_000_000])
    def test_ticks_are_unique_and_increasing_after_formatting(self, max_value):
        dtick = _nice_dollar_dtick(max_value)
        labels = [f"${t:,.0f}" for t in _ticks(dtick, max_value * 1.15)]
        assert len(labels) == len(set(labels)), f"duplicate $ ticks for max={max_value}: {labels}"
        assert labels == sorted(labels, key=lambda s: int(s.replace("$", "").replace(",", "")))

    # Tick-count reasonableness applies to realistic dollar axes (≥ ~$100); a tiny
    # max legitimately yields few whole-dollar ticks after the $1 floor.
    @pytest.mark.parametrize("max_value", [137, 2_400, 49_285, 1_950_000, 24_000_000])
    def test_tick_count_is_reasonable(self, max_value):
        dtick = _nice_dollar_dtick(max_value)
        n = (max_value * 1.15) / dtick
        assert 3 <= n <= 10, f"{n} ticks for max={max_value} — axis is over/under-divided"


class TestDollarYaxis:
    def test_extends_range_past_max_and_formats_dollars(self):
        axis = dollar_yaxis(100_000)
        assert axis["range"][1] > 100_000  # top data label isn't clipped
        assert axis["tickformat"] == "$~s"  # SI-abbreviated dollars ("$2M", "$325k")

    def test_nonpositive_max_yields_valid_range(self):
        axis = dollar_yaxis(0)
        assert axis["range"][0] == 0 and axis["range"][1] >= 1
