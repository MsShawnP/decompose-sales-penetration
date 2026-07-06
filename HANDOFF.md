# Decompose — Handoff Log

Session-by-session state. Updated by /log mid-session and /wrap at session end.

For durable choices, see DECISIONS.md. For the current arc, see PLAN.md. For
things that didn't work, see FAILURES.md.

---

## 2026-07-06 — Slice 5: reviewed, fixed, DEPLOYED (custom-domain DNS pending)

**Deployed.** Live at **https://decompose-sales-penetration.fly.dev** (2 machines,
iad, health checks passing). `/health` → `200 {"status":"ok"}`; production
`_dash-layout` contains all chart targets + as-of note + synthetic disclosure — the
panel generates in-container and the app is fully wired.

**⚠ One manual step left (Shawn — no registrar access from here):** point
`decompose.lailarallc.com` DNS at Fly, then it goes live on the branded domain. Cert
already created (`fly certs add`), currently "Not verified" pending DNS. Records:
- `A    decompose → 66.241.125.108`
- `AAAA decompose → 2a09:8280:1::140:558f:0`
  (or a `CNAME decompose → decompose-sales-penetration.fly.dev`). Then
  `fly certs check decompose.lailarallc.com`.

**5A — multi-agent code review (5 personas):** correctness, Python, maintainability,
testing, project-standards. Drove all real findings to resolution:
- **Correctness bug fixed:** period_a == period_b made the verdict falsely claim
  "Sales rose $0 … driven by more households buying." Now a neutral "unchanged"
  verdict + neutral headline.
- Data-driven card deltas (no more label-string branch); consolidated 3 duplicated
  `_filters` into `panel_data.parse_filter_state`; removed 34 dead palette tokens +
  `fmt_delta`; dropped redundant xaxis overrides; added value labels to the
  buyer-flow bars + penetration points (chart rule); hardened `_nice_dollar_dtick`
  ($1 floor). **+24 tests** (charts, figure-builders, zero-delta, parse). Fixed the
  stale README (no-DB reality).

**5B — drafts** in `docs/launch/` (blog reveal post + work-page card) for Shawn's
copy pass.

