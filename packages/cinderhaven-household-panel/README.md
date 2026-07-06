# cinderhaven-household-panel

Shared, versioned, **seed-locked** synthetic **household panel** for the
Cinderhaven sales-penetration tools. Built by tool #3 (Decompose); imported
unchanged by tool #4 (Leaky Bucket). This is the largest new data asset of the
series — panel data, not POS scan data.

> **Not yet implemented.** This README defines the contract and planned API so
> Slice 1 builds to it. Mirror `cinderhaven-store-universe` (doormath) for
> packaging, seed-locking, and the canonical test pattern.

## Why a package (not per-tool code)

The panel is shared with #4. A second copy would drift. Ship it once as a
`pip install -e`-able package with a locked `SEED`, deterministic generation, and
a canonical test — exactly how `cinderhaven-store-universe` is shipped.

## Grain

`household_id × transaction × item × date × spend` — with derived per-period
aggregates. Households buy the canonical universe: ~$25M brand, 50 SKUs, 5 product
lines (AS·PS·SC·DG·SB), 6 retailers.

## Timeline (locked)

- **~5,000 households**
- **12 quarters total** = **4 burn-in quarters** + **8 analysis quarters**
- Burn-in exists so tool #4's trial/repeat logic has history runway before the
  analysis window. Do not remove it.

## Realism bar

- Purchase-incidence and frequency distributions are heavily right-skewed
  (negative-binomial-ish). If they look uniform/toy, anyone who has seen real
  panel output dismisses the demo. Enforced by realism unit tests.

## Seeded story (the punchline)

A deliberate window where **sales grow on price increases while household
penetration quietly declines** — "growth that's actually erosion" — mapping to the
trap named in the anchor blog post. Enforced by a unit test.

## Planned API (subject to Slice 1)

```python
from cinderhaven_household_panel import (
    SEED,                    # locked int
    PANEL_VERSION,           # e.g. "0.1.0"
    ANALYSIS_QUARTERS, BURN_IN_QUARTERS,
    get_households,          # household dimension (id, region, segment, ...)
    get_transactions,        # household × date × item × spend (the panel)
    get_period_metrics,      # penetration %, frequency, spend/trip per period
    get_buyer_flow,          # new / retained / lapsed per period pair
)
```

All generators are deterministic given `SEED` and return identical frames across
calls (`assert_frame_equal`).

## Tests

Mirror `cinderhaven-store-universe/tests/test_canonical.py`: fixed counts, locked
seed, reproducibility, realism (skew), and the seeded-story assertion.
