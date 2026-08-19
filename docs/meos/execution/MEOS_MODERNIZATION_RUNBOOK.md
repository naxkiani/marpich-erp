# MEOS Modernization Runbook

**Date:** 2026-08-19T06:15:00Z  
**P336 overlay.** Priorities flow into **existing** P335 initiatives. **Not** a new project system.

## Law

Prioritize business/risk/dependency/readiness — not language fashion. No production retire from static inventory. AI must not migrate databases or delete apps.

## Order (evidence)

1. **INIT-G26** — production topology (R-01). Unlocks measurement.  
2. **INIT-G25 / INIT-G27** — immutable SHA + rollback.  
3. **INIT-G23** — production alerting (observability gap).  
4. **TD-EVENT-PAYLOAD-SCHEMA** — event envelope honesty.  
5. Persistence: production **postgres** (already gated when `MARPICH_ENVIRONMENT=production`).  
6. Legacy TS `services/*` **CONSOLIDATE** only after consumer evidence — not a P0 vs G26.  
7. Empty scaffolds stay **FREEZE**. Blueprints stay **MONITOR**.

Do **not** extract microservices as a P0 (Wave 01 architecture status still holds).

## Consolidation

| Candidate | Preserve | Risk |
|-----------|----------|------|
| TS identity/gateway → FastAPI | Identity/tenant capability | Duplicate auth if both run |
| warehouse vs inventory | Inventory TESTED capability | warehouse is empty — nothing to merge in prod |

## Decommission checklist (none eligible)

USAGE, DEPENDENCIES, DATA, SECURITY, COMPLIANCE, BACKUP, MIGRATION, ROLLBACK — all **NOT_APPLICABLE** for production because **0 ACTIVE** apps. `retirement_candidates: []`.
