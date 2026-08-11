# ADR 649 — MEOS Enterprise API Management, Service Gateway & Digital Integration Experience Platform (MEAPIE)

- **Status:** Accepted
- **Date:** 2026-08-11
- **Deciders:** Chief Enterprise Architect · MEOS Architecture Board
- **Tags:** meos · p292 · meapie · api-management · api-gateway · developer-portal · api-product · productization
- **Related:** [ADR 648](648-meos-enterprise-integration-architecture-event-mesh-interoperability-intelligence-platform.md) · [ADR 650](650-meos-enterprise-event-streaming-intelligence-realtime-event-platform-event-product-marketplace.md) · [ADR 651](651-meos-enterprise-notification-communication-omnichannel-event-experience-platform.md) · [ADR 646](646-meos-enterprise-application-architecture-api-governance-software-architecture-intelligence-platform.md) · [ADR 647](647-meos-enterprise-data-architecture-master-data-information-architecture-intelligence-platform.md) · [Law P292](../architecture/ENTERPRISE_MEOS_API_MANAGEMENT_SERVICE_GATEWAY_DIGITAL_INTEGRATION_EXPERIENCE_PLATFORM.md) · [INTEGRATION_PLATFORM.md](../architecture/INTEGRATION_PLATFORM.md) · Governance Standard 11.0

## Context

MEOS needs a specialized **API Management / Service Gateway / API Product Experience** productization layer — without replacing Application Architecture API Governance (P289), Integration/Event Mesh (P291), Event Product/Streaming Experience (P293), Integration Platform connector execution, Data Mesh (P263), Secrets, or financial billing peers (P278/P279/P271), and without ungated external API exposure or plaintext credentials.

## Decision

1. Establish SoR **`api_management_operating`** as MEAPIE fabric under API **`/api/v1/api-management-operating*`**, schema **`api_management_operating_*`**.
2. Capability **`CAP-PLT-MEAPIE-001`**; fabric id **`meos_enterprise_api_management_service_gateway_digital_integration_experience_platform_framework`**.
3. **Boundary law (hard):**
   - **P289** = Application / Software Architecture / API Governance (*architectural ownership*)
   - **P291** = Enterprise Integration / Event Mesh / Interoperability
   - **P292** = API Management / Service Gateway / API Product Experience
   - **P293** = Event / Streaming / Real-Time Event Product Experience (delivered; distinct)
   - **P294** = Notification / Omnichannel Experience (delivered; distinct)
   - **P295** = Experience Personalization / Journey / Interaction (next)
   - Never replace Integration Platform · P263 · Secrets · Observability · financial billing SoRs
4. Federate-by-contract: P289, P291, Integration Platform, Secrets, Observability, Identity, P262, P268, P269, P270, P287, Workflow, Policy — never fork peer APIs; never dual-write connector or GL/AR tables; never local metrics stores; never plaintext credentials.
5. API contracts, versions, products and gateway policies are **versioned, explainable, reproducible, auditable**. Material publish/external activate/credential revoke require **Policy + Risk + Approval + Verification + Audit** (or published Autonomy Threshold).
6. No External API without Identity + Authorization; no Production API without Contract Governance; no Breaking Change without Impact Analysis.
7. Monetization meters usage; billing/AR only via P278/P279/P271 ACL.
8. **No AI Agent may execute uncontrolled API gateway mutations outside Policy + Delegation Authority.** Simulation ≠ execute.
9. Inference → **P214-Z** only; no module-local LLM.

## Consequences

- Unlocks Phase 1–5 MEAPIE roadmap (P292-A…E); **P293** MEESIE and **P294** MENCOE delivered; **P295** Experience Personalization series unblocked.
- P289 remains architectural API ownership; P291 remains integration/event-mesh; MEAPIE owns gateway experience, products, marketplace and consumption governance.
- Ungated external API exposure or merging P289+P291+P292+P293 SoRs is an architecture failure.

## Alternatives considered

| Alternative | Rejected because |
|-------------|------------------|
| Embed API Management inside P289 App Architecture | Violates architecture ownership vs product/gateway experience split |
| Embed API Gateway OS inside P291 Event Mesh | Violates integration mesh vs API product experience split |
| Store API keys in module tables | Violates Secrets Platform law |
| Dual-write usage into AR/GL | Violates Financial Kernel / P278–P279/P271 |
| Ungated agent publish/external activate | Violates human API governance |

## Compliance checklist

- [x] DDD · CQRS · events · hexagonal boundaries documented
- [x] Peer federation matrix (P289 · P291 · Integration Platform · Secrets · Observability · Workflow · Policy · Audit)
- [x] Versioned contracts · gateway · product/DX · no plaintext secrets · no dual-write billing
- [x] P289 · P291 · Integration Platform boundaries preserved explicitly
- [x] No ungated external API exposure
- [x] P293 MEESIE · P294 MENCOE delivered · P295 stub announced
