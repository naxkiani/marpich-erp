# MEOS Automation Registry

**Date:** 2026-08-18T06:40:00Z  
**Machine companion:** [MEOS_AUTOMATION_REGISTRY.v1.yaml](./MEOS_AUTOMATION_REGISTRY.v1.yaml)  
**Rule:** Never mark **ACTIVE** without production runtime evidence. Overall: **`BLOCK_AUTOMATION`**.

Allowed states: `DESIGNED` · `IMPLEMENTED` · `TESTED` · `ACTIVE` · `DISABLED` · `DEPRECATED`  
P319 additional honesty labels in notes: `IMPLEMENTED_UNVERIFIED` · `NOT_IMPLEMENTED`.

| AUTOMATION_ID | NAME | DOMAIN | TRIGGER | OWNER | RISK | POLICY | WORKFLOW | STATUS |
|---------------|------|--------|---------|-------|------|--------|----------|--------|
| `AUTO-Q2C-001` | Quote-to-cash event chain | sales / inventory / accounting | `crm.opportunity.won` → `sales.order.placed` | NOT_AVAILABLE | High (finance) | Financial Kernel posting rules | Task Center if approval defined | **TESTED** (demo loop) — not ACTIVE |
| `AUTO-P2P-001` | Procure-to-stock | procurement / inventory | reorder / receive events | NOT_AVAILABLE | High (spend) | procurement approval | requisition approve step | **TESTED** — not ACTIVE |
| `AUTO-H2R-001` | Hire to payroll/tax | HR / payroll / tax | `hr` hire events | NOT_AVAILABLE | High (employment) | payroll/tax policies | NOT_IMPLEMENTED generic HITL | **TESTED** — not ACTIVE |
| `AUTO-CARE-001` | Encounter to lab/pharmacy | hospital / clinic / lab / pharmacy | `*.encounter.*` | NOT_AVAILABLE | Critical (healthcare) | privacy + clinical HITL required | Must not auto-decide clinically | **TESTED** (care loop) — not ACTIVE |
| `AUTO-WF-001` | Module activation approval | workflow | `platform.module.activated` | platform | Medium | module activation | `module.{id}.approval` | **IMPLEMENTED** — production **NOT_AVAILABLE** |
| `AUTO-OUTBOX-001` | Outbox dispatch with retry cap | platform events | unpublished outbox rows | platform | Medium | n/a | n/a | **IMPLEMENTED** (P319 cap) — production dispatcher **NOT_AVAILABLE** |
| `AUTO-AI-001` | AI assist → action | ai | user prompt | NOT_AVAILABLE | High | `autonomy.high_risk` | Wave 05 HITL | **DISABLED** — stub; not an executor |
| `AUTO-AGENT-001` | Autonomous agents | core_platform / Wave 05 | propose action | NOT_AVAILABLE | Critical | flag + policy + human | `autonomy.action.approve` | **DISABLED** — deny-by-default |
| `AUTO-INC-001` | Incident to resolution | ops | incident created | NOT_AVAILABLE | High | — | — | **NOT_IMPLEMENTED** |
| `AUTO-RISK-001` | Risk to remediation | risk | threshold | NOT_AVAILABLE | High | — | — | **NOT_IMPLEMENTED** |

Rollout states for any future production enablement: `DISABLED` → `SHADOW` → `CANARY` → `LIMITED` → `FULL`. None are past DISABLED/TESTED.
