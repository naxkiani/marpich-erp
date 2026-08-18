# MEOS Adoption Standard

**Date:** 2026-08-18T17:15:00Z  
**SoR:** [MEOS_ADOPTION_STATUS.md](./MEOS_ADOPTION_STATUS.md)  
**Outcome:** `OUT-ADOPT-001` IDENTIFIED · baseline **NOT_MEASURED** ([MEOS_OUTCOME_GOVERNANCE.md](./MEOS_OUTCOME_GOVERNANCE.md))  
**Experience:** P320 **FUNCTIONAL** · **ADOPTED = false**

P334 does **not** create a second adoption-analytics or LMS product. Login or screen visits ≠ successful adoption. Deploy ≠ adopted.

## Model (measure only where data exists)

| Signal | Production actual |
|--------|-------------------|
| AWARENESS | **NOT_MEASURED** |
| TRAINING | assigned **0** · LMS **NOT_IMPLEMENTED** |
| USAGE | **NOT_AVAILABLE** |
| ENGAGEMENT | **NOT_AVAILABLE** |
| PROCESS_ADHERENCE | **NOT_MEASURED** |
| SUCCESS_RATE | **NOT_MEASURED** |
| REWORK | **NOT_MEASURED** |
| SUPPORT_REQUESTS | **NOT_MEASURED** |

Workstation Q2C / healthcare **TESTED** loops are **not** DAU, feature usage, or process adoption.

## Application adoption

ACTIVE_USERS, FEATURE_USAGE, TRANSACTION_VOLUME, SUCCESS_RATE, ERROR_RATE, WORKFLOW_COMPLETION: **NOT_AVAILABLE**. Application registry: **no app ACTIVE**. Connect later to registry + observability — not a new BI product.

## Process adoption

PROCESS_USAGE, COMPLIANCE, MANUAL_WORKAROUND, REWORK, ESCALATION, COMPLETION: **NOT_MEASURED**. Resistance/failure: **NOT_MEASURED**. Do not label individuals.

## Capability adoption

```
NEW_CAPABILITY → TRAINING → USAGE → BUSINESS_RESULT
```

P333 `operational_count: 0` · `validated_capability_count: 0`. Capability is **not** adopted because code is TESTED on a workstation.

## Training integration

```
CHANGE → SKILL_GAP → TRAINING → ASSESSMENT → VALIDATION → ADOPTION
```

Skill gap **NOT_IMPLEMENTED** (P333). University ≠ operator LMS. Training completion (none) ≠ operational adoption.

## Friction detection

MANUAL_WORKAROUND, REPEATED_ERROR, LOW_ADOPTION, HIGH_SUPPORT_VOLUME, PROCESS_REVERSION, TRAINING_GAP: **NOT_MEASURED** in production. Policy: do not brand people “resistant” without evidence and HR/policy SoR — neither is evidenced here.

## Value link (P326)

CHANGE → ADOPTION → CAPABILITY → OUTCOME → VALUE: **NOT_MEASURED**. Do not treat home pulse catalog counts as adoption KPIs.
