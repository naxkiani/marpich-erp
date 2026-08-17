# MEOS Security Status

**Date:** 2026-08-17 · **Principle:** DENY BY DEFAULT

## Strengths

- Backend JWT HS256 sign/verify (`JwtTokenService`) + `require_permissions`
- Production rejects default/short JWT secret and memory persistence
- Production rejects default `marpich:marpich` DATABASE_URL credentials
- Production forces `event_bus_mode=outbox`
- Admin middleware protects `/`, `/modules`, enterprise/banking/education/healthcare/account
- Session cookie stores access JWT; middleware validates claims + **HS256** when `JWT_SECRET` / `MARPICH_JWT_SECRET` is set (required in `NODE_ENV=production`)

## Gaps (remaining)

| Issue | Risk | Status |
|-------|------|--------|
| Cookie not HttpOnly (SPA `document.cookie`) | XSS can steal token | **OPEN** — needs BFF Set-Cookie |
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
