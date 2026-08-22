# MEOS Architecture Drift Report

**Date:** 2026-08-19T06:15:00Z  
**Supersedes stale counts in** [MEOS_ARCHITECTURE_STATUS.md](./MEOS_ARCHITECTURE_STATUS.md) (2026-08-12 empty-scaffold list).  
**Companion (older productization):** [docs/productization/MEOS_ARCHITECTURE_GAP_REPORT.md](../../productization/MEOS_ARCHITECTURE_GAP_REPORT.md) — A3 updated conceptually: **12** empty scaffolds, not 18 including crm/HR.

## Intended vs actual

| ID | Intended | Actual | Class |
|----|----------|--------|-------|
| DRIFT-ARCH-STATUS-SCAFFOLDS | Aug 12 status: crm/sales/HR empty | Wave 02 **TESTED** in application registry | DOCUMENTATION_DRIFT |
| DRIFT-CTX-VS-APP-YAML | Context ≈ application | **79** packages vs **47** registry apps | COVERAGE_GAP (not 32 missing products) |
| DRIFT-FE-MODULES | `frontend/modules/` mirrors backend | Directory **ABSENT**; `admin_portal` only | STRUCTURAL_DRIFT |
| DRIFT-PERSISTENCE-DEFAULT | Production postgres | Code default **memory**; local `.env` postgres | CONFIG_DRIFT |
| DRIFT-MISSING-ROUTERS | All ROUTER_SPECS import | P3 baseline skip / omit | BOUNDARY_HONESTY |
| DRIFT-GRAPHQL | README REST+GraphQL | GraphQL **NOT_AVAILABLE** | DOC_VS_RUNTIME |
| DRIFT-MICROSERVICES-DOCS | README lists TS ports 4000–4003 | Local MEOS run is FastAPI 8000 + Next 3001 | RUNTIME_VS_README |

## Boundary laws (still binding)

No cross-context **domain** imports. Documents blob SoR. Workflow = `workflow` context. AI via AI platform. Audit via audit context. Do **not** redesign to close count gaps.

## What is not drift

- TESTED workstation loops vs production ACTIVE — that is **environment**, already honest in registry `NOT_READY`.
- Blueprint fabrics gated off — by design (P2).
