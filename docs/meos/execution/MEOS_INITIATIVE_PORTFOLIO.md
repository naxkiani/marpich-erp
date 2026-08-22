# MEOS Initiative Portfolio

**Date:** 2026-08-18T12:45:00Z  
**Machine:** [MEOS_INITIATIVE_PORTFOLIO.v1.yaml](./MEOS_INITIATIVE_PORTFOLIO.v1.yaml)  
**SoR (backlog):** [MEOS_TECHNICAL_DEBT_REGISTRY.md](./MEOS_TECHNICAL_DEBT_REGISTRY.md) — **do not fork a second project/PMO product.**  
**Overall:** `BACKLOG_ONLY` · `in_progress_count: 0` · `cost_measured_count: 0`  
**P334:** each initiative maps 1:1 to `CHG-*` in [MEOS_CHANGE_REGISTRY.v1.yaml](./MEOS_CHANGE_REGISTRY.v1.yaml). Mapping ≠ IN_PROGRESS. Do not expand `projects`.  
**P335:** wrapped as `PF-LAUNCH-GOVERNANCE` in [MEOS_PORTFOLIO_INTELLIGENCE.v1.yaml](./MEOS_PORTFOLIO_INTELLIGENCE.v1.yaml). Still `BACKLOG_ONLY`. No budget/ROI. See [MEOS_P335_PORTFOLIO_INTELLIGENCE.md](./MEOS_P335_PORTFOLIO_INTELLIGENCE.md).

`projects` is **SCAFFOLDED** (empty). Finance registry claims `finance.budget.approved` but the finance context implements **accounts / fiscal periods / journals** — **no budget aggregate**. Resource alignment: **NOT_MEASURED**.

## Law

COST, EFFORT, VALUE, TIMELINE remain **NOT_MEASURED** unless a bill, timesheet, or approved budget exists. None evidenced.

## Portfolio (mapped from P325 debt)

| INITIATIVE_ID | DEBT | OBJECTIVE | STATUS | CATEGORY | COST | VALUE |
|---------------|------|-----------|--------|----------|------|-------|
| `INIT-G26` | `TD-G26-PROD-CLUSTER` | `OBJ-GATE-P314` | ASSESSED | OPERATIONAL_RESILIENCE | **NOT_MEASURED** | **NOT_MEASURED** |
| `INIT-G25` | `TD-G25-DIRTY-SHA` | `OBJ-GATE-P314` | ASSESSED | OPERATIONAL_RESILIENCE | **NOT_MEASURED** | **NOT_MEASURED** |
| `INIT-G27` | `TD-G27-ROLLBACK` | `OBJ-GATE-P314` | ASSESSED | OPERATIONAL_RESILIENCE | **NOT_MEASURED** | **NOT_MEASURED** |
| `INIT-G23` | `TD-G23-ALERTING` | `OBJ-GATE-P317` | IDENTIFIED | RISK_REDUCTION | **NOT_MEASURED** | **NOT_MEASURED** |
| `INIT-G18` | `TD-G18-AI-STUB` | `OBJ-GATE-P317` | IDENTIFIED | RISK_REDUCTION | **NOT_MEASURED** | **NOT_MEASURED** |
| `INIT-G19` | `TD-G19-DSAR` | `OBJ-GATE-P317` | IDENTIFIED | COMPLIANCE | **NOT_MEASURED** | **NOT_MEASURED** |

Remaining debt (`TD-G20-E2E`, `TD-G21-A11Y`, `TD-P319-AUTOMATION`, `TD-P321-INTEGRATIONS`, `TD-EVENT-PAYLOAD-SCHEMA`) stays on the **debt registry**. Do not duplicate as fake “growth” initiatives. `TD-SDK-STUB-SUCCESS` is **RESOLVED** (P323) — not an open initiative.

## Prioritization model (policy, not a scored ranker)

Order already evidenced by P325 / P313:

1. **P0** G26 → G25 → G27 (unblock go-live)  
2. **P1** G23 / G18 / G19 (trust)  
3. **P2** UX, automation, integrations **after** production exists  

Criteria (documented, **not** numerically scored — no invented weights): business impact (go-live blocks all value), risk, urgency, dependencies, capacity (**NOT_MEASURED**). Policy Engine remains SoR for business rules; this list is launch governance, not a new optimizer.

Do **not** prioritize unused marketplace SKUs or stub-AI “value” work over G26.

## Capacity / demand

P325 capacity: **NOT_MEASURED**. DEMAND vs CAPACITY, overload, underutilization: **BLOCKED**. No people/budget/compute inventory for initiatives.

## Portfolio balance

Open mapped initiatives concentrate in **OPERATIONAL_RESILIENCE** + **RISK_REDUCTION** + **COMPLIANCE**. That is honest (pre-production). GROWTH / CUSTOMER_VALUE / INNOVATION / EFFICIENCY initiatives: **none evidenced** — do not invent them for balance.
