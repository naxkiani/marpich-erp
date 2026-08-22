# MEOS Decision Runbook

**Date:** 2026-08-19T07:10:00Z  
**P338 overlay.** Operational path for decision intelligence — **not** a new PM or BI product.

## Law

No invented KPIs, signals, or outcomes. Catalog counts ≠ business KPIs. No false early warnings.

## Current operating mode

1. **Read** phase decisions: [MEOS_DECISION_REGISTRY.v1.yaml](./MEOS_DECISION_REGISTRY.v1.yaml)
2. **Check** blockers: G26 (production), G19 (DSAR), G23 (alerting)
3. **Use** home pulse only as catalog sizes — see [MEOS_METRIC_GOVERNANCE.md](./MEOS_METRIC_GOVERNANCE.md)
4. **Do not** treat AI stub as recommendation evidence
5. **Route** real work through Workflow Task Center when tasks exist — decision IDs not yet bound  
6. **P339:** do not invent ACTION_IDs for gate holds. See [MEOS_EXECUTION_CONTROL_RUNBOOK.md](./MEOS_EXECUTION_CONTROL_RUNBOOK.md)

## Target loop (after GO_LIVE)

```
DATA → KPI (governed) → SIGNAL → INSIGHT → DECISION → WORKFLOW → ACTION → OUTCOME → LEARNING (P332)
```

## Priority into existing initiatives

| Order | ID | Why |
|-------|-----|-----|
| 1 | INIT-G26 | Production telemetry required for KPI trust |
| 2 | INIT-G23 | Early warning / observability |
| 3 | INIT-G18 | AI assist hardening (still HITL) |
| 4 | INIT-G19 | Privacy before executive PII views |
| 5 | TD-EVENT-PAYLOAD-SCHEMA | Event-backed KPI integrity |

`new_decision_platform: FORBIDDEN` · `new_initiative: FORBIDDEN`

## Forbidden

- Second BI / KPI / analytics / AI platform
- Displaying pulse counts as revenue, risk, or availability
- Autonomous approval of material decisions
- Fake decision queue or COMPLETED badges
