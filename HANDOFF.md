# Decompose — Handoff Log

Session-by-session state. Updated by /log mid-session and /wrap at session end.

For durable choices, see DECISIONS.md. For the current arc, see PLAN.md. For
things that didn't work, see FAILURES.md.

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
