# Decompose — Current Work Plan

The current arc of work. For session-by-session state, see HANDOFF.md.

**Tier:** Heavy · **Series:** tool #3 of 5 (paired with #4 Leaky Bucket)

---

## Goal — clarified 2026-07-06 (via /clarify)

A **public, interactive-but-guided portfolio demo** that decomposes Cinderhaven's
period-over-period sales change into three levers — buying households (household
penetration) × frequency × spend per trip — with new/retained/lapsed buyer flow,
and tells a CEO/CFO in plain language which lever moved, **all derived honestly
from the SSOT**.

Clarified scope refinements (these shape every slice below):
- **Audience/hosting:** CEO/CFO; public on lailarallc.com. Showcases the *method*
  on Cinderhaven synthetic data — **no upload, no login**; synthetic-data
  disclosure on the page.
- **Interactive-but-guided:** opens on an exec default (whole brand, latest A-vs-B);
  user slices by **Period A/B, product line, retailer** (channel NOT a top control);
  penetration/waterfall/flow/verdict all recompute from the SSOT.
- **Truth principle:** the verdict is always *computed* from the data, never
  scripted. The generator is tuned with realistic parameters so a genuine erosion
  window (price up, penetration down) *exists to be found* — the tool derives it,
  doesn't assert it.
- **Honest-hedge verdict:** when no lever exceeds a set share-of-move threshold,
  the verdict says "mixed / X and Y together" rather than forcing one winner.

---

## Goal

Ship Decompose to `decompose.lailarallc.com`: a household-penetration
decomposition tool on the Spin Rate stack, backed by a new versioned, seed-locked
`cinderhaven-household-panel` package (with burn-in) that tool #4 will reuse.

## Why this arc, why now

The anchor blog post "Penetration Means Three Things" is already live and
explicitly promises household penetration as "the one your dashboard isn't showing
you." This tool is the payoff to a promise already on the site. #4 cannot start
until the shared panel exists, so #3 is on the critical path for two tools.

## Business question this arc answers

Which of the three levers — more buyers, more frequent trips, bigger baskets —
moved this brand's sales between two periods, and which one to pull next.

## Tasks

Work in vertical slices — panel → math → one output end-to-end → app shell →
deploy. Each visualization is reviewed in its own slice, not deferred to polish.

### Slice 0 — Foundation (this session)
- [x] Read prior memory (cinderhaven-db, Spin Rate, Void Finder, doormath); summarize lessons
- [x] Lock decisions: name=Decompose, subdomain, panel size = 5,000 HH × 12 quarters (8 analysis + 4 burn-in)
- [x] Scaffold workflow (state files, CLAUDE hierarchy, .gitignore, git, GitHub remote)
- [x] Write full spec (docs/SPEC.md) + carry brief/brainstorm into docs/

### Slice 1 — Shared household panel package
- [ ] Scaffold `packages/cinderhaven-household-panel` (src layout, pyproject, locked SEED)
- [ ] Generate ~5,000 households with right-skewed (negative-binomial-ish) purchase frequency
- [ ] Timeline: 4 burn-in quarters + 8 analysis quarters, aligned to canonical universe (50 SKUs / 5 lines / 6 retailers)
- [ ] Seed the "growth that's actually erosion" story (sales up on price, penetration down)
- [ ] Lock + version the panel; canonical/reproducibility unit tests (mirror store-universe test_canonical.py)
- [ ] Panel-realism checks (skew, frequency distribution) as tests

### Slice 2 — Decomposition math
- [ ] Household penetration %, purchase frequency, spend per trip (units/trip × price/unit)
- [ ] Three-lever period-over-period waterfall
- [ ] **Unit test: waterfall reconciles exactly to the sales delta** (hard gate)
- [ ] New / retained / lapsed buyer decomposition
- [ ] Plain-language "which lever" verdict generator

### Slice 3 — App shell (clone Spin Rate)
- [ ] Clone app/ structure, lailara_frame, assets, lailara-palette
- [ ] Resilient health: Fly check on a liveness endpoint (200 while up); separate DB-readiness endpoint; branded "data temporarily unavailable" state
- [ ] Wire DATABASE_URL into the synced cred set
- [ ] Branded pre-hydration loading state (no blank white first paint)

### Slice 4 — Outputs (each reviewed in-slice)
- [ ] Three-lever waterfall chart (shared chart template; inspect for clipped labels / dup ticks / legend overlap)
- [ ] Penetration trend + buyer-flow (new/retained/lapsed) chart
- [ ] "Which lever" diagnostic panel; glossary; "why this matters"; tooltips; timeframe labels + as-of date
- [ ] Tabs regression test (each tab renders its own content)

### Slice 5 — Ship
- [ ] `/ce:compound` + multi-agent code review; drive findings to resolution
- [ ] Tests green (match the Spin Rate bar)
- [ ] Deploy to Fly.io + `decompose.lailarallc.com` (CONFIRM name/subdomain/panel/canonical with Shawn first)
- [ ] Work-page card (Door Math / Spin Rate format)
- [ ] Launch/reveal blog post draft ("here's the one your dashboard isn't showing you")
- [ ] HANDOFF.md + FAILURES.md + memory saved; **panel generator left ready for #4**

## Out of scope for this arc