**5C — deploy:** vendored `cinderhaven-store-universe` into `packages/` (best-practice
for this context — matches the lailara-palette precedent; textbook alt is a private
index but that's overkill for a locked, versioned canonical package). Panel's 49
canonical tests still pass (no drift). Confirmed with Shawn: name/subdomain/panel
unchanged; deploy go-ahead given.

**State:** **104 tests green** (55 app + 49 panel), ruff clean. Image 151 MB.

**Remaining (not blocking a working deploy):**
- DNS for the custom domain (above).
- Optional: `/ce:compound` to compound the learnings (no-DB decision, ag-grid
  hidden-init fix, the review). `/publish` to flip the repo public when ready.
- Shawn's copy pass on the blog/work-card; a prescriptive "next move" line on the
  verdict if wanted (kept computed/honest for now).

---

## 2026-07-06 — Slice 4 complete: all outputs live (charts, cards, table)

**Did (5 commits, 4A–4E):** Built the real outputs, each inspected in-slice.
- `charts.py`: cloned economist_layout + CHART_CONFIG; added `dollar_yaxis` /
  `_nice_dollar_dtick` for true, evenly-spaced, non-duplicate $ ticks.
- **Waterfall** (which_lever): `go.Waterfall` bridging Period A→B across the three
  levers, reconciled to ΔSales; increase=teal / decrease=berry / totals=navy, bold
  signed-$ labels, exact-$ hover. Figure + verdict recompute together from filters.
- **Penetration trend + buyer flow** (penetration): penetration % line (A/B marked)
  + new/retained/lapsed relative bars (lapsed below zero).
- **Metric cards + ag-grid table** (detail): four cards (Sales, penetration,
  frequency, spend/trip; B big, A + signed Δ) + per-quarter grid (Quarter pinned,
  cents where they matter).
- **Glossary** (6 terms), **filter tooltips**, **why-this-matters** panels.

**Real bug fixed:** ag-grid mounted in a `display:none` tab panel sized its columns
to 0 width. Keyed the detail callback on `main-tabs` value so the grid rebuilds when
the tab is shown → responsiveSizeToFit fits all 8 columns. (Also: charts render their
data via callbacks at load regardless of tab visibility — so verifying chart *data*
doesn't require the tab to be visible; only the ag-grid *sizing* did.)

**Inspected** @1280 and @375 across all three tabs: no clipped labels, currency
ticks true/non-duplicate ($0..$50,000; 0%..50%), legends at bottom, bold labels, no
horizontal overflow, no console errors. Whole-brand default is the erosion story end
to end — penetration −2.2pp, frequency −0.14 trips, spend/trip +$1.88 → +$1,954.

**State:** **80 tests green** (31 app + 49 panel), ruff clean. Preview-harness notes:
Plotly inits at 0 width until a viewport is set (resize to 1280 first); dcc.Tab divs
don't respond to `preview_click` — drive them with a native `.click()` via eval.

**Deferred to Shawn (Slice 5 copy pass):** a prescriptive "recommended next move" on
the verdict. Kept the verdict computed/honest (names the dominant lever) rather than
scripting advice — that's a copy decision for Shawn.

**Next:** Slice 5 — ship. `/ce:compound` + multi-agent code review; drive findings to
resolution; then deploy (needs Shawn's go-ahead + the store-universe vendoring blocker
resolved — see FAILURES.md); Work-page card; launch blog post draft.

---

## 2026-07-06 — Slice 3 complete: app shell (in-process, no DB)

**Decision (Shawn):** Decompose uses **no database**. Data is the in-process,
seed-locked `cinderhaven-household-panel` package, warmed once at startup. No
psycopg2, no `DATABASE_URL`, no Postgres at request time — this keeps Decompose (and
#4) off the `cinderhaven-db` fragility surface (cred sync, 503 gate, pg health check).
Corrected CLAUDE.md/SPEC/PLAN/app-CLAUDE and superseded the two DB decisions in
DECISIONS.md to match. Memory saved (`no-db-in-process-panel`).

**Did (7 commits, 3A–3F):** Vendored `lailara-palette` + assets; full app stack in
`pyproject.toml`. Built `panel_data.py` (the single data seam: warm_cache, filter
options, exec defaults, metrics/flow pass-throughs, `decompose()` bundle). Cloned the
Spin Rate shell: `app.py` (Dash factory + branded loading overlay), `constants.py`
(tokens + three-lever vocabulary), `lailara_frame.py`, `layout.py` (3 tabs + 4-control
filter bar + as-of/synthetic disclosure + tab-toggle), `filters.py`, `components.py`,
`views/` (which_lever/penetration/detail). `wsgi.py` with **liveness-only** `/health`;
`fly.toml`/`Dockerfile` with no DB secret.

**One output already live end-to-end:** the verdict headline recomputes from the
filters via the tested `panel_data.decompose`. Whole-brand default (2024-Q4→2025-Q4)
lands the punchline: *"Sales rose $1,954 … driven mainly by higher spend per trip."*

**No disk cache** (overrode the "cache to disk" ask, flagged to Shawn): panel gen is
**measured ~0.6s**, already `lru_cached`, and Fly `min_machines_running=1` keeps the
machine up — a parquet cache would save ~0.6s at rare boots and can't be wired without
coupling to the package's internal cache. Warm-at-startup instead. DECISIONS logged.

**State:** **77 tests green** (28 app: 13 decomposition + 11 panel_data + 4 tabs
regression; 49 panel package). Run-verified live: boots clean, `/health` 200, tabs
switch (only active panel shows), no horizontal overflow at 1280px or 375px, no
console errors. Note: env has **Dash 4.2.0** (CLAUDE said 3.x) — clone works on 4.x.

**⚠ Slice 5 deploy blocker (FAILURES.md):** peer pkg `cinderhaven-store-universe`
lives in the doormath repo, not in this build context — the Docker image won't build
until it's vendored into `packages/` (or a private index). Flagged in the Dockerfile.

**Next:** Slice 4 — the real outputs, each reviewed in-slice: three-lever waterfall
chart (shared chart template + the #5 chart rules: automargin, non-dup currency ticks,
bottom legend, bold labels), penetration trend + buyer-flow chart, "which lever"
diagnostic panel / glossary / tooltips, per-period metric cards + ag-grid detail
table. Replace the three `slice4_placeholder` blocks. The loading overlay currently
watches `#main-tabs .custom-tab`; consider re-pointing it at the waterfall chart once
it exists.

---

## 2026-07-06 — Slice 2 complete: decomposition math + verdict

**Did:** Built `app/decomposition.py` — exact **Shapley** three-lever waterfall
(buying households x frequency x spend-per-trip) that reconciles to ΔSales, plus a
direction-aware "which lever" verdict with the honest-hedge threshold. Root app
package + minimal `pyproject.toml` scaffolded (Slice 3 adds the dash/plotly/psycopg2
stack). Also cached `get_transactions` (deterministic) — speeds metrics + app filter
callbacks. Penetration/frequency/spend + buyer flow were already delivered in the
panel package (A5), so Slice 2's remaining work was the waterfall + verdict.

**State:** **62 tests green** (49 panel + 13 decomposition). Reconciliation proven on
2000 random triples + real pairs. Real erosion pair 2024-Q4→2025-Q4: sales +$1,954
"driven mainly by higher spend per trip" while buying households −$2,459 and
frequency −$3,597 — the growth-is-actually-erosion punchline, computed honestly.

**Next:** Slice 3 — clone the Spin Rate app shell (Dash/Plotly, `lailara_frame`,
`lailara-palette`, assets, shared chart template with the #5 chart rules), resilient
`/health` (liveness endpoint for the Fly check + separate DB readiness), branded
loader, `DATABASE_URL` into the synced cred set. This is the visual + DB + deploy
phase — expand root `pyproject.toml` to the full stack here. Deploy (Slice 5) needs
Shawn's explicit go-ahead.

---

## 2026-07-06 — Slice 1 complete: household-panel generator built

**Did:** Built `cinderhaven-household-panel` end-to-end (A1–B), committing each
sub-task: locked constants + 12-quarter calendar (A1); household dimension with
gamma propensity + price-sensitivity + innovator-affinity (A2); per-SKU prices +
2025 price-up path + two launch items (A3); vectorized NB transaction generator with
launch trial/repeat + retailer dimension (A4); period-metrics + buyer-flow accessors
(A5); seeded-story gates (A6); integration/version/README (B).

**State:** **49 tests green.** Panel is deterministic (`SEED=42`), versioned
(v0.1.0), reproducible, importable by #4. Emergent + verified: quarterly erosion
(2024→2025 YoY sales up ~+4%, mean penetration −1.5pp; flat 2023→2024 does not
erode), realism (trips/hh var/mean≈15, skew≈2.3), launch repeat leaky ~14% /
sticky ~52%. New scope folded in per Shawn: #4's two launch stories baked into the
shared panel (burn-in launch, 2023-Q2); retailer dimension added for the app slice.

**Decisions this session:** penetration erosion is a *quarterly* phenomenon (annual
reach saturates) → compare quarters YoY; launches sit in burn-in for #4 runway.

**Next:** Slice 2 — decomposition math: three-lever waterfall (Shapley, reconciles
exactly to ΔSales) + "which lever" verdict with the honest-hedge threshold, built on
`get_period_metrics` / `get_buyer_flow`. Then Slice 3 (clone Spin Rate app shell).

---

## 2026-07-06 — Project initialized + fully spec'd

**Started from:** New project. Brief + brainstorm attached (now in
`docs/brainstorms/`).

**Did:**
- Read prior memory across cinderhaven-db, Spin Rate, Void Finder, doormath;
  summarized carried lessons (DB resilience, don't-touch-cinderhaven-db, design/
  chart rules, shared-package + seed-locking, exec-facing content).
- Locked decisions with Shawn: name=**Decompose**, subdomain
  **decompose.lailarallc.com**, panel = **5,000 households × 12 quarters
  (8 analysis + 4 burn-in)**. Repo **private** (flips public later via /publish).
- Ran the new-project process: workflow state files, hierarchical CLAUDE.md,
  `.gitignore`, README (Lailara standard), full spec (`docs/SPEC.md`), git init +
  GitHub remote.
- Recorded inherited dead-ends in FAILURES.md so they aren't re-discovered.

**State:** Foundation complete. Slice 0 done. No app or panel code yet.

**Blocker/note:** The original folder `decomppose-sales-penetration` (misspelled,
double-p) is pinned open by this session and can't be renamed in place. All work
is in `decompose-sales-penetration`. **Reopen Claude Code in
`decompose-sales-penetration` for the next session**, and delete the empty
misspelled folder from a session not rooted in it.

**Next:** Slice 1 — scaffold `packages/cinderhaven-household-panel` and generate
the seed-locked panel (right-skewed frequencies, burn-in, seeded erosion story),
with canonical/reproducibility + realism unit tests. See PLAN.md.

---
