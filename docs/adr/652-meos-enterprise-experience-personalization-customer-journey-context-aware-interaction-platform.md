# ADR 652 — MEOS Enterprise Experience Personalization, Customer Journey & Context-Aware Interaction Platform (MEEPJI)

- **Status:** Accepted
- **Date:** 2026-08-11
- **Deciders:** Chief Enterprise Architect · MEOS Architecture Board
- **Tags:** meos · p295 · meepji · experience · personalization · journey · context · nba · productization
- **Related:** [ADR 651](651-meos-enterprise-notification-communication-omnichannel-event-experience-platform.md) · [ADR 650](650-meos-enterprise-event-streaming-intelligence-realtime-event-platform-event-product-marketplace.md) · [ADR 653](653-meos-enterprise-conversational-voice-multimodal-interaction-intelligence-platform.md) · [Law P295](../architecture/ENTERPRISE_MEOS_EXPERIENCE_PERSONALIZATION_CUSTOMER_JOURNEY_CONTEXT_AWARE_INTERACTION_PLATFORM.md) · Governance Standard 11.0

## Context

MEOS needs a specialized **Experience / Journey / Personalization / Interaction** productization layer — without replacing Communication Delivery (P294/Notifications), Event Streaming Intelligence (P293), Event Transport (P291), Workflow Execution (P260), Application Shell (P258), Conversational/Voice/Multimodal Interaction (P296), or Identity/Customer/HR systems of record, and without ungated personalization mutations or unexplained AI recommendations.

## Decision

1. Establish SoR **`experience_personalization_operating`** as MEEPJI fabric under API **`/api/v1/experience-personalization-operating*`**, schema **`experience_personalization_operating_*`**.
2. Capability **`CAP-PLT-MEEPJI-001`**; fabric id **`meos_enterprise_experience_personalization_customer_journey_context_aware_interaction_platform_framework`**.
3. **Boundary law (hard):**
   - **P293** = Event / Streaming / Event Intelligence
   - **P294** = Notification / Communication / Omnichannel Delivery
   - **P295** = Experience / Journey / Personalization / Interaction
   - **P296** = Conversational / Voice / Multimodal Interaction (delivered; distinct)
   - **P297** = Human-AI Collaboration / Agentic Workspace (delivered; distinct)
   - Never replace P260 Workflow · P258 Application Shell · Identity/Customer/HR SoRs · P291–P292
4. Experience Profile is **Experience Context only** — never an uncontrolled duplicate of Identity, Customer, or HR masters.
5. Federate-by-contract: P294, P293, P258, P260, P261, P262, Identity, P264–P270, Policy, Workflow — never implement channel delivery; never dual-write notification/identity/customer/HR tables; never local metrics/approval/workflow engines.
6. Experience definitions, variants, journeys and personalization rules are **versioned, explainable, reproducible, auditable**. Material activate/personalize/NBA execute/variant promote require **Policy + Consent (where required) + Risk + Approval + Verification + Audit** (or published Autonomy Threshold).
7. No Personalization without Policy; no Sensitive Context without Privacy Validation; no sensitive AI Recommendation without Governance; AI scores expose Confidence + Evidence + Model Version.
8. Communication Intent → P294 only; executable workflows → P260 only; shell personalization → P258 contracts only.
9. **No AI Agent may execute uncontrolled experience mutations outside Policy + Privacy + Consent + Delegation Authority.** Simulation ≠ execute.
10. Inference → **P214-Z** only; no module-local LLM.

## Consequences

- Unlocks Phase 1–6 MEEPJI roadmap (P295-A…F); **P296** MECVII · **P297** MEAWHC · **P298** MEAPAE · **P299** MEPICO · **P300** MEPAMP · **P301** MEPCVA · **P302** MEPQDV · **P303** MEPRED · **P304** MEPOCI · **P305** MEIRRE · **P306** MEESOP · **P307** MEKNOL · **P308** MEDCIM · **P309** MERILG · **P310** MEIGSI delivered; **P311** DLP / Information Protection / Adaptive Data Security Control series unblocked.
- P294 remains delivery; P260 remains workflow execution; MEEPJI owns experience context, journeys, personalization, NBA/NBE and interaction intelligence.
- Ungated personalization or merging P293–P303 SoRs is an architecture failure.

## Alternatives considered

| Alternative | Rejected because |
|-------------|------------------|
| Embed Experience OS inside P294 Communication | Violates delivery vs experience decision split |
| Embed journeys as a second Workflow Engine | Violates P260 ownership |
| Duplicate Customer/Identity profiles as SoR | Violates platform charter / master data ownership |
| Direct Email/SMS/Push from experience domain | Violates Notification / Integration laws |
| Ungated AI NBA execution | Violates Human Governance · Consent · Policy |

## Compliance checklist

- [x] DDD · CQRS · events · hexagonal boundaries documented
- [x] Peer federation matrix (P294 · P293 · P258 · P260 · Identity · P269 · Workflow · Policy · Audit)
- [x] Experience Profile context-only · gated personalize/NBA · no channel delivery
- [x] P258 · P260 · P293 · P294 boundaries preserved explicitly
- [x] No ungated personalization · AI explainability required
- [x] P296 MECVII · P297 MEAWHC · P298 MEAPAE · P299 MEPICO · P300 MEPAMP · P301 MEPCVA · P302 MEPQDV delivered · P303 stub announced
