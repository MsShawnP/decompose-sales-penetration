# Decompose (Tool #3) — Fable / Claude Code build brief

Paste to Claude Code. Attach `decompose-build-brainstorm.md`. This brief front-loads
every lesson learned across the Spin Rate (#2) and Void Finder (#5) builds so we don't
relearn any of them.

```
Build Decompose — tool #3 of the Cinderhaven sales-penetration series (Household
Penetration Decomposition). Full brainstorm is attached; this brief is the actionable
summary plus the accumulated lessons.

STEP 0 — READ YOUR OWN MEMORY FIRST
Before writing code, load and re-read the relevant Claude memory files from prior
sessions in this project, including at minimum:
  - the cinderhaven-db infra memory + cinderhaven-db-pg-health-check-blocked.md
  - the Void Finder and Spin Rate HANDOFF / FAILURES notes
  - any design-system and chart-config notes
Summarize back to me what lessons you're carrying in before you start. Do not
rediscover things we already solved.

WHAT IT IS
"Did sales move because more households bought us, because they bought more often, or
because they spent more per trip — and which lever do we pull next?" Decomposes
Sales = households buying x purchase frequency x spend per trip, plus household
penetration % and new/retained/lapsed buyer flow. This is the payoff to the live blog
post ("Penetration Means Three Things") which promised household penetration as the
metric your dashboard isn't showing.

BUILD AS A PAIR WITH #4
#3 builds the shared synthetic HOUSEHOLD PANEL; #4 (Leaky Bucket) reuses it. Build the
panel as a standalone, versioned, seed-locked generator package (e.g.
cinderhaven-household-panel) the way doormath ships cinderhaven-store-universe — so #4
imports it, no second copy. Include a BURN-IN period in the panel timeline now (#4's
trial/repeat needs history runway before the analysis window); retrofitting later is
expensive. ~5,000 households, right-skewed (negative-binomial-ish) frequencies, locked
seeds like CINDERHAVEN_CANONICAL. Seed the punchline: a period where sales rise on
price while household penetration quietly declines ("growth that's actually erosion").

METRICS / OUTPUTS
Household penetration %, purchase frequency, spend per trip; a three-lever
period-over-period waterfall that MUST reconcile exactly to the sales delta (unit-test
this); new/retained/lapsed buyer decomposition; a plain-language "which lever" verdict.

=== LESSONS LEARNED — APPLY ALL OF THESE FROM DAY ONE ===

DATABASE (from the #2 outage + #5):
- Do NOT hard-gate /health on the DB. Serve the branded shell + "data temporarily
  unavailable" on DB outage; keep a SEPARATE readiness signal. This is the exact bug
  that took Spin Rate to an external 503.
- Wire DATABASE_URL into the SYNCED credential set (canonical creds in
  cinderhaven-data-platform/.env, gitignored) so this app never repeats the cred
  desync. New panel tables live in the same cinderhaven-db SSOT.
- Do NOT touch cinderhaven-db internals (the parked pg / flypgadmin health-check issue)
  without a separate explicit go-ahead. Don't restart that machine casually.

DESIGN (from the #5 "looks unprofessional" pass):
- Apply LAILARA_DESIGN_SYSTEM.md and REUSE Spin Rate's actual design tokens, layout
  components, header/footer chrome — don't rebuild from scratch. The two tools should
  come out visually identical by construction. Serif headings, brand navy/burgundy,
  logo + link back to lailarallc.com + matching footer.
- Filter row: one tidy grid, equal-width controls, labels aligned on a common baseline
  (uniform label min-height) so no control floats above the others. Don't let long
  labels wrap and shove their control down.
- Stat cards: real cards with hierarchy — the primary numbers emphasized (top border /
  larger), secondary counts muted.

CHARTS (hard-won on #5 — put ALL of this in the SHARED chart template, then verify
every chart individually):
- Category-axis labels must not clip. Set automargin=True / adequate margins so the
  LONGEST label renders in full. (We shipped "5moky…", "lmond…" — never again.)
- Currency tick formatter must show each tick's TRUE value, evenly spaced, NO
  duplicates. We shipped axes reading "$100k, $100k, $200k, $200k" — the abbreviation
  was rounding adjacent ticks to the same label. Fix dtick + formatter; extend axis max
  past the largest value.
- Legends go at the BOTTOM (horizontal), with enough margin that they never overlap a
  bar. Top legends got overwritten by tall bars.
- Bar charts: bold value data labels, formatted ($ for dollars, ints for counts), not
  clipped at the edge.
- After building, click/inspect EVERY chart and confirm: no clipped labels, no
  duplicate/misrounded ticks, no legend overlap.

TABS (regression from the #5 design pass):
- Tab switching must render each tab's DISTINCT content. A CSS/markup refactor once
  disconnected the tab-content callback so every tab showed the default body. Add a
  regression test asserting each tab renders its own content so a future style change
  can't silently break it.

TABLES/GRIDS (from #5):
- Never truncate the key identifier column (rows looked identical because the ID was
  cut off). Give headers room or short clear labels. Show scores as % or High/Med/Low,
  not raw decimals. Label/clarify any computed column (tooltip).

EXEC-FACING CONTENT (from the #5 CEO/CFO passes) — this tool is CEO/CFO-facing too:
- Lead with a big headline number in plain language a CFO can't misread. We learned
  "sitting in stores" read as inventory and "already won" was too implicit — say the
  plain thing.
- LABEL every number with its timeframe. We shipped a figure tooltipped "annual" that
  was actually cumulative-to-date — a credibility bug. State the period; if there's an
  as-of/measurement date, show it and make it selectable if useful.
- Tooltips on every metric and filter; a short "why this matters" panel; a glossary;
  keep the synthetic-data disclosure on the page.
- I (Shawn) will want to review the copy — draft it but expect a copy pass; keep the
  Cinderhaven synthetic figure and methodology honest.

DATA MODEL / CANONICAL:
- Reuse shared packages, don't duplicate (the cinderhaven-store-universe pattern). Lock
  the panel seeds and version them. If anything would shift doormath's or the series'
  locked canonical figures, that's the change protocol + a canonical-figures impact
  check + my explicit approval — do NOT change locked figures silently.

=== PROCESS — DO NOT SKIP ===
- Run /ce:compound and the multi-agent code review before calling anything done; drive
  findings to resolution (Spin Rate shipped after "22 findings resolved, 138 tests
  green" — match that bar).
- Write HANDOFF.md and FAILURES.md. Save a memory capturing what was built, decisions,
  and any dead ends so the next session doesn't repeat them.
- Tests green before done, including the waterfall-reconciliation and panel-realism
  checks.

DELIVERABLES
- Versioned cinderhaven-household-panel generator (with burn-in), the Decompose app on
  the Spin Rate stack, deployed to a subdomain (default decompose.lailarallc.com),
  Work-page card in the Door Math / Spin Rate format, and the launch/reveal blog post
  draft ("here's the one your dashboard isn't showing you").

CONFIRM WITH ME before deploy: (1) name/subdomain, (2) panel size/period count,
(3) anything that touches locked canonical figures. Report the compound-review result
and tests before you consider it done.
```
