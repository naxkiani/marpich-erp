# MEOS Application Portfolio

**Date:** 2026-08-19T06:15:00Z  
**SoR (inventory):** [MEOS_APPLICATION_REGISTRY.md](./MEOS_APPLICATION_REGISTRY.md) / [MEOS_APPLICATION_REGISTRY.v1.yaml](./MEOS_APPLICATION_REGISTRY.v1.yaml)  
**P336 overlay:** lifecycle and redundancy only. **Do not** treat this file as a second registry.

## Law

ACTIVE only per registry rule (login-scoped create/read/update/search in production). Route, menu, screen, or folder ≠ ACTIVE. `overall_status: NOT_READY` · `ACTIVE: 0`.

## Portfolio snapshot (reconciled)

| Status | Count | P336 recommendation |
|--------|-------|---------------------|
| INTEGRATED | 6 | **RETAIN** |
| IMPLEMENTED | 12 | **RETAIN** |
| TESTED | 12 | **RETAIN** |
| BLUEPRINT | 5 | **MONITOR** (gated) |
| SCAFFOLDED | 12 | **FREEZE** (coming_soon) |
| ACTIVE | 0 | — |

Owner / usage / cost / business_value on every row: **NOT_AVAILABLE** / **NOT_MEASURED**. Do not copy registry `score` as production health.

## Objects

Fields APPLICATION_ID, NAME, DOMAIN, STATUS, routes, api_prefix live in the YAML SoR. This overlay does not duplicate them.

Criticality in production: **NOT_APPLICABLE** (nothing deployed). Workstation TESTED slices are **not** production-critical.

## Redundancy (evidence only)

| ID | Pair | Class | Action |
|----|------|-------|--------|
| RD-INV-WH | inventory / warehouse | PARTIAL_OVERLAP | warehouse empty — none |
| RD-EDU | university / school | COMPLEMENTARY | none |
| RD-IDENTITY-FABRIC | identity / authentication / directory | COMPLEMENTARY | none |
| RD-FINANCE-SURFACE | accounting vs finance/kernel/treasury | UNKNOWN | do not eliminate |
| RD-TS-PYTHON-IDENTITY | `services/identity-service` vs `contexts/identity` | FULL_DUPLICATION (intent) | CONSOLIDATE toward FastAPI; **no production retire** |

## Capability coverage

Wave 02 TESTED apps map to CAP-ENT / CAP-HLT in P326. Production capability coverage **NOT_MEASURED**. Empty scaffolds do **not** cover capabilities.
