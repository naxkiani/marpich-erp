# MEOS Security Status

**Date:** 2026-08-18T05:56:36Z · **Principle:** DENY BY DEFAULT  
**P317:** Continuous production assurance **not started** (`TRUST_CRITICAL`). Candidate controls: [MEOS_SECURITY_CONTROL_MATRIX.md](./MEOS_SECURITY_CONTROL_MATRIX.md).

## Strengths

- Backend JWT HS256 sign/verify (`JwtTokenService`) + `require_permissions`
- Production rejects default/short JWT secret and memory persistence
- Production rejects default `marpich:marpich` DATABASE_URL credentials
- Production forces `event_bus_mode=outbox`
- Admin middleware protects `/`, `/modules`, enterprise/banking/education/healthcare/account
- Session cookie stores access JWT HttpOnly via BFF; SPA `sessionStorage` holds tenant metadata only

## Gaps (remaining)

| Issue | Risk | Status |
|-------|------|--------|
| Cookie not HttpOnly (SPA `document.cookie`) | XSS can steal middleware cookie | **CLOSED** — BFF Set-Cookie HttpOnly |
| Access JWT in `sessionStorage` | XSS can steal Bearer token | **CLOSED** — metadata-only storage + `/api/backend` proxy (`meos-session-storage-selftest.mjs`) |
| Edge verify requires env secret on FE host | Misconfig → fail-closed in prod | Documented |
| MFA package deferred | Incomplete auth surface | Deferred / gated |

## Mitigated

| Issue | Mitigation |
|-------|------------|
| Shell search/notify without Bearer | Wave 01 session headers |
| `/` and `/modules` public | Middleware → `/login` |
| Cookie presence-only `=1` | JWT cookie + signature verify |
| Production memory SoR | Hard gate |

## Rules

1. API AuthZ remains source of truth  
2. Middleware is defense-in-depth  
3. Never AuthZ-only-in-UI
