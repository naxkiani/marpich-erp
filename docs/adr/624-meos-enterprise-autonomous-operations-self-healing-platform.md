# ADR 624 — MEOS Enterprise Autonomous Operations & Self-Healing Platform (P267)

## Status
Accepted

## Context
P266 established MEAAOI over AI Platform / P214-Z. P267 productizes Autonomous Operations & Self-Healing as the MEOS Autonomous Enterprise Operations Layer. P225 EAOSHP already owns `autonomous_operations` and `/api/v1/autonomous-operations*`; Observability owns technical telemetry. MEAOSH must federate those SoRs — never fork the autonomous-ops API, never create module-local metrics stores, and never ungated critical self-healing. P268 is planned for Cybersecurity Intelligence & Zero Trust Defense productization over P226/P246.

## Decision
1. SoR `operations_autonomy`; fabric `meos_enterprise_autonomous_operations_self_healing_operating_platform_framework`; API `/api/v1/operations-autonomy*`; capability `CAP-PLT-MEAOSH-001`; acronym **MEAOSH**.
2. Logical BCs inside one SoR: Operations Intelligence, Self-Healing, Reliability Management, Optimization, Observability Operating, Ops Governance.
3. Federate with P225, Observability, P266, P265, P264, Workflow, Policy, Scheduler, P214-Z, Audit — never replace them; never dual-write `autonomous_operations_*`.
4. Inference only via P214-Z; critical recovery requires Workflow + human approval; simulation ≠ execute; physical actuation via P216-Z + Workflow; no silent recovery without audit.
5. Roadmap: P267 foundation → P267-A…D; unblocks P268.

## Consequences
Positive: governed Ops OS (incident/RCA/recovery/reliability campaigns) over canonical autonomous operations.  
Negative: healing aggregate truth remains P225-owned; telemetry remains Observability-owned — MEAOSH stores operating campaigns and peer refs only.

## Links
Law: `ENTERPRISE_MEOS_AUTONOMOUS_OPERATIONS_SELF_HEALING_PLATFORM.md` · Prior: ADR 623 · Next: P267-A · Peer: ADR 625 (P268 MECZTD) · Canonical: P225 EAOSHP
