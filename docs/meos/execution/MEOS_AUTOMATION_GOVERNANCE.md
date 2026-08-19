# MEOS Automation Governance

**Date:** 2026-08-18T06:40:00Z  
**Gate result:** **`BLOCK_AUTOMATION`** for production activation.

## Security gates (all required before ACTIVE)

| Gate | Production status |
|------|-------------------|
| AUTH | Candidate P313; production **NOT_AVAILABLE** |
| AUTHZ | Permissioned APIs in code; production **NOT_AVAILABLE** |
| TENANCY | `tenant_id` on events/workflows; cross-tenant mutate forbidden |
| POLICY | Evaluate API exists; not proven on live automations |
| AUDIT | Event → audit path in code; production **NOT_AVAILABLE** |
| IDEMPOTENCY | Consumer keys in event bus |
| FAILURE_HANDLING | Outbox retry cap (P319); no infinite fetch |
| OBSERVABILITY | Production automation metrics **NOT_AVAILABLE** |
| ROLLBACK/COMPENSATION | Generic saga **NOT_IMPLEMENTED** |

**Any critical miss → do not mark ACTIVE.** Current miss: no production cluster (G26) plus TRUST_CRITICAL.

## HITL vs autonomous

| Class | Rule |
|-------|------|
| Low-risk bounded reversible | May be event-driven without extra workflow **after** production go-live + owner + monitoring |
| Financial / healthcare / privacy / employment / tenant / irreversible | Automation → recommendation → **human approval** → action → audit |
| AI | Must not convert stub/inference into irreversible action. Identify AI actor in audit when used. |

## Identities

Automation must not use uncontrolled superuser credentials. Production service-account inventory: **NOT_AVAILABLE**.

## Canary

Future rollout: DISABLED → SHADOW → CANARY → LIMITED → FULL. Nothing is FULL.

## Healthcare / financial safety

Do not enable unrestricted autonomous financial posting or clinical actions merely because ACL code exists.

## Wave 05

[MEOS_WAVE05_AUTONOMY_GATE.md](./MEOS_WAVE05_AUTONOMY_GATE.md) remains the autonomy contract. P319 tightened `AutonomyGate` to deny when flag/policy ports are missing.  
**P330 safety overlay:** [MEOS_AUTOMATION_SAFETY.md](./MEOS_AUTOMATION_SAFETY.md) — do not enable L3/L4 while `BLOCK_AUTOMATION` holds.
