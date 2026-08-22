# MEOS Capability Model

**Date:** 2026-08-18T17:00:00Z  
**SoR (taxonomy):** [BUSINESS_CAPABILITIES_REGISTRY.md](../architecture/BUSINESS_CAPABILITIES_REGISTRY.md) · `backend/shared/contracts/business_capabilities.json`  
**SoR (implementation status):** [MEOS_APPLICATION_REGISTRY.md](./MEOS_APPLICATION_REGISTRY.md)  
**P333 overlay (maturity/gaps):** [MEOS_CAPABILITY_READINESS.v1.yaml](./MEOS_CAPABILITY_READINESS.v1.yaml)

P333 **extends** the existing catalog. It does **not** create a second capability taxonomy.

## What a capability is here

| Field | Source |
|-------|--------|
| CAPABILITY_ID / NAME / DOMAIN | Registry JSON (`CAP-ENT-*`, `CAP-EDU-*`, …) or platform owner (`identity`, `search`) |
| OWNER | **NOT_AVAILABLE** (not invented) |
| MATURITY / STATUS | Overlay only — evidence-backed |
| STRATEGIC_ALIGNMENT | P327 PLATFORM_GATE DRAFT rows only |
| DEPENDENCIES | Documented gaps (cluster, DSAR, observe) |
| STATUS | `DEFINED` \| `PARTIAL` \| `OPERATIONAL` \| `MATURE` \| `AT_RISK` \| `DEPRECATED` |

`OPERATIONAL` and `MATURE` require production evidence. **`operational_count: 0`** · **`mature_count: 0`**.

Application `TESTED` / `INTEGRATED` on workstation ⇒ overlay **PARTIAL** + CMMI **IMPLEMENTED** + validation **IMPLEMENTED_UNVERIFIED**.  
Catalog row with no aggregate ⇒ **DEFINED**.  
G19/G23/G26 ⇒ **AT_RISK** or gap **MISSING**.

## CMMI overlay (do not inflate)

| Level | When allowed | Current |
|-------|----------------|---------|
| DEFINED | Catalog / architecture exists | Yes (registry) |
| IMPLEMENTED | Code + tests on an environment | Workstation only for several apps |
| MEASURED | Production telemetry + outcome | **NOT_MEASURED** |
| OPTIMIZED | Measured improvement (P331) | **NOT_MEASURED** (P331 BLOCKED) |

Incomplete evidence must **not** become MATURE.

## Business capability chain (where supported)

```
BUSINESS_CAPABILITY (registry ID)
  → BUSINESS_PROCESS (P326 outcomes IDENTIFIED)
  → APPLICATION (application registry; none ACTIVE)
  → SERVICE (bounded context)
  → ROLE (identity permission strings — not job architecture)
  → SKILL (NOT_IMPLEMENTED)
```

Example: CAP-ENT-010 → hire/terminate process TESTED → `human_resources` TESTED → identity user is a **separate** SoR. Job title on Employee is unstructured text.

CAP-ENT-011/012/013/014/016 remain **DEFINED** (recruitment/attendance/leave/performance/benefits not implemented as aggregates). Payroll CAP-ENT-015 is **PARTIAL** (TESTED, not production).

University `CAP-EDU-*` is an **industry** student lifecycle — **not** MEOS operator capability training.

## Strategic mapping

See YAML `strategic_mappings`. All three P327 objectives are **DRAFT**; readiness **BLOCKED**. Critical objectives without sufficient capability are **surfaced as gaps**, not marked ACHIEVED.

## Forbidden

- Duplicate CAP IDs or a parallel “MEOS capability library”
- Treating registry existence as OPERATIONAL
- Treating identity users as skilled workforce
- Promoting PARTIAL → MATURE because tests pass
