# MEOS Decision Intelligence

**Date:** 2026-08-18T12:45:00Z  
**SoR (fabric):** [MEOS_DECISION_FABRIC.md](./MEOS_DECISION_FABRIC.md) — **do not duplicate** as a second decision product.  
**Machine decisions:** [MEOS_DECISION_REGISTRY.v1.yaml](./MEOS_DECISION_REGISTRY.v1.yaml)  
**P338 overlay:** [MEOS_P338_DECISION_INTELLIGENCE.md](./MEOS_P338_DECISION_INTELLIGENCE.md) · machine [MEOS_DECISION_INTELLIGENCE.v1.yaml](./MEOS_DECISION_INTELLIGENCE.v1.yaml)  
**Overall:** `DOCUMENTED` · `executed_count: 0` · `measured_followup_count: 0`  
**P332 overlay:** [MEOS_DECISION_MEMORY.md](./MEOS_DECISION_MEMORY.md) — RESULT→LEARNING still **BLOCKED**.

P327 records **already-taken phase decisions**. It does not run a decision engine.

## Lifecycle (actual vs claimed)

```
IDENTIFY → ANALYZE → COMPARE → DECIDE → EXECUTE → MEASURE → REVIEW
                              ▲ current (docs only)
```

EXECUTE / MEASURE / REVIEW of those decisions against production outcomes: **BLOCKED** (no production). Workflow Task Center connection: `workflow_task_id: NOT_AVAILABLE`.

## Registry (actual)

| DECISION_ID | SELECTED | LIFECYCLE | EVIDENCE |
|-------------|----------|-----------|----------|
| `DEC-P314-001` | `GO_LIVE = NOT APPROVED` | DECIDE | P314 report |
| `DEC-P319-001` | `BLOCK_AUTOMATION` | DECIDE | P319 fabric |
| `DEC-P324-001` | `NOT_RELEASE_CANDIDATE` | DECIDE | P324 |
| `DEC-P326-001` | value `NOT_REALIZED` | DECIDE | P326 |

Owners: **NOT_AVAILABLE** (not invented). Review dates: **NOT_SET**.

## Evidence sources allowed

KPI (P318 catalog — ACTUAL **NOT_MEASURED**) · Outcome (P326 IDENTIFIED) · Risk (R-01…R-07) · Cost (**NOT_MEASURED**) · Capacity (**NOT_MEASURED**) · Forecast (**NOT_CREATED**) · Scenario (**NOT_CREATED**).

## AI decision support

Reuse `/api/v1/ai/assist` stub (G18). May **not** be treated as SUMMARY / OPTIONS / TRADE-OFFS / FORECAST / RECOMMENDATION evidence. Confidence: **NOT_AVAILABLE**. Human decides. Autonomy gate fail-closed. No high-impact autonomous policy ACTIVE.

## Scenarios / forecasts

Analytics predictive/prescriptive **catalogs** exist (`/predictive*`, `/prescriptive/objectives` mode names). Production BASELINE vs SCENARIO_A/B/C: **NOT_CREATED**. Distinguish: catalogs = DESIGNED; results would be **SIMULATED** if ever run — none run. Horizon / model / confidence: **NOT_AVAILABLE**.

Digital twin: identity projections only. Strategic twin STRATEGY→SCENARIO→EXPECTED_OUTCOME: **NOT_AVAILABLE**.

Knowledge graph: ACL flags only. OBJECTIVE→INITIATIVE→CAPABILITY graph for decisions: **NOT_AVAILABLE**. No second graph.

## Trade-offs

Insufficient cost/capacity/value data for VALUE vs COST vs RISK scoring. Qualitative: G26 first (blocks all later options). Unexplained ranked recommendations: **forbidden**.

## Early warning / notifications

Reuse Notification Center + analytics `AlertRule`. Production OBJECTIVE_AT_RISK / KPI_DECLINE alerts: **NOT_AVAILABLE** (G23). Do not create a notifier.

## Governance / audit / privacy

Objective/target/decision changes must go through existing Audit Platform when they become runtime mutations. This phase added **documents + YAML**, not new mutation APIs — no OBJECTIVE_CREATED runtime events. Tenant isolation: future runtime registries must carry `tenant_id`; these YAML files are **platform-launch** records, not tenant OKRs. Workforce/customer PII: none in this overlay.
