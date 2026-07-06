"""Detail view — per-period metric cards + an ag-grid detail table.

Slice 3 renders the shell skeleton; the cards and table land in Slice 4.
"""

from dash import html

from app.components import slice4_placeholder, view_heading


def layout():
    return html.Div(
        [
            view_heading(
                "Period detail",
                "The three levers side by side for the two periods, with the "
                "spend-per-trip split into units per trip × price per unit.",
            ),
            slice4_placeholder(
                "Per-period metric cards",
                "Penetration %, purchase frequency, and spend per trip for "
                "Period A and Period B, with the change on each.",
            ),
            slice4_placeholder(
                "Detail table",
                "Every metric per quarter in a sortable grid — the numbers behind "
                "the waterfall.",
            ),
        ],
        className="view detail-view",
    )


def register_callbacks():
    # Table/card callbacks land in Slice 4.
    return None
