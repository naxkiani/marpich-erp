# ADR 601 — Enterprise Autonomous Justice, Legal Intelligence & Regulatory Evolution Platform (P241)

## Status
Accepted

## Context
P240 established EAGDGIP (governance intelligence). P241 opens the Enterprise Autonomous Justice, Legal Intelligence & Regulatory Evolution Platform (EAJLIREP) for legal analysis, regulatory monitoring, contract intelligence, dispute assist and regulatory evolution tracking under MEOS 11.0. P240 remains institutional/digital governance SoR; Compliance Platform remains violation SoR; Policy Engine remains rule-evaluation SoR; Document Exchange remains document SoR — EAJLIREP is legal intelligence only and must never issue binding legal judgments or filings without human authority.

## Decision
1. SoR `legal_intelligence`; fabric `meos_enterprise_autonomous_justice_legal_intelligence_regulatory_evolution_platform_framework`; API `/api/v1/legal-intelligence*`; capability `CAP-PLT-EAJLIREP-001`.
2. Ten logical BCs inside one SoR: Legal Management, Regulatory Intelligence, Contract Management, Compliance Management, Dispute Management, Justice Analytics, Legal Knowledge, Evidence Management, Policy Interpretation, Legal Governance.
3. Federate with P240, Compliance, Policy Engine, Documents, P230, P224, P226, P227, P228, P229, government/municipality via ACL/events — never replace them.
4. Inference only via P214-Z; binding decide/file via Workflow + human legal authority + owning SoRs; contract/evidence blobs via Document Exchange IDs only; simulation ≠ decide.
5. Never local compliance violation stores; never fork Policy Engine evaluate; never PDF/binary in domain tables; never module-local LLM; never opaque unexplainable legal advice; never bypass privilege/privacy gates.
6. Roadmap: P241 foundation → P241-A…D (legal domain → AI/KG/twin → autonomous assist → civilization-scale gated legal intel).

## Consequences
Positive: governed legal control-tower intelligence federated with governance, compliance and document peers.  
Negative: courts of record, violations, rule evaluation and document binaries remain peer-owned — EAJLIREP stores legal models, analyses and peer/document refs only.

## Links
Law: `ENTERPRISE_AUTONOMOUS_JUSTICE_LEGAL_INTELLIGENCE_REGULATORY_EVOLUTION_PLATFORM.md` · Prior: ADR 600 · Next: P241-A · Peer: ADR 602 (P242 EASRDIP)
