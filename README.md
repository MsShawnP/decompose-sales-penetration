# Decompose

**Splits a brand's sales change into the only three levers that can move it — and says which one to pull next.**

**Live:** https://decompose.lailarallc.com

## What it does

Sales went up. That tells you nothing about *why*. Decompose takes a brand's
period-over-period sales change and decomposes it into the three components
that fully explain it, reconciling exactly back to the sales delta:

- **Household penetration %** — buying households ÷ total panel households, per period.
- **Purchase frequency** — trips per buying household per period.
- **Spend per trip** — further split into units/trip × price/unit.
- **Three-lever waterfall** — bridges period-A sales to period-B sales across the
  three levers; reconciles exactly to the sales delta.
- **Buyer flow** — new / retained / lapsed buyer counts behind the penetration number.
- **"Which lever" verdict** — the plain-language paragraph that goes into a board deck.

The demo has a deliberate story seeded into the panel: a stretch where sales grow
on price increases while household penetration quietly declines — "growth that's
actually erosion."

## Why it matters

Household penetration — the % of households that bought the brand at least once
in a period — is the Byron Sharp / *How Brands Grow* growth metric, and the one
most POS dashboards can't show because it needs panel data, not scan data. A
brand can post growing revenue while its buyer base shrinks; Decompose surfaces
that distinction before it shows up as a cliff, and tells leadership which of
the three levers actually moved the number.

Built on the Cinderhaven synthetic dataset — a ~$25M specialty food brand, 50
SKUs across 5 product lines and 6 contracted retailers. Data is synthetic;
methodology and deliverables are real. Decompose adds a synthetic **household
panel** (household × transaction × item × date × spend) on top of the shared
universe, shipped as a versioned, seed-locked package so downstream tools reuse
the identical panel.

## Quick start

No database or credentials required — the panel is generated in-process at
startup and cached.

```bash
# Install the vendored packages first (local, not on PyPI), then the app
pip install ./packages/lailara-palette \
            ./packages/cinderhaven-store-universe \
            ./packages/cinderhaven-household-panel
pip install -e ".[dev]"

python wsgi.py    # serves on http://127.0.0.1:8050
pytest            # app suite (charts, views, decomposition, data seam)
```

Or with Docker:

```bash
docker build -t decompose .
docker run -p 8050:8050 decompose
```

## Tech stack

- Python 3.11
- Dash + Plotly (dash-ag-grid for tables, clientside JS callbacks)
- pandas, numpy, pyarrow (parquet disk-cache for the generated panel)
- **No database.** Data is the in-process, seed-locked `cinderhaven-household-panel`
  package — generated once at startup, cached, and reused. Health check is
  liveness-only, so a data issue can never pull the machine from the proxy.
- Gunicorn + Docker + Fly.io (`iad`)

## Project structure

```
app/          Dash app: layout, views, charts, decomposition math, panel access
packages/     Vendored, seed-locked data packages (store universe, household panel, palette)
assets/       CSS, fonts, clientside JS
docs/         SPEC.md and design notes
tests/        pytest suite
wsgi.py       Entry point: Flask/Dash server + /health liveness route
```

## Data contract

**Canonical baseline:** 50 SKUs · 5 product lines (AS·PS·SC·DG·SB) · 6 retailers
(Walmart·Costco·Whole Foods·Sprouts·Kroger·Regional Group). The household panel
is a new, additive asset aligned to this universe; its own figures are locked and
versioned at generation time and do not alter any existing canonical figure.

## License

MIT

---

Built by [Lailara LLC](https://lailarallc.com) — data hygiene and analytics
consulting for specialty food brands scaling into national retail.
