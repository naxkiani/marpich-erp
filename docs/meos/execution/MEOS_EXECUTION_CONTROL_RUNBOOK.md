# MEOS Execution Control Runbook

**Date:** 2026-08-19T07:40:00Z  
**P339 overlay.** Reuses Workflow Task Center. **Not** a PMO, BPM, or second task engine.  
**P340:** G26 **BLOCKED**. Workflow binding **NOT_AVAILABLE**. Do not bind synthetic tasks. See [MEOS_P340_G26_EXECUTION_ENABLEMENT.md](./MEOS_P340_G26_EXECUTION_ENABLEMENT.md).

## Law

No action may bypass required approval. No fake IN_PROGRESS/COMPLETED. Material actions require human authorization (P330 L0 / `BLOCK_AUTOMATION`).

## Current operating mode

1. **Read** gate decisions: [MEOS_DECISION_REGISTRY.v1.yaml](./MEOS_DECISION_REGISTRY.v1.yaml) — all `workflow_task_id: NOT_AVAILABLE`
2. **Do not** treat Task Center catalog counts as execution of those decisions
3. **Do not** create ACTION_IDs for work that was explicitly not authorized (GO_LIVE, automation enable, release, value claim)
4. **Route** real operator work through existing `/api/v1/workflow/tasks` when tasks exist — they are **not** bound to DEC-* today
5. **Check** blockers: G26 cluster, G23 alerting, G19 DSAR  
6. **P340:** `meos-prod` stack STOPPED ≠ G26 PASS. Local `/health` 200 ≠ production runtime.

## Target loop (after GO_LIVE)

```
DECISION → APPROVAL → WORKFLOW TASK → ACTION → MEASURE → OUTCOME → BENEFIT
```

Bind `workflow_task_id` on the decision registry. Do not stand up `projects` as a parallel task SoR unless a true project aggregate is needed later.

## Priority into existing initiatives

| Order | ID | Why |
|-------|-----|-----|
| 1 | INIT-G26 | Production plane required to execute and measure |
| 2 | INIT-G23 | Observe execution failures |
| 3 | INIT-G18 | AI assist only; still HITL |
| 4 | INIT-G19 | Privacy before sensitive execution views |

`new_execution_platform: FORBIDDEN` · `new_initiative: FORBIDDEN`

## Executive control view

Extend [MEOS_EXECUTIVE_COCKPIT.md](./MEOS_EXECUTIVE_COCKPIT.md): DECISIONS → ACTIONS → BLOCKERS → OUTCOMES → BENEFITS. Until evidence exists, show **NOT_AVAILABLE** / documented holds — not fake progress bars.
