---
title: dash-ag-grid columns collapse to zero width when the grid mounts in a hidden tab
date: 2026-07-06
category: ui-bugs
module: app/views/detail.py (Dash tabbed layout + dash-ag-grid)
problem_type: ui_bug
component: frontend_stimulus
symptoms:
  - "Only ~3 of 8 columns render; each is stuck at its ~200px default and the grid horizontal-scrolls instead of filling its container"
  - "The grid's .ag-root-wrapper reports getBoundingClientRect().width == 0 even after switching to its tab"
  - "columnSize='sizeToFit' (and 'responsiveSizeToFit') do not fix it once the tab is shown"
root_cause: async_timing
resolution_type: code_fix
severity: medium
tags: [dash, dash-ag-grid, ag-grid, tabs, column-sizing, hidden-container, responsivesizetofit]
related_components: [dcc-tabs, tab-toggle-callback]
---

# dash-ag-grid columns collapse to zero width when the grid mounts in a hidden tab

## Problem
In a Dash app that pre-renders all tab panels and toggles their `display` (so every
view's callbacks always find their targets), a `dash_ag_grid.AgGrid` placed in a
non-default tab sizes its columns to nothing. The grid initialized while its panel was
`display:none` (0 width), so `sizeToFit` computed against zero and the columns never
recovered — even after the tab became visible.

## Symptoms
- Only a few columns render; they sit at the ~200px default and the grid
  horizontal-scrolls rather than filling the container.
- `document.querySelector('#grid .ag-root-wrapper').getBoundingClientRect().width` is
  `0` when first inspected, and stays narrow after the tab is shown.
- Switching `columnSize` from `"sizeToFit"` to `"responsiveSizeToFit"` does **not** fix
  it on its own.

## What Didn't Work
- **`columnSize="responsiveSizeToFit"`** alone. It attaches a resize handler, but the
  grid had already been built at 0 width in the hidden panel; making the panel visible
  (`display:none → block`) did not reliably re-fire the fit, so columns stayed at their
  defaults (measured 200px each → 1400px total → horizontal scroll).
- **Dispatching `window.dispatchEvent(new Event('resize'))`** after showing the tab.
  It resized the wrapper to the full container width (1152px) but did **not** re-fit the
  *columns* — 8 columns stayed at 200px inside a 1152px viewport.
- Note: this was masked during testing because Dash figure/data callbacks fire at page
  load for **all** views regardless of tab visibility, so chart *data* looked correct
  in hidden panels. Only ag-grid's *layout* depended on the container actually being
  visible — so verifying chart contents didn't surface the grid-sizing bug.

## Solution
Rebuild the grid when its tab is activated by adding the tab selector's value as an
`Input` to the callback that renders the grid. A fresh `AgGrid` that **mounts while its
panel is visible** measures the real container width and `responsiveSizeToFit` fits all
columns correctly.

```python
# app/views/detail.py
@callback(
    Output("metric-cards", "children"),
    Output("detail-table", "children"),
    Input("filter-state", "data"),
    Input("main-tabs", "value"),   # <-- rebuilds the grid when the Detail tab is shown
)
def _update(filter_json, _active_tab):
    period_a, period_b, line, retailer = panel_data.parse_filter_state(filter_json)
    metrics = panel_data.get_metrics(line, retailer)
    return _build_metric_cards(metrics, period_a, period_b), _build_detail_table(metrics)

# the grid itself:
dag.AgGrid(
    rowData=row_data,
    columnDefs=column_defs,
    columnSize="responsiveSizeToFit",
    dashGridOptions={"domLayout": "autoHeight", "suppressCellFocus": True},
    className="ag-theme-alpine decompose-grid",
    style={"width": "100%"},
)
```

Verified live: after the fix all 8 columns fit to width (142/144px each filling 1152px),
no horizontal scroll.

## Why This Works
ag-grid measures its container **once at mount** to lay out columns. When the container
is `display:none`, that measurement is 0, and a one-shot `sizeToFit` collapses the
columns; the resize observer behind `responsiveSizeToFit` does not dependably re-fit on a
`display` change from a pre-rendered hidden panel. Re-mounting the grid *while the panel
is visible* — triggered by keying the render callback on the tab value — guarantees the
first (and correct) measurement happens against the real width. `domLayout: "autoHeight"`
plus `responsiveSizeToFit` then keep it fitted on later container resizes.

## Prevention
- When a data grid lives in a tab/accordion/modal that is **pre-rendered hidden**, make
  its construction depend on the show event (e.g. add the tab-value `Input` to its Dash
  callback) so it mounts at a real width — don't rely on a post-show resize to re-fit.
- Verify grids in the **actually-visible** state. Reading DOM from a hidden panel is
  misleading: Dash data callbacks populate hidden panels at load, so content looks right
  while layout (widths, column count) is still 0. Drive the tab switch (in the preview
  harness, dcc.Tab divs don't respond to synthetic clicks — use a native
  `document.querySelectorAll('.custom-tab')[i].click()` via eval) before measuring.
- Quick check: `getBoundingClientRect().width` on `.ag-root-wrapper` should be non-zero
  and the header-cell count should equal the column count once the tab is open.

## Related Issues
- Introduced in Slice 4D of this project; fix committed in `8b7bc3c`.
- Same class of bug applies to Plotly `dcc.Graph` in hidden panels (renders at a default
  700px until a resize) — there the fix is a `window` resize on show, which is sufficient
  for Plotly but, as shown above, **not** for ag-grid column fitting.
