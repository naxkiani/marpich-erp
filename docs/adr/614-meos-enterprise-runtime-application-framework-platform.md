# ADR 614 — MEOS Enterprise Runtime & Application Framework Platform (P257)

## Status
Accepted

## Context
P220–P254 established a large MEOS capability blueprint corpus. P257 opens the Productization & Experience Evolution Phase: convert blueprints into an executable Enterprise Operating Product via a central Runtime & Application Framework. Existing Module Registry, Plugin Platform, Feature Flags, Workflow, AppShell/UI standards and Identity already own adjacent concerns — MERAF must orchestrate, not fork them. P258 is planned for Shell & Command Center UX depth.

## Decision
1. SoR `enterprise_runtime`; fabric `meos_enterprise_runtime_application_framework_platform_framework`; API `/api/v1/enterprise-runtime*`; capability `CAP-PLT-MERAF-001`; acronym **MERAF**.
2. Logical BCs inside one SoR: Runtime Management, Application Experience contracts, Module Governance orchestration, Application Catalog, Deployment, Runtime Governance.
3. Federate with Module Registry, Plugin Platform, Feature Flags, Workflow, Identity/AuthZ, API Gateway, AppShell (deepened by P258), P214-Z, Policy, Audit, Observability — never replace them; never dual-write registry/plugin catalogs; never fork `/api/v1/plugins*`.
4. Inference only via P214-Z; activate/deploy/retire via Workflow + Policy; unsigned third-party load forbidden; no local feature flags; no business aggregates in runtime SoR.
5. Roadmap: P257 foundation → P257-A Runtime Foundation → P257-B Experience (with P258) → P257-C AI Native Runtime → P257-D Enterprise OS.

## Consequences
Positive: governed path from blueprint → activatable enterprise applications under Zero Trust.  
Negative: UX shell depth and command-center productization deferred to P258; module/plugin truth remains peer-owned — MERAF stores sessions, compositions and peer refs only.

## Links
Law: `ENTERPRISE_MEOS_RUNTIME_APPLICATION_FRAMEWORK_PLATFORM.md` · Prior: ADR 613 · Next: P257-A · Peer: ADR 615 (P258 MESCC)
