# ADR 653 — MEOS Enterprise Conversational, Voice & Multimodal Interaction Intelligence Platform (MECVII)

- **Status:** Accepted
- **Date:** 2026-08-11
- **Deciders:** Chief Enterprise Architect · MEOS Architecture Board
- **Tags:** meos · p296 · mecvii · conversational · voice · multimodal · dialogue · rag · productization
- **Related:** [ADR 652](652-meos-enterprise-experience-personalization-customer-journey-context-aware-interaction-platform.md) · [ADR 651](651-meos-enterprise-notification-communication-omnichannel-event-experience-platform.md) · [Law P296](../architecture/ENTERPRISE_MEOS_EXPERIENCE_INTELLIGENCE_VOICE_CONVERSATIONAL_MULTIMODAL_INTERACTION_PLATFORM.md) · [AI_PLATFORM_STANDARD.md](../architecture/AI_PLATFORM_STANDARD.md) · Governance Standard 11.0

## Context

MEOS needs a specialized **Conversational / Voice / Multimodal Interaction** productization layer — without replacing Communication Delivery (P294), Experience Personalization (P295), Workflow Execution (P260), AI Agent Orchestration (P266), Application Shell (P258), or API Management (P292), and without ungated tool invocations, ungrounded “facts”, or module-local LLMs.

## Decision

1. Establish SoR **`conversational_interaction_operating`** as MECVII fabric under API **`/api/v1/conversational-interaction-operating*`**, schema **`conversational_interaction_operating_*`**.
2. Capability **`CAP-PLT-MECVII-001`**; fabric id **`meos_enterprise_conversational_voice_multimodal_interaction_intelligence_platform_framework`**.
3. **Boundary law (hard):**
   - **P294** = Communication / Notification Delivery
   - **P295** = Experience / Journey / Personalization
   - **P296** = Conversational / Voice / Multimodal Interaction
   - **P297** = Human-AI Collaboration / Agentic Workspace (next)
   - **P260** = Workflow Execution · **P266** = AI Agent Orchestration — **never replace**
4. Federate-by-contract: P266, P260, P295, P294, P258, P257, Search, Documents, P263–P270, P214-Z, Policy, Workflow — never dual-write workflow/agent/notification tables; never embed provider/LLM SDKs in domain; never local metrics/approval engines.
5. Conversations, voice sessions, multimodal interactions and tool invocations are **versioned, explainable, reproducible, auditable**. Material tool/workflow/enterprise actions require **Authorization + Policy + Confirmation (when required) + Verification + Audit** (or published Autonomy Threshold).
6. AI must distinguish Known / Retrieved / Calculated / Inference / Recommendation; grounded answers preserve Source Traceability + Evidence + Confidence + Model Version.
7. Document/media via `document_id` / media refs only; memory governed by Privacy · Retention · Consent · Tenant Isolation.
8. Communication Intent → P294 only; agent execution → P266 only; workflows → P260 only; navigation → P258 contracts only.
9. **No AI Agent may execute uncontrolled conversational actions outside Policy + Authorization + Confirmation + Audit.** Simulation ≠ execute.
10. Inference → **P214-Z** only; no module-local LLM.

## Consequences

- Unlocks Phase 1–7 MECVII roadmap (P296-A…G) and **P297** Human-AI Collaboration / Agentic Workspace series.
- P266 remains agent orchestration; P260 remains workflow; P294 remains delivery; P295 remains experience; MECVII owns conversational/voice/multimodal interaction and tool-interaction interface.
- Ungated tool/action execution or merging P294–P297 SoRs is an architecture failure.

## Alternatives considered

| Alternative | Rejected because |
|-------------|------------------|
| Embed Conversation OS inside P266 Agent Orchestration | Violates agent orchestration vs interaction interface split |
| Embed voice/multimodal inside P295 Experience | Violates experience vs conversational interaction split |
| Direct Email/SMS/Push from conversation domain | Violates Notification Platform law |
| Local LLM / STT SDKs in domain | Violates AI Platform / Integration / P214-Z law |
| Present inference as verified fact | Violates Responsible AI · Explainability |

## Compliance checklist

- [x] DDD · CQRS · events · hexagonal boundaries documented
- [x] Peer federation matrix (P266 · P260 · P295 · P294 · P258 · Search · Documents · P269 · Workflow · Policy · Audit)
- [x] Grounding · confirmation gates · no channel delivery · no local LLM
- [x] P258 · P260 · P266 · P294 · P295 boundaries preserved explicitly
- [x] No ungated tool/action · inference ≠ verified fact
- [x] P297 stub announced
