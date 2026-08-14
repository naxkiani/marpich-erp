# ADR 666 — MEOS Enterprise Records, Retention, Legal Hold & Information Lifecycle Governance Platform (MERILG)

- **Status:** Accepted
- **Date:** 2026-08-11
- **Deciders:** Chief Enterprise Architect · MEOS Architecture Board
- **Tags:** meos · p309 · merilg · records · retention · legal-hold · disposition · evidence · information-lifecycle · productization
- **Related:** [ADR 665](665-meos-enterprise-document-intelligence-content-lifecycle-intelligent-information-management-platform.md) · [Law P309](../architecture/ENTERPRISE_MEOS_RECORDS_RETENTION_LEGAL_HOLD_INFORMATION_LIFECYCLE_GOVERNANCE_PLATFORM.md) · Document Exchange · Governance Standard 11.0

## Context

MEOS needs a specialized **Records / Retention / Legal Hold / Information Lifecycle Governance** productization layer — without replacing Document Intelligence (**P308**), Document Exchange (blob SoR), Knowledge OS (**P307**), Knowledge Graph (**P264/P228**), Governance Policy (**P270**), Workflow (**P260**), Agent Orchestration (**P266**), or creating a Legal Case Management / parallel disposition engine — while making every governed record defensible across retention, hold, preservation, and disposition.

## Decision

1. Establish SoR **`records_lifecycle_operating`** as MERILG fabric under API **`/api/v1/records-lifecycle-operating*`**, schema **`records_lifecycle_operating_*`**.
2. Capability **`CAP-PLT-MERILG-001`**; fabric id **`meos_enterprise_records_retention_legal_hold_information_lifecycle_governance_platform_framework`**.
3. **Boundary law (hard):**
   - **P308** = CONTENT · Document Lifecycle · Document Intelligence
   - **P309** = RECORD LIFECYCLE · Retention · Legal Hold · Preservation · Disposition · Evidence
   - **Documents** = Document Exchange blob/version SoR (`document_id` / source content refs)
   - **P270** = Governance/Policy · **P260** = Workflow · **P266** = Agents
   - **P307** = Knowledge · **P264/P228** = Semantic/Graph
   - **P310** = Information Classification / Sensitive Information Intelligence (delivered)
   - **P311** = DLP / Information Protection / Adaptive Data Security Control (next)
4. Federate-by-contract: P308, Documents, P270, P260, P266, P294, P304, P305, P307, P214-Z, Policy — never dual-write P308/Documents tables as second SoR; never embed local LLM; never local policy/workflow engines.
5. Records are **tenant-scoped, classified, retention-scheduled, hold-aware, integrity-hashed, custody-traced, auditable**; disposition requires eligibility + no hold + policy + human authorization.
6. Conflict priority: **Legal Hold > Regulatory Preservation > Investigation > Governance Exception > Retention Policy > Ordinary Disposition**.
7. P309 may Declare · Classify · Schedule · Hold · Preserve · Dispose · Certify · Package Evidence — and must **NOT** Own content intelligence · Own blob SoR · Own knowledge/graph/agent/workflow/governance engines · Become Legal Case Management.
8. AI must never autonomously release holds, approve disposition, override retention, delete records, bypass governance, or alter custody/evidence.
9. Communications via **P294** only; inference → **P214-Z** only.
10. Sensitive information classification / DLP coordination specialization deepens in **P310**.

## Consequences

- Unlocks Phase 1–9 MERILG roadmap (P309-A…I); **P310** MEIGSI delivered; **P311** DLP / Information Protection / Adaptive Data Security Control series unblocked.
- P308 remains content; P270 remains policy; P260 remains workflow; MERILG owns records/ILM productization.
- Forking P308 content SoR, disposing under Legal Hold, or autonomous destruction is an architecture failure.

## Alternatives considered

| Alternative | Rejected because |
|-------------|------------------|
| Keep all ILM forever inside P308 only | Violates content vs records specialization |
| Embed disposition policy engine in P309 | Violates P270 governance authority |
| Local approval workflow for disposition | Violates P260 workflow law |
| Auto-dispose on retention expiry | Violates Human-in-the-Loop + Legal Hold |
| Become Legal Case Management | Out of MEOS records/ILM boundary |
| Merge sensitive classification into P309 forever | P310 specializes information classification |

## Compliance checklist

- [x] DDD · CQRS · events · hexagonal boundaries documented
- [x] Peer federation matrix (P308 · Documents · P270 · P260 · P266 · P294 · P307 · P264)
- [x] No local LLM · no parallel policy/workflow/graph engines
- [x] P308 · P270 · P260 · Documents boundaries preserved explicitly
- [x] Defensible disposition · hold override · no autonomous destruction
- [x] P310 MEIGSI delivered · P311 stub announced
