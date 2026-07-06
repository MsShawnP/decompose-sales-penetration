# Code conventions for `app/` (the Dash application)

Applies when working in `decompose-sales-penetration/app/`. Mirror the Spin Rate
`app/` layout: `app.py`, `layout.py`, `views/`, `decomposition.py`, `charts.py`,
`components.py`, `filters.py`, `constants.py`, `panel_data.py`, `lailara_frame.py`.
(Spin Rate's `db.py` is replaced by `panel_data.py` — Decompose has no database.)

## Style
- Match Spin Rate's code style exactly — this is a clone, not a fresh design.
  Follow the ruff config; new files mirror the structure of the Spin Rate file
  that does the same job.
- No mixing paradigms inside a module without a reason stated in DECISIONS.md.

## Naming
- Functions: verbs (`compute_penetration`, `build_waterfall`). Variables: nouns.
  Booleans: predicates (`is_authorized`, `has_lapsed`). Avoid non-standard abbrevs.

## Data (no DB)
- There is no database. All data access goes through `panel_data.py`, the single
  seam onto the in-process `cinderhaven-household-panel` package. Views/filters
  import from `panel_data`, not from the package directly.
- The panel comes from the package — import it, do not re-implement its generation
  or metric logic in `app/`. `warm_cache()` builds it once at startup.
- Health is liveness-only (no DB to gate on) — see root CLAUDE.md / DECISIONS.md.

## Charts
- All charts go through the shared chart template (cloned from Spin Rate). The
  chart rules in the root CLAUDE.md are non-negotiable: automargin, true/non-dup
  currency ticks, bottom legends, bold formatted labels. Inspect every chart.

## Comments
- Comment *why*, not *what*. TODOs include a date or PLAN reference.

## Don't invent
- Before adding a utility, check if Spin Rate already has it. Before adding a
  dependency, ask Shawn and log to DECISIONS.md.

## When stuck
- Smallest reproducer. One change at a time. Read the actual output.
