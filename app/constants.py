"""Lailara design-system tokens and format helpers for Plotly/Dash charts.

Cloned from Spin Rate's constants, then trimmed to the tokens Decompose's charts
actually use — colour values still come from the lailara-palette package (the single
source of truth), re-exported under short semantic aliases. The three-lever
vocabulary (labels, waterfall colours) lives at the bottom.
"""

import math

from lailara_palette import (
    LL_CANVAS,
    LL_CHICAGO,
    LL_GRIDLINE,
    LL_HK,
    LL_INK,
    LL_REFERENCE,
    LL_SANS,
    LL_SERIF,
    LL_TEXT_SEC,
    LL_TOKYO,
)

# ── Canvas & London greyscale ──
CANVAS = LL_CANVAS
TEXT_SECONDARY = LL_TEXT_SEC
GRIDLINE = LL_GRIDLINE
REFERENCE = LL_REFERENCE
INK = LL_INK

# ── Accent hues (default shades) ──
CHICAGO_20 = LL_CHICAGO   # navy
HK_35 = LL_HK             # teal
TOKYO_40 = LL_TOKYO       # berry

# ── Typography (for Plotly) ──
FONT_SERIF = f"{LL_SERIF}, Georgia, Times New Roman, serif"
FONT_SANS = f"{LL_SANS}, Source Sans Pro, Helvetica Neue, Helvetica, Arial, sans-serif"

# ── The three levers (Decompose's core vocabulary) ──────────────────
# Keys match app.decomposition.LEVERS and the panel metric columns.
LEVER_ORDER = ("buying_households", "frequency", "spend_per_trip")

LEVER_LABELS = {
    "buying_households": "Buying households",
    "frequency": "Purchase frequency",
    "spend_per_trip": "Spend per trip",
}

# Waterfall bar semantics (direction of each contribution to ΔSales).
WATERFALL_INCREASE = HK_35     # teal — a lever that pushed sales up
WATERFALL_DECREASE = TOKYO_40  # berry — a lever that pushed sales down
WATERFALL_TOTAL = CHICAGO_20   # navy — the period-A and period-B totals


# ── Format helpers ──
def _is_missing(value):
    return value is None or (isinstance(value, float) and math.isnan(value))


def fmt_pct(value, decimals=1):
    """Format a decimal (0.123) as a percentage string ('12.3%')."""
    if _is_missing(value):
        return "N/A"
    return f"{value * 100:.{decimals}f}%"


def fmt_number(value):
    """Format a count with thousands separators."""
    if _is_missing(value):
        return "N/A"
    return f"{value:,.0f}"


def fmt_dollars(value):
    """Format a dollar amount with K/M suffixes."""
    if _is_missing(value):
        return "N/A"
    if abs(value) >= 1_000_000:
        return f"${value / 1_000_000:,.1f}M"
    if abs(value) >= 1_000:
        return f"${value / 1_000:,.0f}K"
    return f"${value:,.0f}"


def fmt_signed_dollars(value):
    """Format a signed dollar contribution ('+$12K' / '-$3K') for waterfall labels."""
    if _is_missing(value):
        return "N/A"
    sign = "+" if value >= 0 else "-"
    return f"{sign}{fmt_dollars(abs(value))}"
