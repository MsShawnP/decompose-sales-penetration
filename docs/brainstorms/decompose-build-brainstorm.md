# Household Penetration Decomposition — Build Brainstorm (Tool #3 of 5)

**Working title:** `decompose` (alts: `threelever`, `buyersplit`)
**Series status:** #1 Door Math live · #2 Spin Rate live · **#3 = this doc** ·
#4 Leaky Bucket (shares this tool's panel) · #5 Void Finder (scoped)
**Pairing:** #3 and #4 are a matched pair built against ONE shared household panel.
Build #3 first (it creates the panel), then #4 reuses it. Do not build them apart.

---

## Business question

> "Did sales move because more households bought us, because existing buyers bought
> more often, or because they spent more per trip — and which lever should we pull
> next?"

The decomposition: **Sales = households buying × purchase frequency × spend per trip.**
Each term is a different strategy. New-buyer growth means trial drivers (display,
sampling, distribution). Frequency growth means usage occasions and reminders.
Spend-per-trip growth means pack architecture and trade-up. A brand that can't
decompose its growth literally cannot tell whether its *marketing* or its
*merchandising* is working.

## Why this one matters conceptually — and it's already teed up

This is the *other* meaning of "penetration" — **household** penetration, the % of
households that bought the brand at least once in a period. It's the Byron Sharp /
*How Brands Grow* metric, and it's what the more sophisticated CEOs mean.

**Direct continuity with what's already live:** the anchor blog post published
2026-07-01 ("Penetration Means Three Things…") explicitly names household penetration
as *Meaning #3 — "the one your dashboard isn't showing you"* and tells readers to get
in touch to know when it's live. **This tool is the payoff to a promise already on the
site.** Its launch post writes itself: it's the "here's the one" reveal.

## The disambiguation job

Tool #1 is *shelf* penetration; this is *buyer* penetration. Conflating them produces
bad strategy, and that contrast is the spine of the series. This tool exists partly to
make the distinction concrete.

---

## The big new build: a synthetic household panel

This is the largest new data asset of the series (Door Math/Spin Rate/Void Finder all
share the POS/store universe; this needs something different).

- **Grain:** household ID × transaction × item × date × spend
- **This is PANEL data, not POS** — a meaningful distinction worth explaining in the
  writeup, since most small brands have POS and no panel (Numerator/Circana territory).
- **Size:** ~5,000 households (lock the number + period count before generating).
- **Realism bar:** purchase-incidence and frequency distributions must be heavily
  right-skewed (negative-binomial-ish). If they look uniform/toy, anyone who's seen
  real panel output dismisses the demo instantly.
- **Lock the seeds** the way CINDERHAVEN_CANONICAL locks figures — this panel is
  shared with tool #4, so it must be reproducible and versioned, not regenerated
  per run.

## Core metrics

- **Household penetration %** — buying households ÷ total households in panel
- **Purchase frequency** — trips per buying household per period
- **Spend per trip** (decompose further into units/trip × price/unit)
- **Period-over-period bridge** — waterfall attributing the sales delta to each lever
- **New vs. lapsed vs. retained buyer counts** — the flow behind the penetration number

## Outputs

- **Three-lever waterfall chart** bridging period-A sales to period-B sales
- **Penetration trend** with buyer-flow decomposition (new / retained / lapsed)
- **"Which lever" diagnostic** in plain language — the paragraph that goes straight
  into a board deck

## Cinderhaven angle (seed the punchline)

Build a deliberate story into the panel: a period where **sales grew on price
increases while household penetration quietly declined** — the classic
"growth that's actually erosion" trap. That seeded story is the demo's punchline and
maps exactly to the trap called out in the anchor blog post.

---

## Proposed stack — mirror Spin Rate (proven, deployed)

- **App:** Dash 3.x, Plotly 6.0, Python 3.11
- **Data:** pandas 2.x, numpy, psycopg2 → Cinderhaven SSOT Postgres (`cinderhaven-db`).
  The household panel becomes new tables in the same SSOT.
- **UI:** dash-ag-grid where tabular; clientside JS callbacks
- **Deploy:** Gunicorn + Docker + Fly.io (shared-cpu-1x, `iad`)
- **Subdomain:** `decompose.lailarallc.com` (or threelever/buyersplit — pick before
  deploy so repo name and subdomain match)

## Bake in the #1/#2 lessons (don't relearn)

1. **Do NOT hard-gate `/health` on the DB** — serve branded shell + "data temporarily
   unavailable" if the DB is down; keep a separate readiness signal. (This is the exact
   bug that took Spin Rate dark.)
2. **DB creds:** wire `DATABASE_URL` into the synced cred set (canonical creds in
   `cinderhaven-data-platform/.env`, gitignored) so this app never repeats the desync.
3. **Branded pre-hydration loading state** — no blank white first paint on a cold link.
4. **Test rigor to Spin Rate's bar** (138 tests green). Unit-test the decomposition
   math hard — the waterfall must reconcile exactly to the sales delta, or the whole
   tool is suspect.

## Panel-generator packaging (resolve before coding)

The panel is shared with tool #4. Build it as a **standalone, versioned generator
module/package** (e.g. `cinderhaven-household-panel`) that BOTH #3 and #4 import — the
same way #5 should share Door Math's store universe. Lock seeds; treat the generated
panel as canonical.

---

## Open decisions for Shawn

1. **Name/subdomain:** decompose vs. threelever vs. buyersplit.
2. **Panel size / period count** — needs to be fixed before generation (suggest ~5,000
   households, enough periods to show a multi-quarter penetration decline).
3. **Panel realism source:** hand-tuned negative-binomial parameters, or fit to a
   public reference shape? (Hand-tuned is fine if the skew reads real.)
4. **Launch post:** publish the "here's the one your dashboard isn't showing you"
   reveal as its own post, or add it as the capstone to the penetration series?

## Suggested session plan

1. Design + build the shared household panel generator; lock seeds; version it.
2. Seed the "growth that's actually erosion" story into the panel.
3. Build the decomposition math (households × frequency × spend/trip) + the buyer-flow
   (new/retained/lapsed); unit-test that the waterfall reconciles to the sales delta.
4. Build the three outputs (waterfall, penetration+flow trend, plain-language verdict).
5. Wrap in the Spin Rate app shell (Dash/Plotly, branded loader, resilient /health).
6. Deploy to Fly.io + subdomain + DATABASE_URL into the synced cred set.
7. Work-page card (same format as Door Math / Spin Rate) + the reveal blog post.
8. HANDOFF.md + tests green before done. **Leave the panel generator ready for #4.**

## What to pull from source at build time

- The CINDERHAVEN_CANONICAL locking pattern (so the panel is versioned/reproducible
  like the existing canonical figures).
- Spin Rate's app shell / `wsgi.py` health contract to clone the resilient-`/health`
  and branded-loader setup.
