# MEOS Wave 05 — Autonomy (gated)

**Status:** GATED · **Date:** 2026-08-13  
**P319 (2026-08-18):** Autonomy remains **GATED**. Production automation **`BLOCK_AUTOMATION`**. See [MEOS_P319_AUTOMATION_FABRIC.md](./MEOS_P319_AUTOMATION_FABRIC.md). `AutonomyGate` now denies when flag or policy ports are missing.  
**P330:** production ceiling **L0** (`observe_operational: false`). L3/L4 **NOT_ACTIVE**. See [MEOS_AUTONOMY_LEVELS.md](./MEOS_AUTONOMY_LEVELS.md).

**Law:** No high-risk autonomous action without Policy Engine allow + human Workflow approval.

## Gate conditions (all required)

1. Wave 04 Privacy activation pack present and Policy evaluate reachable
2. Feature flag `autonomy.agents.enabled` = true (Feature Flag System — tenant scope)
3. Policy evaluate `autonomy.high_risk` → allow
4. Workflow task `autonomy.action.approve` completed by human

## Runtime contract

```
POST /api/v1/autonomy/actions/propose
→ Policy evaluate
→ if deny: 403
→ if allow: create workflow instance
→ on workflow.completed: execute via owning context ACL (never direct peer DB)
```

Implementation: `backend/contexts/core_platform` or dedicated thin autonomy facade — **stub** in
`shared/application/ports/autonomy_gate.py` + unit tests proving deny-by-default.

## Forbidden until gates pass

- Self-healing that mutates production data without approval
- Agent writes to financial_kernel / healthcare without policy+workflow
- Module-local agent runners bypassing AI Platform

## Verification

```bash
./scripts/meos-wave05-autonomy-gate.sh
```
