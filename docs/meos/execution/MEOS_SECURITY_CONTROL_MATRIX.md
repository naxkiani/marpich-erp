# MEOS Security Control Matrix

**Date:** 2026-08-18T05:56:36Z · **P328:** effectiveness overlay [MEOS_CONTROL_EFFECTIVENESS.md](./MEOS_CONTROL_EFFECTIVENESS.md). Production **EFFECTIVE** count remains **0**.  
**Scope:** Candidate codebase + P313 tests. **Not** a production continuous-monitoring matrix.  
**States:** IMPLEMENTED · VERIFIED · MONITORED · GAP · NOT_APPLICABLE · NOT_AVAILABLE

| Control | Classification | Evidence |
|---------|----------------|----------|
| Authentication (JWT HS256, exp, iss, type) | VERIFIED (candidate) | P313 G02; `test_jwt_token_service.py` |
| Session / HttpOnly BFF cookie | VERIFIED (candidate) | P313 G01; sessionStorage selftest |
| Authorization (`require_permissions`, PDP allow/deny) | VERIFIED (candidate) | P313 G03 |
| Tenant isolation (CRM cross-tenant deny) | VERIFIED (candidate) | P313 G04 |
| Public API protection (401 without token) | VERIFIED (candidate) | P313 G01 live 401s |
| Production settings (no default JWT, no memory SoR, no default DB creds) | VERIFIED (config) | `test_production_settings_gates.py` |
| Secrets in git | GAP / NOT_AVAILABLE | Must not commit prod secrets; `.env.meos-prod` gitignored — production store **NOT_AVAILABLE** |
| Encryption at rest (production) | NOT_AVAILABLE | No production disk/KMS evidence |
| TLS public CA | GAP | P313 G26 BLOCKED (self-signed / none in prod) |
| Rate limiting | NOT_AVAILABLE | Not production-verified this program |
| Audit of mutations | VERIFIED (candidate) | P313 G17 Wave 01 |
| Security event monitoring (production) | NOT_AVAILABLE | P313 G23 FAIL |
| Privileged-access review (production) | NOT_AVAILABLE | No production IdP/access recertification |
| Dependency CVE program | NOT_AVAILABLE | No inventory run claimed this phase |
| AI safety (governed provider) | GAP | P313 G18 FAIL (template echo) |
| Privacy DSAR / erasure runtime | GAP | P313 G19 FAIL |
| Backup protection (production cluster) | NOT_AVAILABLE | Host MinIO drill ≠ production backup security |
| Autonomous remediation | NOT_APPLICABLE | Disabled (P316) |

MONITORED in production: **none** — `PRODUCTION_ACTIVE` is false.
