"""Which-Lever view (default tab) — the headline verdict + the waterfall.

Slice 3 wires ONE thing end-to-end to prove the shell: the plain-language verdict
headline recomputes live from the filter selections via the tested
``panel_data.decompose``. The three-lever waterfall chart itself lands in Slice 4.
"""

import json

from dash import Input, Output, callback, html

from app import panel_data
from app.components import slice4_placeholder, view_heading
from app.constants import fmt_dollars


def layout():
    return html.Div(
        [
            view_heading(
                "Which lever moved sales?",
                "Sales can only move three ways: more households buy you, they buy "
                "more often, or they spend more per trip. This is which one did.",
            ),
            html.Div(id="verdict-headline", className="verdict-headline"),
            slice4_placeholder(
                "Three-lever waterfall",
                "Bridges Period A sales to Period B across buying households, "
                "purchase frequency, and spend per trip — reconciled to the exact "
                "sales change.",
            ),
        ],
        className="view which-lever-view",
    )


def _verdict_children(filters: dict):
    period_a = filters.get("period_a") or panel_data.DEFAULT_PERIOD_A
    period_b = filters.get("period_b") or panel_data.DEFAULT_PERIOD_B
    result = panel_data.decompose(
        period_a, period_b, filters.get("product_line"), filters.get("retailer")
    )
    wf = result["waterfall"]
    verdict = result["verdict"]
    direction_class = "delta-up" if wf.delta >= 0 else "delta-down"
    return [
        html.Div(
            fmt_dollars(wf.sales_b) + " in " + period_b,
            className="verdict-figure",
        ),
        html.Div(
            f"{'+' if wf.delta >= 0 else '−'}{fmt_dollars(abs(wf.delta))} vs {period_a}",
            className=f"verdict-change {direction_class}",
        ),
        html.P(verdict["sentence"], className="verdict-sentence"),
    ]


def register_callbacks():
    @callback(
        Output("verdict-headline", "children"),
        Input("filter-state", "data"),
    )
    def _update_verdict(filter_json):
        filters = json.loads(filter_json) if filter_json else {}
        return _verdict_children(filters)
