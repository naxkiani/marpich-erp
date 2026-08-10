# ADR 616 — MEOS Dynamic Module Activation & Application Lifecycle Platform (P259)

## Status
Accepted

## Context
P257 (MERAF) and P258 (MESCC) established runtime composition and human experience. P259 deepens dynamic module activation and application lifecycle governance. Module Registry and Plugin Platform remain catalog/install SoRs; Workflow remains approval SoR — MDMAL must not fork those APIs or dual-write catalogs. P260 is planned for workflow execution/orchestration productization depth.

## Decision
1. SoR `module_lifecycle`; fabric `meos_dynamic_module_activation_application_lifecycle_platform_framework`; API `/api/v1/module-lifecycle*`; capability `CAP-PLT-MDMAL-001`; acronym **MDMAL**.
2. Logical BCs inside one SoR: Module Management, Application Lifecycle, Activation, Dependency Graph, Module Governance, Health.
3. Federate with Module Registry, Plugin Platform, P257, P258, Workflow, Feature Flags, Identity, Policy, Audit, P214-Z — never replace them; never dual-write registry/plugin catalogs; never fork `/api/v1/enterprise-runtime*`, `/api/v1/enterprise-experience*` or `/api/v1/plugins*`.
4. Inference only via P214-Z; activate/deploy/upgrade/retire via Workflow + Policy; unsigned load forbidden; plan/simulation ≠ execute; no local approval or feature-flag stores.
5. Roadmap: P259 foundation → P259-A Registry Foundation → P259-B Activation Runtime → P259-C Autonomous Lifecycle → P259-D Self Evolution; unblocks P260.

## Consequences
Positive: governed path from blueprint modules to runtime evolution with dependency and health control.  
Negative: catalog and runtime session truth remain peer-owned — MDMAL stores lifecycle state, plans, graphs, health and peer refs only.

## Links
Law: `ENTERPRISE_MEOS_DYNAMIC_MODULE_ACTIVATION_LIFECYCLE_PLATFORM.md` · Prior: ADR 615 · Next: P259-A · Peer: ADR 617 (P260 MEWEOP)
