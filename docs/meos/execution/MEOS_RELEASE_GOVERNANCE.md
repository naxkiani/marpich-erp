# MEOS Release Governance

**Date:** 2026-08-18T11:50:00Z  
**CI SoR:** `.github/workflows/meos-*.yml` (GitHub Actions)  
**Change procedure:** [MEOS_CHANGE_MANAGEMENT.md](./MEOS_CHANGE_MANAGEMENT.md) — not in force on production  
**Law:** Do not create a second CI/CD, artifact, or orchestrator platform.

## Gates (P324 numbering → existing evidence)

| Gate | Meaning | Actual |
|------|---------|--------|
| G01 BUILD | Compile / image | **PARTIAL** — CI checkout + pip install; no immutable production image digest |
| G02 UNIT_TEST | pytest unit | **PARTIAL** — Wave 01/02/04/05 jobs exist; not a full suite on this dirty SHA |
| G03 INTEGRATION_TEST | API/Q2C/healthcare scripts in CI | **PARTIAL** — workflow files exist; this host is not a certified green immutable run |
| G04 E2E_TEST | Playwright UI | **FAIL** (P313 G20) |
| G05 CONTRACT_TEST | OpenAPI + events + plugin manifest + release honesty | **IMPLEMENTED** in pytest; some event files remain payload-only |
| G06 SECURITY | Secrets, auth, dependency CVE | Auth tests exist; secret manager / container scan **NOT_AVAILABLE** |
| G07 TENANT_ISOLATION | Cross-tenant tests | **TESTED** memory (CRM, plugins) — not production |
| G08 DATABASE | Postgres ready | Workstation `:5433` historically; **not** production |
| G09 MIGRATION | `scripts/run-migrations.sh` | **IMPLEMENTED** (idempotent versions); destructive-prod rollback **NOT_EXERCISED** |
| G10 PERFORMANCE | Baseline script | Workstation p95 in P313 — not soak |
| G11 OBSERVABILITY | Health + OTel | Health endpoints exist; alerting **FAIL** (G23) |
| G12 BACKUP | `meos-postgres-backup.sh` | Drill PASS historically (P313 G07); not production cluster |
| G13 ROLLBACK | Live release rollback | **BLOCKED** (G27) |
| G14 DOCUMENTATION | This set + P313–P323 | **IMPLEMENTED** |

A release **must not** skip G06/G07/G13/G26-equivalent for PRODUCTION_RELEASE.

## Security gate (critical blocks)

Critical: missing production cluster (G26), dirty SHA (G25), TRUST_CRITICAL.  
Plugin pack/sign/publish CLI **exit 2** (P323).  
Dependency CVE scan in CI: **NOT_EVIDENCED**.

## API / event releases

- API: `/api/v1` only; breaking path changes require ADR + `test_openapi_contract.py`.  
- Events: versioned JSON under `docs/architecture/events/`; envelope required. Payload-only legacy files must not be treated as full-envelope certification.

## Extension releases (P322/P323)

```
DEVELOP → VALIDATE manifest → TEST → SECURITY_SCAN → CERTIFY → PUBLISH → INSTALL → ENABLE
```

CERTIFY/PUBLISH production path: **NOT_AVAILABLE**. Install ≠ activate.

## Feature flags

`POST /api/v1/feature-flags/evaluate` exists (canary/emergency-disable in catalog). **Not** a substitute for G26/G13. Production tenant canary of MEOS itself: **NOT_AVAILABLE**.

## Emergency release

[MEOS_CHANGE_MANAGEMENT.md](./MEOS_CHANGE_MANAGEMENT.md) EMERGENCY category still requires SHA, audit, rollback plan. Emergency ≠ uncontrolled. **Not in force** until production exists.

## Promotion

`LOCAL → TEST (CI) → STAGING → CERTIFICATION → PRODUCTION`  
Only LOCAL and CI TEST are evidenced. Promotions to PRODUCTION: **forbidden** until P313 P0=0 and P314 GO_LIVE APPROVED.
