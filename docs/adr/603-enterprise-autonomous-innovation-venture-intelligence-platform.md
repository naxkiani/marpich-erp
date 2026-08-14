# ADR 603 — Enterprise Autonomous Innovation & Venture Intelligence Platform (P243)

## Status
Accepted

## Context
P242 established EASRDIP (scientific research intelligence). P243 opens the Enterprise Autonomous Innovation & Venture Intelligence Platform (EAIVIP) for opportunity discovery, venture creation, portfolio/investment intelligence and transformation assist under MEOS 11.0. P223 EGIKEP already owns SoR `innovation` and `/api/v1/innovation*` — EAIVIP must not fork that SoR. EAIVIP is venture/opportunity/commercialization intelligence only and must never post local GL or launch binding ventures without human authority.

## Decision
1. SoR `venture_intelligence` (not `innovation`); fabric `meos_enterprise_autonomous_innovation_venture_intelligence_platform_framework`; API `/api/v1/venture-intelligence*`; capability `CAP-PLT-EAIVIP-001`.
2. Ten logical BCs inside one SoR: Innovation Management (venture lens), Opportunity Intelligence, Venture Creation, Idea Management, Market Intelligence, Investment Intelligence, Ecosystem Management, Technology Intelligence, Transformation Management, Innovation Governance.
3. Federate with P223, P242, P231, Financial Kernel, P234, P224, P228, P227, P229, P241 via ACL/events — never replace them; never dual-write P223 tables; never fork `/api/v1/innovation*`.
4. Inference only via P214-Z; invest/launch via Workflow + Financial Kernel/P231; simulation ≠ invest/launch; market feeds via Integration Platform.
5. Never local JournalEntry/GL; never module-local LLM; never opaque unexplainable investment recommendations; never ungated capital deployment.
6. Roadmap: P243 foundation → P243-A…D (venture domain → AI/KG/twin → autonomous assist → civilization-scale gated venture intel).

## Consequences
Positive: governed venture control-tower intelligence federated with innovation, research and finance peers.  
Negative: canonical innovation/knowledge-evolution aggregates and capital ledgers remain peer-owned — EAIVIP stores venture/opportunity models and peer refs only.

## Links
Law: `ENTERPRISE_AUTONOMOUS_INNOVATION_VENTURE_INTELLIGENCE_PLATFORM.md` · Prior: ADR 602 · Next: P243-A · Peer: ADR 604 (P244 EAFIEEP)
