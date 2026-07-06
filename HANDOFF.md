# Decompose — Handoff Log

Session-by-session state. Updated by /log mid-session and /wrap at session end.

For durable choices, see DECISIONS.md. For the current arc, see PLAN.md. For
things that didn't work, see FAILURES.md.

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
