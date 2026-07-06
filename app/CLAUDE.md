# Code conventions for `app/` (the Dash application)

Applies when working in `decompose-sales-penetration/app/`. Mirror the Spin Rate
`app/` layout: `app.py`, `layout.py`, `views/`, `calculations.py`, `charts.py`,
`components.py`, `filters.py`, `constants.py`, `db.py`, `lailara_frame.py`.

## Style
- Match Spin Rate's code style exactly — this is a clone, not a fresh design.
  Follow the ruff config; new files mirror the structure of the Spin Rate file
  that does the same job.
- No mixing paradigms inside a module without a reason stated in DECISIONS.md.

## Naming
- Functions: verbs (`compute_penetration`, `build_waterfall`). Variables: nouns.
  Booleans: predicates (`is_authorized`, `has_lapsed`). Avoid non-standard abbrevs.

## Data & DB
- All DB access goes through `db.py` with a pooled connection. Never hard-gate the
  Fly health check on the DB (see DECISIONS.md). Never print/commit the credential.
- The panel comes from the `cinderhaven-household-panel` package — import it, do
  not re-implement generation logic in `app/`.

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
