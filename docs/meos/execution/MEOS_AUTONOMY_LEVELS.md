# MEOS Autonomy Levels

**Date:** 2026-08-18T13:35:00Z  
**SoR (gate):** [MEOS_WAVE05_AUTONOMY_GATE.md](./MEOS_WAVE05_AUTONOMY_GATE.md)  
**SoR (production activation):** [MEOS_P319_AUTOMATION_FABRIC.md](./MEOS_P319_AUTOMATION_FABRIC.md) **`BLOCK_AUTOMATION`**  
**Machine:** [MEOS_AUTONOMY_LEVELS.v1.yaml](./MEOS_AUTONOMY_LEVELS.v1.yaml)

No system may silently operate above `max_authorized_level`. Current: **L0**. L3/L4 **NOT_ACTIVE**.

## Levels (P330)

| Level | Name | Production |
|-------|------|------------|
| **L0** | OBSERVE_ONLY | **AUTHORIZED** as ceiling · **observe itself BLOCKED** (G23; `observe_operational: false`) |
| **L1** | RECOMMEND | **NOT_AUTHORITATIVE** — AI stub must not be treated as a recommendation |
| **L2** | HUMAN_APPROVAL | Workflow/Task Center **exists**; production HITL loop **NOT_ACTIVE** |
| **L3** | POLICY_APPROVED_AUTOMATION | Outbox retry cap is **code**; production dispatcher **NOT_AVAILABLE** · **not ACTIVE** |
| **L4** | CONTROLLED_AUTONOMOUS_OPERATION | `AutonomyGate` deny-by-default · `AUTO-AGENT-001` **DISABLED** |

P319 maturity **EVENT_DRIVEN (demo)** is **not** L3/L4.

## Mapping to Wave 05

Wave 05 requires flag + policy + human workflow before high-risk mutate. Missing ports → deny (`autonomy.errors.gate_unavailable`). That is **L2 minimum** for high-risk; **not enabled** in production.

`POST /api/v1/autonomy/actions/propose` remains a **stub contract** in the Wave 05 doc — not a live action bus.

## HITL (L2)

Would show: RECOMMENDATION · EVIDENCE · RISK · EXPECTED_RESULT · APPROVE/REJECT.  
Production: **NOT_ACTIVE**. Do not invent approval queues.
