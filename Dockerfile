FROM python:3.11-slim AS base

WORKDIR /app

# Vendored + peer packages first (they change less often than app code).
COPY packages/ /app/packages/
RUN pip install --no-cache-dir /app/packages/lailara-palette/ \
 && pip install --no-cache-dir /app/packages/cinderhaven-household-panel/

# ── SLICE 5 DEPLOY BLOCKER ───────────────────────────────────────────────────
# cinderhaven-household-panel requires the peer package cinderhaven-store-universe,
# which currently lives in the doormath repo
# (doormath-sales-penetration/packages/cinderhaven-store-universe) and is NOT in
# this build context. The install above will fail to resolve it until it is made
# available — vendor it into packages/ (like lailara-palette) or install from a
# private index. This is a pre-deploy task; deploy itself is gated on Shawn.
# Tracked in HANDOFF.md / FAILURES.md.
# ─────────────────────────────────────────────────────────────────────────────

# Install app dependencies (the two local packages above already satisfy their pins).
COPY pyproject.toml /app/
RUN pip install --no-cache-dir .

# Copy application code
COPY app/ /app/app/
COPY assets/ /app/assets/
COPY wsgi.py /app/

EXPOSE 8050

# No DATABASE_URL — Decompose has no database. Each gunicorn worker warms its own
# in-process panel copy at boot (~0.6s), then serves everything from cache.
CMD ["gunicorn", "wsgi:server", "--bind", "0.0.0.0:8050", "--workers", "2", "--timeout", "120"]
