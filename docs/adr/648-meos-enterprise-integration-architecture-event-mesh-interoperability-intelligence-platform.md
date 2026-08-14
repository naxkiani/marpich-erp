# ADR 648 — MEOS Enterprise Integration Architecture, Event Mesh & Interoperability Intelligence Platform (MEIEII)

- **Status:** Accepted
- **Date:** 2026-08-11
- **Deciders:** Chief Enterprise Architect · MEOS Architecture Board
- **Tags:** meos · p291 · meieii · integration-architecture · event-mesh · interoperability · contracts · productization
- **Related:** [ADR 647](647-meos-enterprise-data-architecture-master-data-information-architecture-intelligence-platform.md) · [ADR 646](646-meos-enterprise-application-architecture-api-governance-software-architecture-intelligence-platform.md) · [ADR 649](649-meos-enterprise-api-management-service-gateway-digital-integration-experience-platform.md) · [ADR 650](650-meos-enterprise-event-streaming-intelligence-realtime-event-platform-event-product-marketplace.md) · [ADR 620](620-meos-enterprise-data-intelligence-data-mesh-operating-platform.md) · [Law P291](../architecture/ENTERPRISE_MEOS_INTEGRATION_ARCHITECTURE_EVENT_MESH_INTEROPERABILITY_INTELLIGENCE_PLATFORM.md) · [INTEGRATION_PLATFORM.md](../architecture/INTEGRATION_PLATFORM.md) · Governance Standard 11.0

## Context

MEOS needs a specialized **Enterprise Integration Architecture / Event Mesh / Interoperability Intelligence** productization layer — without replacing Core Integration Platform connector execution (`contexts/integration`), Data Mesh (P263), Application Architecture (P289), Data Architecture (P290), or API Management/Gateway (P292), and without ungated integration mutations.

## Decision

1. Establish SoR **`integration_architecture_operating`** as MEIEII fabric under API **`/api/v1/integration-architecture-operating*`**, schema **`integration_architecture_operating_*`**.
2. Capability **`CAP-PLT-MEIEII-001`**; fabric id **`meos_enterprise_integration_architecture_event_mesh_interoperability_intelligence_platform_framework`**.
3. **Boundary law (hard):**
   - **Integration Platform** = sole external connector execution SoR — **never replace**
   - **P291** = Integration Architecture / Event Mesh / Interoperability Intelligence
   - **P292** = API Management / Service Gateway / API Product Experience (delivered; distinct)
   - **P293** = Event / Streaming / Real-Time Event Product Experience (delivered; distinct)
   - **P294** = Notification / Omnichannel Experience (next; distinct)
   - Never replace P263 · P289 · P290 · Observability · Secrets
4. Federate-by-contract: Integration Platform, P263, P289, P290, P287, P288, P286, Observability, Secrets, Workflow, Policy — never fork `/api/v1/integrations*`; never dual-write Integration Platform connector tables; never local metrics stores; never local approval engines.
5. Integration/event/message contracts and mesh topology are **versioned, explainable, reproducible, auditable**. Material activate/partner/migrate/autonomous reliability actions require **Policy + Risk + Approval + Verification + Audit** (or published Autonomy Threshold).
6. No event without Contract Governance; no sensitive integration without Identity + Authorization; no breaking change without Impact Analysis.
7. **No AI Agent may execute uncontrolled integration mutations outside Policy + Delegation Authority.** Simulation ≠ execute.
8. Inference → **P214-Z** only; no module-local LLM.
9. Designed vs Actual integration drift must be detectable via Observability/P286/P257 ACL.

## Consequences

- Unlocks Phase 1–5 MEIEII roadmap (P291-A…E); **P292** MEAPIE delivered; **P293** Event Streaming / Real-Time Event Product series unblocked.
- Integration Platform remains connector execution SoR; MEIEII owns integration architecture, event-mesh intelligence and gated modernization overlays.
- Ungated integration mutation or merging Integration Platform+P291+P292+P293 SoRs is an architecture failure.

## Alternatives considered

| Alternative | Rejected because |
|-------------|------------------|
| Embed event-mesh OS inside Integration Platform only | Violates connector execution vs architecture intelligence split |
| Embed integration architecture inside P289 App Architecture | Violates app architecture vs enterprise integration split |
| Dual-write connectors into architecture tables | Violates service boundary / schema isolation |
| Local metrics for integration observability | Violates Observability Platform law |
| Ungated agent activate/failover | Violates human integration governance |

## Compliance checklist

- [x] DDD · CQRS · events · hexagonal boundaries documented
- [x] Peer federation matrix (Integration Platform · P263 · P289 · P290 · Observability · Workflow · Policy · Audit)
- [x] Versioned contracts · event-mesh · resilience · drift law
- [x] Integration Platform boundary preserved explicitly
- [x] No ungated integration mutations · no dual-write connector tables
- [x] P292 MEAPIE delivered · P293 MEESIE delivered · P294 stub announced
