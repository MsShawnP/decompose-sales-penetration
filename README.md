# Decompose

**Live:** https://decompose.lailarallc.com <!-- not yet deployed -->

Sales went up. That tells you nothing about *why*. Decompose splits a brand's
period-over-period sales change into the only three things that can move it —
more households buying, existing buyers buying more often, or buyers spending
more per trip — and reconciles the three back to the exact sales delta. It then
says, in plain language, which lever moved the number and which one to pull next.

This is household penetration: the % of households that bought the brand at least
once in a period — the Byron Sharp / *How Brands Grow* metric, and the one most
POS dashboards can't show because it needs panel data, not scan data.

## Cinderhaven context

Built on the Cinderhaven synthetic dataset — a ~$25M specialty food brand, 50
SKUs across 5 product lines and 6 contracted retailers. Data is synthetic;
methodology and deliverables are real. Decompose adds a new synthetic **household
panel** (household × transaction × item × date × spend) on top of the shared
universe, shipped as a versioned, seed-locked package so tool #4 (Leaky Bucket)
reuses the identical panel.

## What it does

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

## Stack

- Python 3.11
- Dash 3.x + Plotly 6.0 (dash-ag-grid for tables, clientside JS callbacks)
- pandas 2.x, numpy, psycopg2
- Postgres (Cinderhaven SSOT, `cinderhaven-db`)
- Gunicorn + Docker + Fly.io (`iad`)

## Data contract

**Canonical baseline:** 50 SKUs · 5 product lines (AS·PS·SC·DG·SB) · 6 retailers
(Walmart·Costco·Whole Foods·Sprouts·Kroger·Regional Group). The household panel
is a new, additive asset aligned to this universe; its own figures are locked and
versioned at generation time and do not alter any existing canonical figure.

## Run

```
# Local: native PG16 on port 5433, or proxy cinderhaven-db on 127.0.0.1:15432
pip install -e .
python wsgi.py   # serves on http://127.0.0.1:8050
```

---

Built by [Lailara LLC](https://lailarallc.com) — data hygiene and analytics
consulting for specialty food brands scaling into national retail.
