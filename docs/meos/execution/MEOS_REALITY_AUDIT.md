# MEOS Reality Audit

**Date:** 2026-08-17  
**Method:** Code + tests + scripts inspection (not documentation claims)  
**Overall:** `NOT_READY` → hardening in progress  

Legend: **PASS** · **PARTIAL** · **FAIL** · **MISSING** · **DUPLICATE** · **DEPRECATED**

| Area | Status | Evidence |
|------|--------|----------|
| Backend JWT sign/verify (HS256) | **PASS** | `contexts/identity/infrastructure/security/jwt.py` + `require_permissions` |
| Production Postgres hard gate | **PASS** | `settings._enforce_production_hard_gates` rejects non-postgres |
| Production JWT secret hard gate | **PASS** | rejects default/short secret |
| Production outbox force | **PASS** | `event_bus_mode=direct` → forced `outbox` |
| Postgres outbox repository | **PASS** | `get_outbox_repository()` → Postgres when `use_postgres()` |
| Admin route middleware | **PASS** | Protects `/`, `/modules`, apps; JWT claims + HS256 when secret set |
| Session cookie security | **PARTIAL** | Client-set cookie (Secure on HTTPS); not HttpOnly |
| Default DB URL in production | **PASS** | Rejects empty / `marpich:marpich` credentials |
| Edge JWT signature verify | **PASS** | Web Crypto HS256; required when `NODE_ENV=production` |
| Backup scripts | **PARTIAL** | Scripts exist; `MEOS_REQUIRE_OFFSITE` / production fails without S3 URI |
| Restore drill evidence file | **PARTIAL** | Writes `.last_restore_drill.json` (gitignored); SLO not PASS until real drill |
| Wave smoke scripts 01–05 + healthcare | **PASS** | `scripts/meos-*.sh` present |
| MEOS CI workflows | **PASS** | wave01–05, healthcare, money-path, p3 contracts |
| Application registry YAML | **PARTIAL** | Drift vs nav IDs / empty scaffolds |
| Empty scaffolds honesty | **PASS** | `DEFERRED_CONTEXT_IDS` / `coming_soon` in startup |
| Blueprint API gate | **PASS** | `BLUEPRINT_CONTEXT_IDS` + profile flag |
| Memory persistence in production | **PASS** (blocked) | Hard fail |
| Fake ACTIVE apps | **PASS** (policy) | Registry forbids false ACTIVE |
| Full E2E browser suite | **MISSING** | API smoke loops exist; Playwright E2E incomplete |
| Automated offsite backup cron | **MISSING** | Script only; no scheduler in CI/prod yet |

## P0 open after this audit

1. ~~Edge middleware HS256 verify~~ → **done** (`jwtCookie.ts` + middleware; set `JWT_SECRET` on FE host)
2. ~~Reject weak/default `DATABASE_URL` in production~~ → **done**
3. ~~Require offsite backup when production / `MEOS_REQUIRE_OFFSITE=1`~~ → **done** in script
4. Recorded successful restore drill (ops evidence) — **still open**
5. HttpOnly session cookie via BFF — **still open**
6. Scheduled offsite backup + alerts — **still open**

## Notes

- Prefer **reuse** of Identity / AuthZ / Outbox / Audit — do not fork.
- Docs that conflict with this table must be corrected after code changes.
