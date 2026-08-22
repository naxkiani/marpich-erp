# MEOS API Governance

**Date:** 2026-08-18T06:51:00Z  
**Surface:** `/api/v1` · OpenAPI at gateway `/openapi.json`

## Versioning

| Item | Actual |
|------|--------|
| CURRENT_VERSION | **v1** (`/api/v1`) |
| SUPPORTED_VERSIONS | v1 only (evidenced) |
| DEPRECATED_VERSIONS | **none documented** |
| MIGRATION_PATH | Breaking changes require ADR + OpenAPI path update (`test_openapi_contract.py`) |

Do not introduce `/api/v2` in this phase.

## Pipeline (intended = implementation pattern)

```
REQUEST → VALIDATION (Pydantic) → AUTHZ (require_permissions) → BUSINESS LOGIC
  → DATABASE/EVENT (outbox) → RESPONSE envelope → AUDIT (events)
```

Gateway middleware: request ID, duration log, tenant header fail-fast on `/api/v1` (with exemptions). **Rate limiting in this middleware: NOT_IMPLEMENTED.** Architecture doc assigns rate limit to gateway — gap vs code; **do not build a second gateway**.

## Checks

| Concern | Status |
|---------|--------|
| Authentication | JWT on business APIs; `/auth/*` `/health` public |
| Authorization | Permission dependencies |
| Tenant | `X-Tenant-ID`; must not trust unauthenticated body tenant |
| Validation | Pydantic schemas |
| Idempotency | Event consumer keys; financial journal keys; HTTP idempotency **not universal** |
| Audit | Integration events → audit consumer |
| Observability | OTel bootstrap exists; production **NOT_AVAILABLE** |
| Documentation | OpenAPI generated from routers |

## Contract tests

`backend/tests/contracts/test_openapi_contract.py` requires listed platform paths. Not a full partner Pact suite.
