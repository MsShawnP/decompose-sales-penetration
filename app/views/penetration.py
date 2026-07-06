"""Penetration & Buyers view — household penetration trend + new/retained/lapsed flow.

Slice 3 renders the shell skeleton; the trend and buyer-flow charts land in Slice 4.
"""

from dash import html

from app.components import slice4_placeholder, view_heading


def layout():
    return html.Div(
        [
            view_heading(
                "Penetration & buyers",
                "Household penetration is the share of all panel households that "
                "bought you in a quarter — the meaning your dashboard isn't showing.",
            ),
            slice4_placeholder(
                "Household penetration trend",
                "Penetration % across the eight analysis quarters, so a decline "
                "hiding under rising sales is visible.",
            ),
            slice4_placeholder(
                "Buyer flow — new / retained / lapsed",
                "Where each quarter's buyers came from and where they went, "
                "stacked beneath the trend.",
            ),
        ],
        className="view penetration-view",
    )


def register_callbacks():
    # Chart callbacks land in Slice 4.
    return None
