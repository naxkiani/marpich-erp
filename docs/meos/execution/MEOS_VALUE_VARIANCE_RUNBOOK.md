# MEOS Value Variance Runbook

**Date:** 2026-08-19T07:25:00Z  
**P339 overlay** on [MEOS_VALUE_REALIZATION_RUNBOOK.md](./MEOS_VALUE_REALIZATION_RUNBOOK.md). **Not** a second value engine.  
**P340:** variance remains **NOT_MEASURED**. G26 not closed — do not compute ROI/leakage.

## Law

VARIANCE requires both EXPECTED and REALIZED from trusted sources (P338 KPI trust + P337 data trust). Missing either side → **NOT_MEASURED**. Do not invent VALUE_GAP, COST_OVERRUN, or root cause.

## Current state

| Variance type | Actual |
|---------------|--------|
| VALUE_GAP | **NOT_MEASURED** (both sides missing) |
| COST_OVERRUN | **NOT_MEASURED** (no budget aggregate) |
| TIME_OVERRUN | **NOT_MEASURED** |
| QUALITY_GAP | **NOT_MEASURED** |
| OUTCOME_GAP | Outcomes IDENTIFIED only |
| Root cause | **BLOCKED** — cannot claim leakage |

“No realized value” is consistent with **DEC-P326-001** (`NOT_REALIZED`) and G26 — it is **not** a quantified variance.

## When measurement exists

1. DETECT via existing analytics/metrics (not a new KPI engine)  
2. ANALYZE with evidence; AI suggestions **INFERRED_UNVERIFIED** until human review  
3. DECIDE via decision registry + HITL  
4. APPROVE via existing policy/workflow  
5. ACT via Task Center  
6. MEASURE again on production events  

Escalation (MINOR→owner … CRITICAL→governance) uses Policy Engine when bound — **NOT_IMPLEMENTED** today.

## Corrective actions now

**0**. Do not open fake CHG-* or ACTION_* to “close” variance.
