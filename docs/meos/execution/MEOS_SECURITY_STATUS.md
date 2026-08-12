# MEOS Security Status

**Date:** 2026-08-12 · **Principle:** DENY BY DEFAULT

## Strengths

- JWT login / refresh / logout in Identity  
- `require_permissions` on many routes  
- Tenant header `X-Tenant-ID` expected by APIs  
- Authorization check API exists  

## Gaps (P0)

| Issue | Risk |
|-------|------|
| Shell search/notify without Bearer | Unauth calls / silent failure → false UX |
| `/` and `/modules` public | Unauthenticated platform surface |
| Default memory persistence | Session/data loss; weak multi-tenant durability |
| Missing MFA package still referenced | Incomplete auth surface |
| Cookie session is presence-only | Middleware does not validate JWT |

## Wave 01 mitigations

1. Platform session headers from `marpich_auth_session`  
2. Protect home/modules  
3. Postgres runbook for durable Wave 01 cores  
4. Gate missing MFA/security routers until packages exist  
5. Keep server-side permission checks; never AuthZ-only-in-UI
