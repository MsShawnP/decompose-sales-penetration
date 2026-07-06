"""Shared UI building blocks for the Decompose views.

Slice 3 is the app shell: the real charts, cards, and detail table land in Slice 4.
Until then each view renders its own distinct heading plus a labelled placeholder so
the shell is navigable and the tabs-regression test has distinct content to assert.
"""

from dash import html


def view_heading(title: str, blurb: str):
    """A view's serif heading plus a one-line 'why this matters' blurb."""
    return html.Div(
        [
            html.H2(title, className="view-title"),
            html.P(blurb, className="view-blurb"),
        ],
        className="view-heading",
    )


def why_this_matters(text: str):
    """A muted, collapsible 'why this matters' panel for exec context."""
    return html.Details(
        [
            html.Summary("Why this matters", className="why-toggle"),
            html.P(text, className="why-body"),
        ],
        className="why-details",
    )


def slice4_placeholder(label: str, note: str):
    """A labelled placeholder standing in for a Slice 4 output.

    Distinct per view (the label/note differ) so the tabs-regression test sees
    different content in each tab panel.
    """
    return html.Div(
        [
            html.Div(label, className="placeholder-label"),
            html.P(note, className="placeholder-note"),
            html.P("Built in Slice 4.", className="placeholder-tag"),
        ],
        className="slice4-placeholder",
    )
