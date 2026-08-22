# MEOS Automation Safety

**Date:** 2026-08-18T13:35:00Z  
**SoR:** [MEOS_AUTOMATION_GOVERNANCE.md](./MEOS_AUTOMATION_GOVERNANCE.md) — **do not fork a second safety framework.**  
**Gate:** [MEOS_WAVE05_AUTONOMY_GATE.md](./MEOS_WAVE05_AUTONOMY_GATE.md) · `AutonomyGate`

P330 closed-loop actions that are high-impact remain **forbidden** while `BLOCK_AUTOMATION` holds.

## Supported vs unsupported actions

| Action | Supported by existing system? | P330 exposure |
|--------|-------------------------------|---------------|
| RETRY (outbox unpublished) | Yes — bounded `outbox_max_retries` | Code path; prod dispatcher **NOT_AVAILABLE** |
| CREATE_TASK / REQUEST_APPROVAL | Workflow Task Center | Manual/API; not signal-closed-loop |
| ESCALATE | IR severity table | **unstaffed** (P329) |
| ROLLBACK | Runbook + restore scripts | Production **BLOCKED** (G27) |
| RESTART / SCALE / FAILOVER | **NOT_IMPLEMENTED** as platform actions | **Do not recommend as executable** |
| SWITCH_TO_CONTINUITY_MODE | P329 **NOT_IN_FORCE** | **Do not expose as executable** |
| AI execute | Stub | **DISABLED** |

## Closed-loop safety (required, not claimed live)

```
DETECT → VALIDATE → AUTHORIZE → EXECUTE → VERIFY
FAILURE → STOP → ROLLBACK/FALLBACK → ESCALATE → AUDIT
```

HTTP 200 is **not** verification. Business smoke required after recovery (P329). Production loop: **NOT_ACTIVE**.

## Policy / Zero Trust

All L2+ actions: Feature Flags + Policy Engine + AuthZ + `tenant_id`. Cross-tenant mutate **prohibited**. AI **cannot**: change security policy, delete data, cross-tenant access, disable audit, bypass authorization, execute unapproved high-impact actions.

## Rollback

Generic saga **NOT_IMPLEMENTED**. Live production rollback **BLOCKED**. Do not claim reversible automation.

## Failure safety

Outbox parks at retry cap (no infinite fetch). Recursive automation loops: **not enabled** (nothing ACTIVE). Circuit breaker as a fabric: **NOT_IMPLEMENTED** (do not invent).

## Opaque autonomy

Forbidden. Production autonomous workflows emitting WHY/WHAT/WHEN/WHO/POLICY/ACTION/RESULT: **none** (none executing).
