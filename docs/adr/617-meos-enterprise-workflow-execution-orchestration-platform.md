# ADR 617 — MEOS Enterprise Workflow Execution & Orchestration Platform (P260)

## Status
Accepted

## Context
P259 established MDMAL for module lifecycle. P260 productizes workflow execution and orchestration as the MEOS Business Execution Operating Layer. The Enterprise Workflow Engine already owns definitions, instances, tasks and the visual designer (`/api/v1/workflow*`). Policy Engine owns policy evaluation; P224 owns decision intelligence. MEWEOP must federate these SoRs — never fork Workflow Engine or embed module-local approval engines. P261 is planned for Business Rules & Decision Intelligence depth.

## Decision
1. SoR `workflow_orchestration`; fabric `meos_enterprise_workflow_execution_orchestration_platform_framework`; API `/api/v1/workflow-orchestration*`; capability `CAP-PLT-MEWEOP-001`; acronym **MEWEOP**.
2. Logical BCs inside one SoR: Workflow Management (orchestration), Process Execution overlay, Decision Assist, SLA & Exception, Process Monitoring, Orchestration Governance.
3. Federate with Workflow Engine, Policy Engine, P224, P257–P259, Notifications, Identity, P214-Z, Audit — never replace them; never dual-write `workflow_*`; never fork `/api/v1/workflow*`.
4. Inference only via P214-Z; critical approvals and autonomous recovery require human authority + Workflow Engine; simulation ≠ execute; no local policy tables or local approval engines in business modules.
5. Roadmap: P260 foundation → P260-A…D; unblocks P261.

## Consequences
Positive: governed process OS fabric (SLA, exceptions, optimization) over canonical workflow runtime.  
Negative: definition/instance truth remains Workflow Engine-owned — MEWEOP stores orchestration overlays, SLA/exception campaigns, analytics projections and peer refs only.

## Links
Law: `ENTERPRISE_MEOS_WORKFLOW_EXECUTION_ORCHESTRATION_PLATFORM.md` · Prior: ADR 616 · Next: P260-A · Peer: ADR 618 (P261 MEBRDI) · Canonical: `ENTERPRISE_WORKFLOW_ENGINE.md`
