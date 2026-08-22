# MEOS Change Management

**Status:** Procedure only. **Not in force on a production cluster** (P314 go-live not approved).  
**P324:** [MEOS_P324_RELEASE_ENGINEERING.md](./MEOS_P324_RELEASE_ENGINEERING.md) · [MEOS_ROLLBACK_STANDARD.md](./MEOS_ROLLBACK_STANDARD.md).  
**P334 overlay:** [MEOS_CHANGE_MANAGEMENT_STANDARD.md](./MEOS_CHANGE_MANAGEMENT_STANDARD.md) · objects [MEOS_CHANGE_REGISTRY.v1.yaml](./MEOS_CHANGE_REGISTRY.v1.yaml) · runbook [MEOS_CHANGE_RUNBOOK.md](./MEOS_CHANGE_RUNBOOK.md). **Do not** treat this procedure as an ITSM product.  
**Date:** 2026-08-18T05:54:44Z · overlay 2026-08-18T17:15:00Z

Use this after `PRODUCTION_ACTIVE`. Do not treat local hotfixes as production changes.

## Categories

| Category | When | Requirement |
|----------|------|-------------|
| STANDARD | Repeatable, low risk, pre-approved | Checklist + SHA |
| NORMAL | Default | Reason, scope, risk, test, deploy plan, rollback, verification |
| EMERGENCY | P0/P1 containment | Execute, then document the same fields |

## Required fields (every meaningful change)

reason · scope · risk · affected services · testing · deployment plan · rollback plan · verification · documentation · source SHA

Emergency changes remain auditable after execution. Uncontrolled production patches are forbidden.
