# MEOS Change Runbook

**Date:** 2026-08-18T17:15:00Z  
**In force on production:** **false** (P314 GO_LIVE not approved).  
**Reuse:** [MEOS_CHANGE_MANAGEMENT.md](./MEOS_CHANGE_MANAGEMENT.md) · [MEOS_RELEASE_GOVERNANCE.md](./MEOS_RELEASE_GOVERNANCE.md) · [MEOS_ROLLBACK_STANDARD.md](./MEOS_ROLLBACK_STANDARD.md) · Workflow Task Center · Notification Center · Audit Platform.

This is an **operator runbook overlay**, not a new workflow engine or PM tool.

## When a production change is allowed

1. `PRODUCTION_ACTIVE` true and P313 P0 = 0  
2. P314 `GO_LIVE = APPROVED`  
3. Immutable SHA (G25)  
4. Change record fields complete (reason, scope, risk, test, deploy, rollback, verify)  
5. High-risk: human approval (AI must not auto-approve)  
6. Readiness gate not skipped (P333 evidence, not assertion)

Until then: **STOP**. Local hotfixes are not production changes.

## Execution path (target)

```
CHANGE (this overlay)
  → TASKS in existing Workflow (training, comms, config, test, migrate, validate, docs, support)
  → RELEASE (release registry + CI)
  → DEPLOYMENT
  → OBSERVATION (alerting G23 — currently FAIL)
  → VALIDATION (BEFORE vs AFTER — currently NOT_MEASURED)
  → ROLLBACK if needed (G27 BLOCKED until first prod deploy)
```

Do **not** seed Task Center with placeholder tickets. Communication uses Notification Platform — never module SMTP.

## Milestones

MILESTONE requires OWNER, TARGET, STATUS, **EVIDENCE**.  
Current: **none complete**. Dates **NOT_SET**. A docs commit is not a completed go-live milestone.

## Emergency

EMERGENCY category remains in the procedure SoR. P316 quality CRITICAL and G26 are **launch P0s**, not a declared production crisis (P329 `declared_count: 0`). Do not run emergency-change theatre on a cluster that does not exist.

## Continuity checks (P329)

Every critical change must consider RTO/RPO/failover/recovery/rollback. Production values: **NOT_VERIFIED** / **BLOCKED**. Local restore drills ≠ change validation.

## Autonomous change (P330)

Ceiling **L0**. `BLOCK_AUTOMATION`. No autonomous escalation. Future: only low-risk, reversible, policy-authorized changes after observe actually works.

## After-action

Validated outcome → P332 lesson (only when VALIDATED) → P331 if a measured bottleneck. Today: **no** validated change outcomes.

## Notifications (when production exists)

CHANGE_CREATED / APPROVED / BLOCKED / MILESTONE_DUE / TRAINING_REQUIRED / DEPLOYMENT_STARTED / VALIDATION_REQUIRED / COMPLETED / ROLLBACK — via Notification Center, tenant- and role-scoped. **Not implemented** as live events this phase.
