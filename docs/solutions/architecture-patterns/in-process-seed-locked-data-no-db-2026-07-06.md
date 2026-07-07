---
title: Serve a deterministic seed-locked dataset in-process instead of a database
date: 2026-07-06
category: architecture-patterns
module: app/panel_data.py (data seam) + wsgi.py (health)
problem_type: architecture_pattern
component: service_object
severity: medium
applies_when:
  - "The app's data is synthetic/deterministic, generated from a locked seed, not user-supplied"
  - "Generation is cheap (sub-second) and the dataset fits comfortably in memory"
  - "You want to avoid a shared database's operational fragility (cred sync, health-gate outages)"
tags: [architecture, in-process-data, no-database, health-check, liveness, fly-io, dash]
related_components: [panel-data-seam, health-endpoint]
---

# Serve a deterministic seed-locked dataset in-process instead of a database

## Context
This tool needed a 5,000-household × 12-quarter panel. The series' shared Postgres has a
history of operational fragility: credential desync across apps, and a health-check bug
where `/health` returned 503 when the DB was down while `fly.toml` checked `/health` —
which pulled *both* machines from the proxy and 503'd the whole site externally. The
panel data is fully deterministic and seed-locked, so it never actually needed a
database at request time.

## Guidance
Ship the dataset as an **in-process, versioned, seed-locked package**. The app imports
it, warms it once at startup, and serves everything from memory — no `psycopg2`, no
`DATABASE_URL`, no Postgres on the request path.

```python
# app/panel_data.py — the single data seam every view imports
import cinderhaven_household_panel as panel   # deterministic, SEED-locked, versioned

_warmed = False
def warm_cache() -> None:
    """Build the panel once at startup so no request pays generation (~0.6s, lru_cached)."""
    global _warmed
    if _warmed:
        return
    panel.get_transactions()   # first call builds; all downstream reads reuse the cache
    _warmed = True
```

Make the health check **liveness-only** — there is no DB to degrade, so a 200 means "the
process is up," and nothing can 503 for a data reason:

```python
@server.route("/health")
def health():
    return jsonify(status="ok"), 200     # no readiness/DB gate; fly.toml checks this
```

## Why This Matters
- **Designs the outage bug out, not around.** With no request-path DB, the Spin Rate
  503-gate failure literally cannot happen — there is no readiness endpoint and no
  DB-status branch to misfire.
- **Off the fragility surface entirely.** No credential sync, no dependence on the
  (unrepairable) shared-DB `pg` health check, no `DATABASE_URL` secret to desync.
- **A DB copy would only duplicate canonical data.** The data is deterministic; persisting
  it to Postgres just creates a second, drift-prone copy of the same seed output.
- **No disk cache needed** (measured, not assumed): generation is ~0.6s, already
  `functools.lru_cache`d per process, and with Fly `min_machines_running = 1` the machine
  stays up — so the cost is paid once at boot. A parquet cache would save ~0.6s at rare
  boots and couldn't be wired without coupling to the package's internal cache.

## When to Apply
- Deterministic or synthetic datasets that fit in memory (demos, seed-locked panels,
  shared canonical datasets reused across sibling tools).
- **Not** for user-supplied, mutable, or large data — that still wants a database.

## Examples
- **Anti-pattern (what this replaces):** `/health` returns 503 on DB-down + `fly.toml`
  health-checks `/health` → a transient DB blip pulls every machine from the proxy →
  full external outage.
- **This app:** `warm_cache()` builds the panel once at import; `/health` always returns
  `200`; the same in-process package is imported unchanged by the next tool in the series
  (no second copy).

## Related
- `docs/solutions/tooling-decisions/` — the Fly + Cloudflare custom-domain setup, whose
  cert health check is trivial precisely because `/health` is liveness-only.
