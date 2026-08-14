# ADR 665 — MEOS Enterprise Document Intelligence, Content Lifecycle & Intelligent Information Management Platform (MEDCIM)

- **Status:** Accepted
- **Date:** 2026-08-11
- **Deciders:** Chief Enterprise Architect · MEOS Architecture Board
- **Tags:** meos · p308 · medcim · document-intelligence · content-lifecycle · idp · ocr · records-foundation · productization
- **Related:** [ADR 664](664-meos-enterprise-knowledge-centered-service-enterprise-knowledge-management-organizational-learning-platform.md) · [Law P308](../architecture/ENTERPRISE_MEOS_DOCUMENT_INTELLIGENCE_CONTENT_LIFECYCLE_INTELLIGENT_INFORMATION_MANAGEMENT_PLATFORM.md) · Document Exchange · Governance Standard 11.0

## Context

MEOS needs a specialized **Document Intelligence / Content Lifecycle / Intelligent Information Management** productization layer — without replacing Document Exchange (blob/version SoR), Knowledge OS (**P307**), Knowledge Graph (**P264/P228**), Enterprise Search, Agent Orchestration (**P266**), Workflow (**P260**), Governance (**P270**), or creating vendor-locked storage / parallel knowledge / graph engines — while converting enterprise content into governed, discoverable, knowledge-ready information.

## Decision

1. Establish SoR **`document_intelligence_operating`** as MEDCIM fabric under API **`/api/v1/document-intelligence-operating*`**, schema **`document_intelligence_operating_*`**.
2. Capability **`CAP-PLT-MEDCIM-001`**; fabric id **`meos_enterprise_document_intelligence_content_lifecycle_intelligent_information_management_platform_framework`**.
3. **Boundary law (hard):**
   - **P308** = CONTENT · Document Lifecycle · Document Intelligence · Discovery · Collaboration · Knowledge Candidates
   - **Documents** = Document Exchange blob/version SoR (`document_id` / storage abstraction)
   - **P307** = KNOWLEDGE publication · **P264/P228** = Semantic/Graph · **Search** = query execution
   - **P260** = Workflow · **P266** = Agents · **P270** = Governance/Policy
   - **P309** = Records / Retention / Legal Hold / ILM specialization (delivered)
   - **P310** = Information Classification / Sensitive Information Intelligence (delivered)
   - **P311** = DLP / Information Protection / Adaptive Data Security Control (next)
4. Federate-by-contract: Documents, P307, P264/P228, Search, P260, P266, P270, P294, P305–P306, P214-Z, Policy — never dual-write Documents blob tables as second SoR; never embed local LLM; never local search/graph; never vendor-lock storage in domain.
5. Documents are **versioned, classified, tenant-scoped, integrity-hashed, auditable**; published versions immutable.
6. P308 may Ingest · Understand · Classify · Coordinate lifecycle · Discover · Collaborate · Emit knowledge candidates — and must **NOT** Own blob SoR · Own knowledge publication · Own graph/search/agent/workflow/governance engines.
7. AI-generated insights clearly identified; AI retrieval requires Identity + Tenant + Document AuthZ + Classification + Purpose + Policy.
8. Knowledge candidates flow to **P307**; authoritative knowledge never auto-published from P308.
9. Communications via **P294** only; inference → **P214-Z** only.
10. Specialized defensible disposition / ILM analytics deepen in **P309**.

## Consequences

- Unlocks Phase 1–12 MEDCIM roadmap (P308-A…L); **P309** MERILG delivered; **P310** Information Classification / Sensitive Information Intelligence series unblocked.
- Documents remains blob SoR; P307 remains knowledge; P264 remains semantic/graph; MEDCIM owns content intelligence and lifecycle productization.
- Forking Document Exchange, auto-publishing knowledge, or disposing under Legal Hold without policy is an architecture failure.

## Alternatives considered

| Alternative | Rejected because |
|-------------|------------------|
| Embed intelligence inside Documents Exchange only | Violates blob SoR vs intelligence productization split |
| Store blobs in `document_intelligence_operating_*` | Violates Document Exchange law |
| Auto-publish knowledge from documents | Violates P307 knowledge governance |
| Vendor-locked storage in domain | Violates cloud-native replaceability |
| Merge records specialization into P308 forever | P309 specializes ILM/records governance |

## Compliance checklist

- [x] DDD · CQRS · events · hexagonal boundaries documented
- [x] Peer federation matrix (Documents · P307 · P264 · Search · P260 · P266 · P270 · Workflow · Policy · Audit)
- [x] Storage abstraction · no local LLM · no graph/search fork
- [x] Documents · P307 · P264 · P260 · P266 boundaries preserved explicitly
- [x] Immutable published versions · AuthZ for AI retrieval · no dispose under Legal Hold without policy
- [x] P309 MERILG · P310 MEIGSI delivered · P311 stub announced
