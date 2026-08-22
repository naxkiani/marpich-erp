# MEOS Hardening Report (P311)

**Date:** 2026-08-17 · **Status:** `NOT_READY`  
**Do not treat as RELEASE_CANDIDATE.**

## 1. Already complete (re-verified)

- Production settings: Postgres required; default JWT rejected; `marpich:marpich` DATABASE_URL rejected; outbox forced  
- Edge cookie: JWT shape/exp + HS256 when `JWT_SECRET` set (`NODE_ENV=production` requireSignature)  
- Backup/restore **scripts** exist and fail closed without Postgres/offsite in production  
- Registry YAML includes nav IDs + empty scaffolds + blueprints (contract tests)

## 2. Verified this run

- JWT cookie selftest PASS  
- Settings + registry + in-process event fabric PASS  
- Backup/restore **execution** FAIL (no Postgres listener)

## 3. Fixed this slice

- Backend `JwtTokenService` now verifies **issuer** + require `exp`/`iat`  
- Unit tests: valid, tampered, expired, wrong issuer, refresh-as-access  
- Post-hardening verification document

## 4. Remains

See P0/P1 in [MEOS_POST_HARDENING_VERIFICATION.md](./MEOS_POST_HARDENING_VERIFICATION.md).

## 5–6. P0 / P1 remaining

P0: live DR, Postgres outbox E2E, HttpOnly cookie  
P1: AuthZ matrix, tenant negatives, Functional loops on live API, merge PR #16

## 7. Tests executed

14 passed, 2 skipped (outbox postgres) + 5 registry + 6 JWT unit (this commit)

## 8–9. Backup / restore

**BLOCKED** — `127.0.0.1:5432` and `:5433` no response. Not PASS.

## 10. Security

API JWT: **PASS** (unit). Session cookie HttpOnly: **FAIL/open**. Middleware ≠ API security.

## 11. E2E

**BLOCKED** — no running API/DB this host.

## 12. UI/UX

**PARTIAL** — KpiStrip/home pulse on feature branch; visual gate not measured.

## 13. Production build

**NOT RUN** this verification.

## 14. Deployment

**PARTIAL** — compose/runbooks exist; production deploy not proven.

## 15. Final readiness

**`NOT_READY`**
