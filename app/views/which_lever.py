"""Which-Lever view (default tab) — the headline verdict + the three-lever waterfall.

The verdict headline and the waterfall both recompute live from the filter selections
via the tested ``panel_data.decompose``. The waterfall is an exact Shapley bridge:
Period-A sales → ± buying households → ± purchase frequency → ± spend per trip →
Period-B sales, and the bars reconcile to the sales change by construction.
"""

import plotly.graph_objects as go
from dash import Input, Output, callback, dcc, html

from app import panel_data
from app.charts import CHART_CONFIG, dollar_yaxis, economist_layout
from app.components import definitions_panel, view_heading, why_this_matters
from app.constants import (
    FONT_SANS,
    FONT_SERIF,
    INK,
    LEVER_LABELS,
    LEVER_ORDER,
    REFERENCE,
    WATERFALL_DECREASE,
    WATERFALL_INCREASE,
    WATERFALL_TOTAL,
    fmt_dollars,
    fmt_signed_dollars,
)

_WHY = (
    "Sales are buying households × purchase frequency × spend per trip — the only "
    "three things that can move them. The waterfall splits the change between your "
    "two periods across exactly those three levers, and the pieces sum to the total "
    "change. The verdict names the lever that did the most work."
)


def layout():
    return html.Div(
        [
            view_heading(
                "Which lever moved sales?",
                "Sales can only move three ways: more households buy you, they buy "
                "more often, or they spend more per trip. This is which one did.",
            ),
            html.Div(id="verdict-headline", className="verdict-headline"),
            dcc.Graph(id="waterfall-chart", config=CHART_CONFIG, style={"minHeight": "440px"}),
            html.P(
                "Teal raised sales, berry lowered them; navy bars are the period "
                "totals. Bars sum exactly to the change.",
                className="chart-caption",
            ),
            why_this_matters(_WHY),
            definitions_panel(),
        ],
        className="view which-lever-view",
    )


def _verdict_children(wf, verdict, period_a, period_b):
    if wf.delta == 0:
        change, direction_class = f"no change vs {period_a}", "delta-flat"
    else:
        sign = "+" if wf.delta > 0 else "−"
        change = f"{sign}{fmt_dollars(abs(wf.delta))} vs {period_a}"
        direction_class = "delta-up" if wf.delta > 0 else "delta-down"
    return [
        html.Div(fmt_dollars(wf.sales_b) + f" in {period_b}", className="verdict-figure"),
        html.Div(change, className=f"verdict-change {direction_class}"),
        html.P(verdict["sentence"], className="verdict-sentence"),
    ]


def _build_waterfall_figure(wf, period_a, period_b):
    """Build the three-lever waterfall bridging Period A sales to Period B."""
    labels = [LEVER_LABELS[lever] for lever in LEVER_ORDER]
    contribs = [wf.contributions[lever] for lever in LEVER_ORDER]

    x = [period_a, *labels, period_b]
    measure = ["absolute", "relative", "relative", "relative", "total"]
    y = [wf.sales_a, *contribs, wf.sales_b]
    text = [
        fmt_dollars(wf.sales_a),
        *[fmt_signed_dollars(c) for c in contribs],
        fmt_dollars(wf.sales_b),
    ]
    # Exact dollars on hover (the outside bar labels are rounded to $K).
    hover = [
        f"${wf.sales_a:,.0f}",
        *[f"{'+' if c >= 0 else '−'}${abs(c):,.0f}" for c in contribs],
        f"${wf.sales_b:,.0f}",
    ]

    fig = go.Figure(
        go.Waterfall(
            orientation="v",
            measure=measure,
            x=x,
            y=y,
            text=text,
            textposition="outside",
            textfont=dict(family=FONT_SANS, size=13, color=INK),
            cliponaxis=False,
            customdata=hover,
            connector=dict(line=dict(color=REFERENCE, width=1)),
            increasing=dict(marker=dict(color=WATERFALL_INCREASE)),
            decreasing=dict(marker=dict(color=WATERFALL_DECREASE)),
            totals=dict(marker=dict(color=WATERFALL_TOTAL)),
            hovertemplate="%{x}<br>%{customdata}<extra></extra>",
        )
    )

    axis_max = max(wf.sales_a, wf.sales_b)
    # xaxis inherits economist_layout's default (showline, automargin, tickfont).
    layout = economist_layout(
        title=dict(
            text=f"What moved sales, {period_a} → {period_b}",
            font=dict(family=FONT_SERIF, size=22, color=INK),
        ),
        yaxis=dollar_yaxis(axis_max, title="Sales ($)"),
        showlegend=False,
        margin=dict(l=72, r=24, t=64, b=56),
    )
    fig.update_layout(**layout)
    return fig


def register_callbacks():
    @callback(
        Output("verdict-headline", "children"),
        Output("waterfall-chart", "figure"),
        Input("filter-state", "data"),
    )
    def _update(filter_json):
        period_a, period_b, line, retailer = panel_data.parse_filter_state(filter_json)
        result = panel_data.decompose(period_a, period_b, line, retailer)
        wf, verdict = result["waterfall"], result["verdict"]
        return (
            _verdict_children(wf, verdict, period_a, period_b),
            _build_waterfall_figure(wf, period_a, period_b),
        )
