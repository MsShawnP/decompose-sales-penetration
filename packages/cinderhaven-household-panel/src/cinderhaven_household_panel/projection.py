"""Brand-scale projection factor for the household panel.

The panel is a ~5,000-household sample. `get_projection_factor()` returns the single
fixed weight ``k`` that scales ABSOLUTE totals — sales $, buyer/household counts, trip
counts — from panel scale up to Cinderhaven's brand scale. RATES (household
penetration %, purchase frequency, spend per trip) are ratios and are NOT scaled: k
appears in both numerator and denominator and cancels.

``k`` is locked, not re-derived per period, so real period-over-period movement is
preserved and merely scaled. It is anchored so the panel's reference-year sales
project to the canonical ANNUAL scan revenue:

    k = CANONICAL_ANNUAL_SCAN_REVENUE / (raw panel sales for PROJECTION_REFERENCE_YEAR)

This DERIVES from the locked canonical figure; it does not alter it. Tool #4 (Leaky
Bucket) imports this same factor, so any absolute buyer counts it shows match.
"""

import functools

from .constants import CANONICAL_ANNUAL_SCAN_REVENUE, PROJECTION_REFERENCE_YEAR
from .transactions import get_transactions

# Absolute columns that get projected. Rates (penetration, frequency, spend_per_trip,
# units_per_trip, price_per_unit) and buyer-flow rates are deliberately absent.
PROJECTED_METRIC_COLUMNS = ("buying_households", "trips", "units", "sales")
PROJECTED_FLOW_COLUMNS = ("prior_buyers", "current_buyers", "retained", "new", "lapsed")


@functools.lru_cache(maxsize=1)
def get_projection_factor() -> float:
    """The locked sample-to-brand-scale weight ``k`` (see module docstring).

    Computed once from the deterministic panel, so it is itself locked: the reference
    year's raw panel sales are fixed by SEED, and the canonical anchor is a constant.
    """
    tx = get_transactions()
    ref = str(PROJECTION_REFERENCE_YEAR)
    raw_ref_year_sales = tx.loc[tx["quarter_label"].str.startswith(ref), "spend"].sum()
    return CANONICAL_ANNUAL_SCAN_REVENUE / float(raw_ref_year_sales)
