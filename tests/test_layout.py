"""Shell / tabs-regression tests (Slice 3F).

The hard gate carried from tool #5: each tab must render its OWN distinct content
(a CSS/markup refactor once silently broke this). We assert it structurally — every
view renders a unique heading, the content area pre-renders one panel per tab with
the right ids, and exactly the default panel is visible at load.
"""

from app.layout import TAB_IDS, TAB_LABELS, _build_content_area, _build_tabs
from app.views import detail, penetration, which_lever


def _text(component) -> str:
    """Flatten a Dash component tree into its concatenated string content."""
    if isinstance(component, str):
        return component
    if isinstance(component, (list, tuple)):
        return " ".join(_text(c) for c in component)
    children = getattr(component, "children", None)
    if children is None:
        return ""
    return _text(children)


def _ids(component) -> set:
    """Collect every component id present in a Dash component tree."""
    found = set()

    def walk(node):
        if node is None or isinstance(node, str):
            return
        if isinstance(node, (list, tuple)):
            for n in node:
                walk(n)
            return
        cid = getattr(node, "id", None)
        if isinstance(cid, str):
            found.add(cid)
        children = getattr(node, "children", None)
        if children is not None:
            walk(children)

    walk(component)
    return found


class TestTabsRegression:
    def test_three_tabs_with_matching_labels_and_ids(self):
        tabs = _build_tabs()
        values = [tab.value for tab in tabs.children]
        labels = [tab.label for tab in tabs.children]
        assert values == TAB_IDS
        assert labels == TAB_LABELS
        assert tabs.value == "which-lever"  # exec default tab

    def test_each_view_renders_its_own_distinct_heading(self):
        headings = {
            "which-lever": _text(which_lever.layout()),
            "penetration": _text(penetration.layout()),
            "detail": _text(detail.layout()),
        }
        assert "Which lever moved sales?" in headings["which-lever"]
        assert "Penetration & buyers" in headings["penetration"]
        assert "Period detail" in headings["detail"]
        # Pairwise distinct — no two tabs render the same content.
        assert len(set(headings.values())) == 3

    def test_content_area_prerenders_one_panel_per_tab(self):
        area = _build_content_area()
        panels = area.children
        assert [p.id for p in panels] == [f"tab-panel-{t}" for t in TAB_IDS]

    def test_only_the_default_panel_is_visible_at_load(self):
        panels = _build_content_area().children
        displays = [p.style["display"] for p in panels]
        assert displays == ["block", "none", "none"]


class TestChartTargets:
    """Each view must render the output targets its callbacks write to, or the
    figure/table callbacks would silently no-op (an invisible regression)."""

    def test_which_lever_renders_verdict_and_waterfall(self):
        ids = _ids(which_lever.layout())
        assert {"verdict-headline", "waterfall-chart"} <= ids

    def test_penetration_renders_both_charts(self):
        ids = _ids(penetration.layout())
        assert {"penetration-trend", "buyer-flow"} <= ids

    def test_detail_renders_cards_and_table(self):
        ids = _ids(detail.layout())
        assert {"metric-cards", "detail-table"} <= ids