- Building tool #4 (Leaky Bucket) — it imports this panel but is a separate build.
- Any change to `cinderhaven-db` internals (parked pg health-check issue).
- Any change to doormath's or the series' locked canonical figures.
- Real (non-synthetic) panel data.

## Definition of done for this arc

- [ ] Waterfall reconciliation unit test passes exactly.
- [ ] Panel package is versioned, seed-locked, reproducible, and importable by #4.
- [ ] App deployed, resilient `/health` (DB outage → branded shell, not 503).
- [ ] Every chart individually inspected; tabs regression test green.
- [ ] Compound review complete, findings resolved, tests green.
- [ ] Blog post draft + Work-page card delivered.

---

## Decomposition: Slice 1 — cinderhaven-household-panel generator

Goal: A versioned, seed-locked package that deterministically generates a realistic
~5,000-household × 12-quarter panel whose price-up/penetration-down erosion window
**emerges from the mechanism** (not hardcoded), importable by the app and tool #4.

Design note: right-skew comes from per-household latent propensity (gamma → NB
counts). The erosion window is created by a *mechanism* (price rises + price-
sensitive households buying less/lapsing), then the penetration decline is
*computed* from the resulting transactions — never asserted at generation.

Steps:
- [x] A1: Package scaffold + locked constants + quarter calendar
    - Build `packages/cinderhaven-household-panel` (src layout, pyproject mirroring
      cinderhaven-store-universe). Define `SEED`, `N_HOUSEHOLDS=5000`,
      `BURN_IN_QUARTERS=4`, `ANALYSIS_QUARTERS=8`, and a 12-quarter calendar
      (labels + start/end dates). Re-export canonical universe (50 SKUs / 5 lines /
      6 retailers) from cinderhaven-store-universe if importable, else pin locally.
    - Depends on: (none)
    - Done when: `pip install -e` succeeds; `import cinderhaven_household_panel` works;
      a test asserts the constants equal the locked values and the calendar has 12
      quarters (4 burn-in + 8 analysis) with correct, non-overlapping date ranges.
- [ ] A2: Household dimension with right-skewed latent propensity
    - `get_households()` → 5,000 households with id, region, and a gamma-distributed
      latent purchase propensity (the source of NB overdispersion) + a
      price-sensitivity attribute.
    - Depends on: A1
    - Done when: row count == 5000; `assert_frame_equal` across two calls (reproducible);
      a test asserts the propensity distribution is right-skewed (skewness > 0 and
      variance/mean overdispersion above a floor), and all canonical regions present.
- [ ] A3: Price path + price-sensitivity model across the 12 quarters
    - Per-SKU base prices aligned to the canonical universe, and a per-quarter price
      path that *raises* prices over a defined stretch (the mechanism behind the
      erosion window). No penetration outcome is set here — only prices + sensitivity.
    - Depends on: A1
    - Done when: all prices positive; a test asserts the price index rises across the
      intended quarters and is flat/normal elsewhere; 50 SKUs / 5 lines present;
      deterministic across two calls.
- [ ] A4: Transaction generator (the panel)
    - `get_transactions()` → household × date × item × units × spend. Per household
      per quarter, draw trips via Poisson–gamma (NB) from A2 propensity, modulated by
      the A3 price effect on price-sensitive households; each trip emits item lines
      (units × price).
    - Depends on: A2, A3
    - Done when: reproducible (`assert_frame_equal`); a test asserts trips-per-buying-
      household is right-skewed / overdispersed (var > mean); all spend > 0; only
      canonical SKUs appear; every transaction date falls inside its quarter range.
- [ ] A5: Period-metrics + buyer-flow accessors (computed from the panel)
    - `get_period_metrics()` (penetration %, frequency, spend/trip, and its units×price
      split per quarter) and `get_buyer_flow()` (new/retained/lapsed per adjacent
      quarter pair), all derived from A4 transactions.
    - Depends on: A4
    - Done when: penetration ∈ [0,1] every quarter; tests assert the accounting
      identities `buying_hh_prev = retained + lapsed` and `buying_hh_curr = retained +
      new`, and the product identity `sales ≈ buying_hh × frequency × spend_per_trip`
      holds per quarter to tolerance ≤ 1e-6.
- [ ] A6: Verify the erosion window EMERGES (realism/tuning gate)
    - Run A5 metrics over the seeded stretch; confirm computed sales rise while
      computed household penetration falls. If it doesn't emerge, tune A2/A3/A4
      parameters until the mechanism produces it — do not hardcode the outcome.
    - Depends on: A5
    - Done when: a test asserts that across the erosion window, quarter-over-quarter
      sales are up while household penetration is down, using only computed metrics;
      and the same test confirms at least one *other* window is NOT erosion (so the
      signal is specific, not global).
- [ ] B (integration): public API, version lock, full canonical suite, ready for reuse
    - Finalize the public API (`SEED`, `PANEL_VERSION`, constants, `get_households`,
      `get_transactions`, `get_period_metrics`, `get_buyer_flow`), set `PANEL_VERSION`,
      update the package README to match the shipped API.
    - Depends on: A1–A6
    - Done when: full pytest suite green; `assert_frame_equal` across two full
      generations of every accessor; a fresh scratch script can `import` the package
      and pull all four frames; panel is reproducible and ready for the app + tool #4.

---

## Arc history

<!-- Archived on arc completion -->

## Improvement history

<!-- Entries are added by /improve — don't delete this section -->
