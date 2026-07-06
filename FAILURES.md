# Decompose — Failure Log

What was attempted that didn't work, why, and what was tried next. Lower bar than
DECISIONS.md — capture dead-ends so future-you doesn't re-attempt them.

This file is seeded with **inherited dead-ends** from sibling Cinderhaven tools so
they are not re-discovered here.

---

## Entries

### 2026-07-06 — Could not rename the misspelled project folder in place

**Attempted:** `mv` / `Rename-Item` of `decomppose-sales-penetration` →
`decompose-sales-penetration` from within the session.

**Why it didn't work:** The live Claude Code session pins its working directory to
that folder at the OS level (Windows "used by another process" + the shell CWD is
reset back to it after every command). A directory cannot be renamed while it is a
process's CWD.

**What we tried instead:** Created the correctly-named folder and built the whole
project there. The empty misspelled folder must be deleted from a future session
that is not rooted in it.

**Status:** Worked around. **Tags:** windows, folder-rename, cwd-lock

---

### (inherited) cinderhaven-db `pg` health check — PROVEN unrepairable in place

**Attempted (3 prior sessions on cinderhaven-data-platform):** realign
`flypgadmin`'s password via `OPERATOR_PASSWORD`, then `SU_PASSWORD`, then direct
file-based `ALTER ROLE`; verified the DB-level credential is correct and the
checker process has the same value in its own environment.

**Why it didn't work:** The checker still fails auth even though the credential is
provably correct and present in its env — the failure is outside what
`flyctl secrets set` / SQL can reach (cached SCRAM state, different credential
source, or a bug in that postgres-flex build). Cosmetic: does not affect the
app-facing `postgres` role or the 6 downstream apps.

**Do not repeat:** Do not touch `cinderhaven-db` secrets/roles or restart it to
chase this. If ever worth fixing, the scoped path is a fresh Fly Postgres app +
6-app `DATABASE_URL` cutover, with explicit go-ahead — not more credential guessing.
Also: never inline secrets through `flyctl ssh console -C "sh -c \"...$VAR...\""` —
nested shells mangled it to an empty password twice; write SQL to a file and
`sftp put` it.

**Status:** Abandoned (parked). **Tags:** cinderhaven-db, fly, postgres, health-check

---

### (inherited, do-not-clone) Spin Rate `/health` hard-gates the whole site on the DB

**Observed:** Spin Rate's `wsgi.py` `/health` returns `503` when `SELECT 1` fails,
and `fly.toml` points the health check at `/health`. A stale `DATABASE_URL` secret
(DB itself was fine) therefore took the entire external site to 503, not just a
degraded data panel.

**Why it matters here:** This is the exact anti-pattern Decompose must avoid — see
the "resilient health" decision in DECISIONS.md. Do not copy Spin Rate's
`/health`/`fly.toml` health wiring verbatim.

**Status:** Design guardrail. **Tags:** health, fly, resilience, do-not-clone

---

### (inherited) DATABASE_URL secret desync silently breaks Cinderhaven consumer apps

**Observed:** spinrate, ask-cinderhaven, and edi-reconciliation-tool all 503'd on
`password authentication failed for user "postgres"` / `SSL SYSCALL error: EOF`
because their Fly `DATABASE_URL` secrets had drifted from the DB's real `postgres`
password — the DB was fine. Fixed by resyncing each app's secret to the canonical
credential in `cinderhaven-data-platform/.env`, not by touching the DB.

**Do not repeat:** When a Cinderhaven app reports that auth error, check its
`DATABASE_URL` secret against the canonical credential first — don't re-diagnose
the DB. Wire this app's `DATABASE_URL` into the synced set from the start.

**Status:** Resolved (pattern). **Tags:** database-url, secrets, desync, cinderhaven
