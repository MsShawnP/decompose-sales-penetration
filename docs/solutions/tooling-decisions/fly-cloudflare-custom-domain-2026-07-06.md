---
title: Point a Fly.io app at a Cloudflare subdomain (DNS-only CNAME + ACME challenge)
date: 2026-07-06
category: tooling-decisions
module: deploy / DNS (Fly.io + Cloudflare)
problem_type: tooling_decision
component: tooling
severity: medium
applies_when:
  - "Giving a Fly.io app a custom subdomain that is managed in Cloudflare DNS"
  - "The Fly app terminates its own TLS via fly certs, not proxied through Cloudflare"
  - "Automating the DNS record from a script/agent rather than the Cloudflare dashboard"
tags: [fly-io, cloudflare, dns, custom-domain, cname, acme, tls]
related_components: [fly-certs, cloudflare-api]
---

# Point a Fly.io app at a Cloudflare subdomain (DNS-only CNAME + ACME challenge)

## Context
A Fly.io app deploys to `<app>.fly.dev`, but the public URL should be a branded
subdomain (`<sub>.<zone>`) whose DNS lives in Cloudflare. The subdomain needs valid TLS
and must route to the Fly app. Doing this by hand each time is error-prone; the two
easy-to-get-wrong knobs are **proxied vs DNS-only** and **cert validation**.

## Guidance
Use Fly's own cert (not Cloudflare's) and a **DNS-only** CNAME. Steps:

1. Ask Fly what it wants:
   ```bash
   fly certs add   <sub>.<zone>          # provisions the cert
   fly certs setup <sub>.<zone>          # prints the exact records
   ```
   `fly certs setup` gives you a per-app CNAME target `<hash>.<app>.fly.dev` and an ACME
   challenge hostname `<sub>.<zone>.<hash>.flydns.net`.

2. Create **two** CNAMEs in Cloudflare, both `proxied: false` (grey cloud / DNS-only):
   - `<sub>` → `<hash>.<app>.fly.dev`
   - `_acme-challenge.<sub>` → `<sub>.<zone>.<hash>.flydns.net`

3. Poll until issued:
   ```bash
   fly certs check <sub>.<zone>          # Status = Issued
   ```

**Automating the record (Cloudflare API):** create it with a token scoped
`Zone → DNS → Edit` on the zone. Keep that token in a file **outside every git repo**
and read it into a variable — never echo or commit the value. A wrangler OAuth login is
NOT sufficient: it is `zone:read` only and the DNS-records endpoint returns
`Authentication error (code 10000)`.

```bash
TOKEN=$(cat <path-to-dns-token-outside-repo>)     # never printed
curl -s -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  "https://api.cloudflare.com/client/v4/zones/<zone-id>/dns_records" \
  --data '{"type":"CNAME","name":"<sub>.<zone>","content":"<hash>.<app>.fly.dev","proxied":false,"ttl":1}'
```

## Why This Matters
- **DNS-only (grey cloud) is required** for this flow: Fly validates domain ownership and
  terminates TLS directly, so Cloudflare must not proxy. If you proxy (orange cloud),
  Cloudflare terminates TLS instead and Fly needs a `_fly-ownership` TXT record plus an
  origin-SSL config — strictly more moving parts for no benefit on a simple app.
- The `_acme-challenge` CNAME lets the Let's Encrypt cert validate the moment DNS
  propagates, so `fly certs check` flips to `Issued` in a minute instead of waiting on
  traffic.
- Matching one working sibling exactly (rather than improvising) makes every new tool's
  domain setup a 3-step copy job.

## When to Apply
- Any new Fly-hosted tool that needs a branded Cloudflare subdomain.
- Not for apps served *through* Cloudflare's proxy/CDN (that's the TXT-ownership path).

## Examples
Working setup for this project:
`decompose.lailarallc.com` → DNS-only CNAME → `<hash>.decompose-sales-penetration.fly.dev`,
plus `_acme-challenge.decompose` → `decompose.lailarallc.com.<hash>.flydns.net`. Cert
Issued; `https://decompose.lailarallc.com/health` returns `200`. The sibling `doormath`
uses the identical shape.

## Related
- The zone id and the exact DNS-token file path are recorded in the project's private
  session memory (not committed here), since this repo is public.
- See `docs/solutions/architecture-patterns/` for the no-DB / liveness-health decision
  that makes `fly certs`' health check trivial for these apps.
