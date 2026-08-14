# ADR 667 — MEOS Enterprise Information Governance, Data Classification & Sensitive Information Intelligence Platform (MEIGSI)

- **Status:** Accepted
- **Date:** 2026-08-11
- **Deciders:** Chief Enterprise Architect · MEOS Architecture Board
- **Tags:** meos · p310 · meigsi · information-classification · sensitive-information · pii · taxonomy · exposure · productization
- **Related:** [ADR 666](666-meos-enterprise-records-retention-legal-hold-information-lifecycle-governance-platform.md) · [Law P310](../architecture/ENTERPRISE_MEOS_INFORMATION_GOVERNANCE_DATA_CLASSIFICATION_SENSITIVE_INFORMATION_INTELLIGENCE_PLATFORM.md) · Governance Standard 11.0

## Context

MEOS needs a specialized **Information Classification / Sensitive Information Intelligence** productization layer — without replacing Data Mesh (**P263**), Document Intelligence (**P308**), Records/ILM (**P309**), Cybersecurity (**P268**), Privacy (**P269**), Governance Policy (**P270**), Knowledge Graph (**P264/P228**), Workflow (**P260**), Agent Orchestration (**P266**), or creating a parallel DLP / Data Governance engine — while ensuring every governed information object is classified, sensitivity-labeled, risk-scored, and handling-requirement ready for P311 protection execution.

## Decision

1. Establish SoR **`information_classification_operating`** as MEIGSI fabric under API **`/api/v1/information-classification-operating*`**, schema **`information_classification_operating_*`**.
2. Capability **`CAP-PLT-MEIGSI-001`**; fabric id **`meos_enterprise_information_governance_data_classification_sensitive_information_intelligence_platform_framework`**.
3. **Boundary law (hard):**
   - **P310** = Classification · Sensitive Detection · Sensitivity · Taxonomy · Risk/Exposure · Handling Requirements Intelligence
   - **P308** = CONTENT · **P309** = RECORD/ILM · **P263** = Data Mesh
   - **P268** = Security Defense · **P269** = Privacy Policy · **P270** = Enterprise Governance/Policy
   - **P311** = DLP / Information Protection execution (next)
4. Federate-by-contract: P263, P308, P309, P268, P269, P270, P260, P266, P294, P304, P214-Z — never dual-write peer repository tables; never embed local LLM; never local DLP/privacy/security engines.
5. Automated classifications require **Confidence + Evidence + Method**; low confidence → Human Review; overrides/exceptions audited.
6. Propagation must never blindly lower classification; aggregation does not automatically remove sensitivity.
7. P310 may Discover · Detect · Classify · Score Risk · Emit Handling Requirements — and must **NOT** Own mesh/content/records · Own DLP execution · Own privacy/security/governance engines · Auto-downgrade sensitivity · Expose secrets via AI.
8. Communications via **P294** only; inference → **P214-Z** only.
9. Cross-tenant discovery and AI cross-tenant learning: **DENY BY DEFAULT**.
10. Operational prevent/block/quarantine/redact deepens in **P311**.

## Consequences

- Unlocks Phase 1–9 MEIGSI roadmap (P310-A…I) and **P311** DLP / Information Protection / Adaptive Data Security Control series.
- P263 remains Data Mesh; P308/P309 remain content/records; P268/P269/P270 remain security/privacy/governance; MEIGSI owns classification intelligence productization.
- Forking DLP into P310, auto-downgrading sensitivity, or AI-exposing secrets is an architecture failure.

## Alternatives considered

| Alternative | Rejected because |
|-------------|------------------|
| Embed classification forever inside P308/P309 only | Violates specialized information intelligence layer |
| Build DLP engine inside P310 | Violates P311 / P268 execution boundary |
| Replace P269 privacy with P310 rules | Violates privacy authority split (detect vs govern) |
| Local policy engine for handling | Violates P270 governance authority |
| Auto-apply classification downgrades | Violates Human-in-the-Loop + Zero Trust |
| Merge protection execution into P310 forever | P311 specializes DLP / adaptive data security |

## Compliance checklist

- [x] DDD · CQRS · events · hexagonal boundaries documented
- [x] Peer federation matrix (P263 · P308 · P309 · P268 · P269 · P270 · P260 · P266 · P264)
- [x] No local LLM · no parallel DLP/privacy/security/policy engines
- [x] Detect vs govern (P269) · intelligence vs defense (P268) preserved
- [x] Confidence + Evidence · no blind lowering · no AI secret exposure
- [x] P311 stub announced
