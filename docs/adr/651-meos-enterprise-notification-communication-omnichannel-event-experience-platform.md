# ADR 651 — MEOS Enterprise Notification, Communication & Omnichannel Event Experience Platform (MENCOE)

- **Status:** Accepted
- **Date:** 2026-08-11
- **Deciders:** Chief Enterprise Architect · MEOS Architecture Board
- **Tags:** meos · p294 · mencoe · notification · communication · omnichannel · consent · productization
- **Related:** [ADR 650](650-meos-enterprise-event-streaming-intelligence-realtime-event-platform-event-product-marketplace.md) · [ADR 649](649-meos-enterprise-api-management-service-gateway-digital-integration-experience-platform.md) · [ADR 648](648-meos-enterprise-integration-architecture-event-mesh-interoperability-intelligence-platform.md) · [ADR 652](652-meos-enterprise-experience-personalization-customer-journey-context-aware-interaction-platform.md) · [Law P294](../architecture/ENTERPRISE_MEOS_NOTIFICATION_COMMUNICATION_OMNICHANNEL_EVENT_EXPERIENCE_PLATFORM.md) · [ENTERPRISE_NOTIFICATION_PLATFORM.md](../architecture/ENTERPRISE_NOTIFICATION_PLATFORM.md) · Governance Standard 11.0

## Context

MEOS needs a specialized **Communication / Notification / Omnichannel Experience** productization layer — without replacing Notifications Platform execution (`contexts/notifications`), Event Mesh transport (P291), API Management (P292), Event Streaming Intelligence (P293), Experience Personalization (P295), Workflow (P260), Privacy/Consent (P269), or financial billing peers, and without ungated omnichannel sends or AI-generated sensitive sends without validation.

## Decision

1. Establish SoR **`communication_experience_operating`** as MENCOE fabric under API **`/api/v1/communication-experience-operating*`**, schema **`communication_experience_operating_*`**.
2. Capability **`CAP-PLT-MENCOE-001`**; fabric id **`meos_enterprise_notification_communication_omnichannel_event_experience_platform_framework`**.
3. **Boundary law (hard):**
   - **Notifications Platform** = sole notification queue/adapter execution SoR — **never replace**
   - **P291** = Event Mesh / Transport
   - **P292** = API Management
   - **P293** = Event Product / Streaming / Real-Time Intelligence
   - **P294** = Communication / Notification / Omnichannel Experience
   - **P295** = Experience Personalization / Journey / Interaction (delivered; distinct)
   - **P296** = Conversational / Voice / Multimodal Interaction (delivered; distinct)
   - **P297** = Human-AI Collaboration / Agentic Workspace (delivered; distinct)
4. Federate-by-contract: Notifications Platform, P293, P291, P292, Integration Platform, Secrets, Localization, P260, P262, P268, P269, P270, Workflow, Policy — never fork `/api/v1/notifications*`; never dual-write `notifications_*` or GL/AR; never embed provider SDKs in domain; never local metrics/approval engines.
5. Communication definitions, templates, journeys and delivery policies are **versioned, explainable, reproducible, auditable**. Material send/escalation/template publish require **Policy + Consent (where required) + Risk + Approval + Verification + Audit** (or published Autonomy Threshold).
6. No Communication without Policy; no Sensitive Communication without Security Validation; no Consent-required Communication without valid Consent; no AI-generated sensitive send without Validation + Policy + Audit.
7. Cost metering only; billing/AR via P278/P279/P271 ACL.
8. **No AI Agent may execute uncontrolled external communication outside Policy + Consent + Delegation Authority.** Simulation ≠ execute.
9. Inference → **P214-Z** only; no module-local LLM.

## Consequences

- Unlocks Phase 1–5 MENCOE roadmap (P294-A…E); **P295** MEEPJI · **P296** MECVII · **P297** MEAWHC · **P298** MEAPAE · **P299** MEPICO · **P300** MEPAMP · **P301** MEPCVA · **P302** MEPQDV · **P303** MEPRED · **P304** MEPOCI · **P305** MEIRRE · **P306** MEESOP · **P307** MEKNOL · **P308** MEDCIM · **P309** MERILG · **P310** MEIGSI delivered; **P311** DLP / Information Protection / Adaptive Data Security Control series unblocked.
- Notifications Platform remains execution SoR; MENCOE owns communication experience, orchestration overlays, journeys, preference/consent experience and delivery intelligence.
- Ungated omnichannel send or merging Notifications Platform+P291–P295 SoRs is an architecture failure.

## Alternatives considered

| Alternative | Rejected because |
|-------------|------------------|
| Embed Communication Experience inside Notifications Platform only | Violates execution vs experience productization split |
| Own Event Transport / Streaming for notifications | Violates P291/P293 ownership |
| Embed SMTP/Twilio/FCM in communication domain | Violates Integration Platform / hexagonal adapter law |
| Dual-write delivery logs into experience tables | Violates service boundary / schema isolation |
| Ungated AI agent external sends | Violates Consent · Policy · Human Governance |

## Compliance checklist

- [x] DDD · CQRS · events · hexagonal boundaries documented
- [x] Peer federation matrix (Notifications Platform · P291–P293 · Integration · Secrets · Workflow · Policy · Audit · P269)
- [x] Consent-by-design · gated send · no dual-write notifications/billing
- [x] Notifications Platform · P291–P293 boundaries preserved explicitly
- [x] No ungated omnichannel sends · no AI sensitive send without validation
- [x] P295 MEEPJI · P296 MECVII · P297 MEAWHC · P298 MEAPAE · P299 MEPICO · P300 MEPAMP · P301 MEPCVA · P302 MEPQDV delivered · P303 stub announced
