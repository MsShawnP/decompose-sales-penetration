# Test conventions for `tests/`

Applies when working in `decompose-sales-penetration/tests/`. Match the Spin Rate
test bar (many small, behavior-named tests, green before done).

## Must-have tests for this project (hard gates)
- **Waterfall reconciliation:** the three-lever bridge must sum exactly to the
  period-over-period sales delta, across multiple period pairs and edge cases
  (zero delta, single-lever move, all-negative). This is the tool's credibility.
- **Panel canonical/reproducibility:** mirror `cinderhaven-store-universe`'s
  `test_canonical.py` — fixed household count, fixed period count (12 = 8 + 4
  burn-in), locked SEED, `assert_frame_equal` on two generations.
- **Panel realism:** purchase-frequency distribution is right-skewed
  (negative-binomial-ish), not uniform/toy. Assert skew/dispersion bounds.
- **Seeded story:** assert the "growth that's actually erosion" window exists —
  sales up while household penetration down over the seeded periods.
- **Buyer-flow identity:** retained + lapsed = prior-period buyers; retained +
  new = current-period buyers (accounting identities hold every period).
- **Tabs regression:** each tab renders its OWN distinct content (guards the #5
  CSS-refactor regression).

## What doesn't need a test
- Glue/config constants, trivial one-line wrappers, pure type shims.

## Structure & names
- Mirror the source tree. Behavior-named tests: `waterfall_reconciles_when_all_levers_move`,
  not `test_1`.

## Running
- One command runs the suite; document it in README/PLAN. A failing test beats an
  unrun test. Read actual output, not what you expected.
