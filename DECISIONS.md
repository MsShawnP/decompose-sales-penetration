# Decompose — Decisions Log

Permanent record of choices that should survive session turnover. If a decision
is reversed, strike it through and add the replacement below — don't delete.

---

## Architecture & Pipeline

### 2026-07-06 — Clone the Spin Rate stack; do not reinvent
- **Why:** #1/#2 are live and proven. Dash 3.x + Plotly 6.0 + pandas + psycopg2 +
  Gunicorn/Docker/Fly is the shipped stack. Reuse app shell, `lailara_frame`,
  `lailara-palette`, and the shared chart template so #2 and #3 are visually
  identical by construction.
- **Scope:** global.
- **Do not:** rebuild UI chrome or chart config from scratch.

### 2026-07-06 — Decompose uses NO database; data is the in-process panel
- **Why:** Slices 1–2 built the household panel as a deterministic, seed-locked
  *in-process package* (`cinderhaven-household-panel`), not `cinderhaven-db` tables.
  The panel is deterministic, so a DB copy would only duplicate canonical data.
- **Decision:** The app imports the package and warms it once at startup
  (`panel_data.warm_cache()`); no psycopg2, no `DATABASE_URL`, no Postgres at
  request time. This holds Decompose (and #4, which imports the same package)
  entirely off the `cinderhaven-db` fragility surface: no cred sync, no 503 gate,
  no dependence on the unrepairable pg health check.
- **Scope:** global (data layer, deploy, health). Confirmed with Shawn.
- **Supersedes:** the two struck decisions below (resilient-health, DATABASE_URL).

### 2026-07-06 — Health is liveness-only (no readiness endpoint, no 503 gate)
- **Why:** With no DB, there is nothing to degrade — the Spin Rate `/health` 503
  bug is designed *out*, not worked around.
- **Decision:** The Fly check targets a liveness endpoint that returns 200 while
  the process is up. No DB-readiness endpoint. **Do not** add a health path that
  can return non-200 for a data reason.
- **Scope:** `wsgi.py`, `fly.toml`.

### 2026-07-06 — Warm the panel at startup; no disk cache
- **Why:** Panel generation is **measured ~0.6s** and `get_transactions` is already
  `functools.lru_cache(maxsize=1)` (built once per process). With Fly
  `min_machines_running = 1` the machine stays up, so the cost is paid once at boot.
- **Decision:** `panel_data.warm_cache()` calls `get_transactions()` once at startup
  so no visitor's request pays generation. **No parquet/disk cache:** it would save
  only ~0.6s at rare process boots and could not be wired without coupling to the
  package's internal cache (which app/CLAUDE.md forbids re-implementing). Measured,
  not assumed. (Overrides the "cache to disk as parquet" phrasing in the Slice 3
  ask, on the strength of the measurement — flagged to Shawn.)
- **Scope:** `app/panel_data.py`.

### ~~2026-07-06 — Resilient health: do NOT hard-gate the Fly check on the DB~~  · SUPERSEDED
> Superseded by "Decompose uses NO database" above — there is no DB to gate on, so
> there is no readiness endpoint at all. Original kept for the record:
- **Why:** Spin Rate's `/health` returns 503 when the DB is down and its
  `fly.toml` check targets `/health`; a DB outage pulled both machines from the
  proxy and 503'd the whole site externally. The branded shell can serve without
  the DB.
- **Decision:** Fly health check targets a **liveness** endpoint returning 200
  while the process is up. DB connectivity is reported on a **separate**
  readiness/observability endpoint and surfaced in-app as "data temporarily
  unavailable" over the branded shell.
- **Scope:** `wsgi.py`, `fly.toml`.

### ~~2026-07-06 — DATABASE_URL into the synced credential set~~  · SUPERSEDED
> Superseded by "Decompose uses NO database" above — the app never sets or reads
> `DATABASE_URL`. Original kept for the record:
- **Why:** Stale `DATABASE_URL` secrets desynced and broke spinrate/ask-cinderhaven/
  edi-recon. Canonical credential lives in `cinderhaven-data-platform/.env`.
- **Decision:** Wire this app's `DATABASE_URL` into the synced set; URL shape
  `postgres://postgres:<OPERATOR_PASSWORD>@cinderhaven-db.flycast:5432/<db>?sslmode=disable`.
- **Scope:** deploy/secrets. **Do not:** commit or print the credential value.

## Product & Scope (from /clarify, 2026-07-06)

### 2026-07-06 — Narrative is computed from the SSOT, never scripted
- **Why:** Shawn: "the data in the SSOT tells the truth; the narrative tells the
  truth based on the data." Overriding the brief's "seed the punchline" phrasing:
  we do NOT force data to fit a predetermined story.
- **Decision:** The "which lever" verdict and all narrative are a truthful function
  of the actual panel data for the selected period/filter. The generator is tuned
  with realistic parameters so a genuine erosion window exists to be *found* — the
  tool derives the finding; it never hardcodes it. Change the selection → the
  verdict changes.
- **Scope:** global. **Do not:** hardcode a conclusion or stage data to a claim.

### 2026-07-06 — Public portfolio demo on Cinderhaven only; no upload, no login
- **Why:** Intended audience is CEO/CFO; it's a portfolio piece open to all from
  lailarallc.com. It showcases the *method*, not a bring-your-own-data tool.
- **Decision:** No user data upload, no auth. Synthetic-data disclosure stays on
  the page. **Do not:** add a "try your own data" path.

### 2026-07-06 — Interactive-but-guided; slice by period / product line / retailer
- **Decision:** Opens on an exec default (whole brand, latest A-vs-B). Light,
  labeled controls: Period A vs Period B, product line, retailer — all recompute
  from the SSOT. Channel is NOT a top-level control (keeps it clean for a CEO).
- **Why:** A CEO/CFO won't drive an analyst cockpit, but interactivity lets a
  skeptic re-slice and watch the verdict change (serves the truth principle).

### 2026-07-06 — Honest-hedge verdict when no lever dominates
- **Decision:** When no single lever exceeds a defined share-of-move threshold, the
  verdict reports "mixed / X and Y together" instead of naming a marginal winner.
- **Why:** On a public piece aimed at CEOs, overstating a near-tie undercuts
  credibility. Threshold value TBD in Slice 2; log it when set.

## Data & Schema

### 2026-07-06 — Panel ships as a standalone versioned package with burn-in
- **Decision:** `cinderhaven-household-panel` (src layout, locked `SEED`),
  imported by both #3 and #4 — never a second copy. Timeline includes a burn-in
  period baked in now (4 quarters) before the 8-quarter analysis window.
- **Why:** #4's trial/repeat needs history runway; retrofitting burn-in later is
  expensive. Mirrors how doormath ships `cinderhaven-store-universe`.
- **Scope:** `packages/cinderhaven-household-panel`.
- **Do not:** regenerate the panel per run or copy it into #4.

### 2026-07-06 — Panel size: 5,000 households × 12 quarters (8 analysis + 4 burn-in)
- **Why:** ~5,000 matches the brief target; quarterly grain reads cleanly for a
  multi-quarter penetration decline; 4 burn-in quarters give #4 runway. Confirmed
  by Shawn 2026-07-06.
- **Scope:** panel generation constants.

### 2026-07-06 — Panel aligns to the canonical universe; its own figures are locked at generation
- **Decision:** Households buy the canonical 50 SKUs / 5 lines / 6 retailers of the
  ~$25M Cinderhaven brand. Panel-specific figures are locked + versioned at
  generation (like `CINDERHAVEN_CANONICAL`); they are additive and must not alter
  any existing canonical figure.
- **Scope:** global. **Do not:** change doormath's or the series' locked figures
  without the change protocol + impact check + Shawn's approval.

### 2026-07-06 — Bake #4 Leaky Bucket's two launch stories into the shared panel now
- **Decision:** The panel designates **two new-launch SKUs** so tool #4 is pure
  reuse and never forces a panel change: one **leaky** (big trial reach, low repeat
  → ~15% repeat) and one **sticky** (modest trial reach, high repeat → 45%+ repeat),
  both launching inside the analysis window with post-launch runway.
- **Why:** #4 is a trial/repeat tool built on this exact panel; retrofitting launch
  dynamics later would break the shared-asset contract. Shawn, 2026-07-06.
- **Truth principle:** only the *mechanism* is set (trial reach + repeat propensity
  params × household affinity). The ~15% / 45%+ repeat rates are **computed** from the
  generated transactions and verified against bands in A6 — not hardcoded outputs.
- **Scope:** `packages/cinderhaven-household-panel` (A3/A4/A6). **Do not:** hardcode
  the repeat rates or expose a launch story #4 can't recompute from transactions.

### 2026-07-06 — Penetration erosion is a QUARTERLY phenomenon; compare quarter-over-quarter
- **Finding (from A4 measurement):** household penetration erosion shows at the
  quarterly grain (2024-Q4 pen 44.1% + sales $46.6k → 2025-Q4 pen 43.0% + sales
  $52.3k). At the ANNUAL grain, reach saturates (~72% of households buy at least once
  a year regardless of price), so annual buyers barely move and the erosion hides.
- **Decision:** Decompose's period-over-period comparison operates at the quarter
  grain; the default erosion showcase is year-over-year same quarter (2025-Q4 vs
  2024-Q4), which also sidesteps the unmodeled-seasonality issue. This is honest and
  reinforces the thesis — annual penetration hides what quarterly reveals ("the metric
  your dashboard isn't showing you").
- **Do not:** frame the erosion as an annual-penetration decline — it isn't one.

### 2026-07-06 — New panel tables live in the same cinderhaven-db SSOT as new tables
- **Why:** Keep one source of truth; #4 reads the same tables.
- **Do not:** touch the canonical `cinderhaven` raw schema or `cinderhaven-db`
  internals (its parked `pg` health-check issue) without separate explicit go-ahead.

## Visualization

### 2026-07-06 — Chart rules baked into the shared template (from #5)
- `automargin` so the longest label never clips; currency ticks show true,
  evenly-spaced values with no duplicates (fix `dtick` + formatter, extend axis
  max); legends bottom-horizontal; bold formatted data labels; inspect every
  chart after building. Tables never truncate the key ID column.
- **Scope:** all charts/tables.

## Output Formats

### 2026-07-06 — Exec-facing framing
- Lead with one big plain-language headline number; label every number with its
  timeframe + as-of date; tooltips on every metric/filter; glossary; "why this
  matters" panel; synthetic-data disclosure on page. Copy gets a Shawn review pass.

## Project Setup

### 2026-07-06 — Name = Decompose, subdomain decompose.lailarallc.com, private repo
- **Why:** Direct payoff to the live "Penetration Means Three Things" post.
  Repo private now; flips public later via the `/publish` gate.
- **Note:** The original folder was misspelled `decomppose-sales-penetration` and
  is pinned open by the live session (Windows lock), so it could not be renamed
  in place. Work lives in `decompose-sales-penetration`; the empty misspelled
  folder should be deleted from a session not rooted in it.

---

## Reversed / Superseded

<!-- Strike original above, add replacement here, link both ways. -->
