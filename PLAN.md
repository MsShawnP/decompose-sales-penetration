# Decompose — Current Work Plan

The current arc of work. For session-by-session state, see HANDOFF.md.

**Tier:** Heavy · **Series:** tool #3 of 5 (paired with #4 Leaky Bucket)

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

## Arc history

<!-- Archived on arc completion -->

## Improvement history

<!-- Entries are added by /improve — don't delete this section -->
