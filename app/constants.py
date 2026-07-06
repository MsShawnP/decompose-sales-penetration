"""Lailara design-system tokens and format helpers for Plotly/Dash charts.

Cloned from Spin Rate's constants: all color values come from the lailara-palette
package (the single source of truth) and are re-exported under short semantic
aliases the rest of the app imports. Decompose-specific additions (the three-lever
labels/colors) live at the bottom; Spin Rate's quadrant/SPPD tokens are dropped.
"""

import math

from lailara_palette import (
    LL_CANVAS,
    LL_CARD_BG,
    LL_CARD_BORDER,
    LL_CARD_ITEM,
    LL_CARD_MUTED,
    LL_CARD_SUBTITLE,
    LL_CARD_TEXT,
    LL_CHICAGO,
    LL_CHICAGO_HOVER,
    LL_CHICAGO_LIGHT,
    LL_CHICAGO_SURFACE,
    LL_DISABLED,
    LL_GRIDLINE,
    LL_HK,
    LL_HK_DARK,
    LL_HK_LIGHT,
    LL_HK_SURFACE,
    LL_INK,
    LL_REFERENCE,
    LL_SANS,
    LL_SEQ,
    LL_SERIF,
    LL_SG,
    LL_SG_DARK,
    LL_SG_LIGHT,
    LL_SG_SURFACE,
    LL_STATUS,
    LL_TEXT,
    LL_TEXT_SEC,
    LL_TOKYO,
    LL_TOKYO_DARK,
    LL_TOKYO_LIGHT,
    LL_TOKYO_SURFACE,
)

# ── Canvas & London greyscale ──
WHITE = "#ffffff"
CANVAS = LL_CANVAS
TEXT_PRIMARY = LL_TEXT
TEXT_SECONDARY = LL_TEXT_SEC
GRIDLINE = LL_GRIDLINE
REFERENCE = LL_REFERENCE
DISABLED = LL_DISABLED
INK = LL_INK

# ── Chicago (accent blue) ──
CHICAGO_20 = LL_CHICAGO
CHICAGO_10 = LL_CHICAGO_HOVER
CHICAGO_70 = LL_CHICAGO_LIGHT
CHICAGO_95 = LL_CHICAGO_SURFACE

# ── Hong Kong sequential teal ──
HK_35 = LL_HK
HK_70 = LL_HK_LIGHT
HK_DARK = LL_HK_DARK
HK_95 = LL_HK_SURFACE

# ── Singapore (orange) ──
SG_20 = LL_SG_DARK
SG_55 = LL_SG
SG_70 = LL_SG_LIGHT
SG_95 = LL_SG_SURFACE

# ── Tokyo (berry/rose) ──
TOKYO_20 = LL_TOKYO_DARK
TOKYO_40 = LL_TOKYO
TOKYO_70 = LL_TOKYO_LIGHT
TOKYO_95 = LL_TOKYO_SURFACE

# ── Dark card tokens ──
CARD_BG = LL_CARD_BG
CARD_TEXT = LL_CARD_TEXT
CARD_SUBTITLE = LL_CARD_SUBTITLE
CARD_MUTED = LL_CARD_MUTED
CARD_BORDER = LL_CARD_BORDER
CARD_ITEM = LL_CARD_ITEM

# ── Semantic status ──
PASS_BG = LL_STATUS["pass"]["fill"]
PASS_TEXT = LL_STATUS["pass"]["text"]
WARN_BG = LL_STATUS["warn"]["fill"]
WARN_TEXT = LL_STATUS["warn"]["text"]
FAIL_BG = LL_STATUS["fail"]["fill"]
FAIL_TEXT = LL_STATUS["fail"]["text"]
INFO_BG = LL_STATUS["info"]["fill"]
INFO_TEXT = LL_STATUS["info"]["text"]

# ── Directional semantics ──
TREND_UP = HK_35
TREND_DOWN = TOKYO_40

# ── Categorical palette for product lines (5 hues, no Red/Tokyo) ──
PRODUCT_LINE_COLORS = [
    LL_CHICAGO,       # Chicago-20 — dark blue
    LL_CHICAGO_LIGHT,  # Chicago-70 — light blue
    LL_HK_DARK,       # HK-20 — dark teal
    LL_HK_LIGHT,      # HK-70 — light teal
    LL_SG_DARK,       # SG-20 — dark orange
]

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

# One hue per lever, for legends/labels where levers are shown side by side.
LEVER_COLORS = {
    "buying_households": CHICAGO_20,  # navy — the "who" lever
    "frequency": HK_35,               # teal — the "how often" lever
    "spend_per_trip": SG_55,          # orange — the "how much" lever
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


def fmt_delta(value, decimals=1):
    """Format a percentage-point delta with a direction arrow."""
    if _is_missing(value):
        return "N/A"
    arrow = "↑" if value > 0 else "↓" if value < 0 else "→"
    return f"{arrow} {abs(value * 100):.{decimals}f} pp"


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
