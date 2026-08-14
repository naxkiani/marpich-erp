# ADR 664 — MEOS Enterprise Knowledge-Centered Service, Enterprise Knowledge Management & Organizational Learning Platform (MEKNOL)

- **Status:** Accepted
- **Date:** 2026-08-11
- **Deciders:** Chief Enterprise Architect · MEOS Architecture Board
- **Tags:** meos · p307 · meknol · knowledge · kcs · organizational-learning · ai-grounding · lessons-learned · productization
- **Related:** [ADR 663](663-meos-enterprise-it-service-management-service-catalog-request-fulfillment-enterprise-service-operations-platform.md) · [ADR 621](621-meos-enterprise-knowledge-graph-semantic-intelligence-platform.md) · [Law P307](../architecture/ENTERPRISE_MEOS_KNOWLEDGE_CENTERED_SERVICE_ENTERPRISE_KNOWLEDGE_MANAGEMENT_ORGANIZATIONAL_LEARNING_PLATFORM.md) · Governance Standard 11.0

## Context

MEOS needs a specialized **Knowledge-Centered Service / Enterprise Knowledge Management / Organizational Learning** productization layer — without replacing Knowledge Graph & Semantic Intelligence (**P264/P228**), Enterprise Search, Agent Orchestration (**P266**), Incident Management (**P305**), Service Operations (**P306**), Document Exchange, Governance (**P270**), or creating parallel graph/search/agent engines — while converting operational experience into governed, reusable knowledge for humans and AI.

## Decision

1. Establish SoR **`knowledge_operating`** as MEKNOL fabric under API **`/api/v1/knowledge-operating*`**, schema **`knowledge_operating_*`**.
2. Capability **`CAP-PLT-MEKNOL-001`**; fabric id **`meos_enterprise_knowledge_centered_service_enterprise_knowledge_management_organizational_learning_platform_framework`**.
3. **Boundary law (hard):**
   - **P307** = Knowledge Lifecycle · Governance Experience · Discovery Experience · Quality/Trust · Lessons · AI Grounding packs
   - **P264 / P228** = Knowledge Graph · Semantic Intelligence · Ontology (never fork)
   - **Enterprise Search** = Search execution (never local search)
   - **P306** = Service Operations · **P305** = Incident · **P266** = Agent Orchestration · **P270** = Governance authority
   - **P308** = Document / Content Intelligence (delivered)
   - **P309** = Records / Retention / Legal Hold / ILM (delivered)
   - **P310** = Information Classification / Sensitive Information Intelligence (delivered)
   - **P311** = DLP / Information Protection / Adaptive Data Security Control (next)
4. Federate-by-contract: P264/P228, Search, P266, P305, P306, P299–P304, P270, P294, Documents, P214-Z, Policy, Workflow — never dual-write `knowledge_graph_*`; never embed local LLM; never local search/metrics/approval engines.
5. Knowledge items are **versioned, classified, tenant-scoped, explainable, auditable** with Trust/Quality scores and source attribution.
6. P307 may Author · Validate · Publish · Discover · Ground AI · Learn — and must **NOT** Own graph/search/agent/workflow/incident/service-ops/document-blob engines.
7. AI-generated knowledge must **never** become authoritative automatically; human governance mandatory for authoritative publication.
8. Communications via **P294** only; attachments via **Documents** (`document_id` only).
9. Inference → **P214-Z** only; no module-local LLM.
10. Document OCR/content intelligence deepens in **P308**.

## Consequences

- Unlocks Phase 1–10 MEKNOL roadmap (P307-A…J); **P308** MEDCIM delivered; **P309** Records / Retention / Legal Hold / ILM series unblocked.
- P264/P228 remain graph authority; Search remains query authority; P266 remains agent orchestration; MEKNOL owns knowledge lifecycle and organizational learning experience.
- Forking graph/search SoRs or auto-publishing AI drafts as authoritative knowledge is an architecture failure.

## Alternatives considered

| Alternative | Rejected because |
|-------------|------------------|
| Embed knowledge lifecycle inside P264 | Violates semantic/graph vs knowledge-lifecycle split |
| Module-local search or graph DB | Violates Search / P228 / P264 ownership |
| Auto-authoritative AI knowledge | Violates Human-in-the-Loop / Responsible AI |
| Merge into P306 service knowledge only | Violates enterprise knowledge OS vs service ops split |
| Store document blobs in knowledge tables | Violates Document Exchange law |

## Compliance checklist

- [x] DDD · CQRS · events · hexagonal boundaries documented
- [x] Peer federation matrix (P264/P228 · Search · P266 · P305 · P306 · P270 · Documents · Workflow · Policy · Audit)
- [x] Lifecycle/experience only · no local LLM · no graph/search fork
- [x] P264 · Search · P266 · P305 · P306 boundaries preserved explicitly
- [x] Version traceability · source attribution · human approval for authoritative · tenant isolation
- [x] P308 MEDCIM · P309 MERILG · P310 MEIGSI delivered · P311 stub announced
