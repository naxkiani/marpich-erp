# ADR 602 — Enterprise Autonomous Scientific Research & Discovery Intelligence Platform (P242)

## Status
Accepted

## Context
P241 established EAJLIREP (legal intelligence). P242 opens the Enterprise Autonomous Scientific Research & Discovery Intelligence Platform (EASRDIP) for research projects, hypothesis generation, experiment/simulation intelligence, knowledge discovery and scientific collaboration assist under MEOS 11.0. P223 remains innovation/knowledge-evolution SoR; P234 remains education SoR; P217/biotechnology remain bio peers — EASRDIP is scientific discovery intelligence only and must never execute ungated wet-lab actuation or publish binding claims without ethics and human authority.

## Decision
1. SoR `scientific_intelligence`; fabric `meos_enterprise_autonomous_scientific_research_discovery_intelligence_platform_framework`; API `/api/v1/scientific-intelligence*`; capability `CAP-PLT-EASRDIP-001`.
2. Ten logical BCs inside one SoR: Scientific Research Management, Knowledge Discovery, Experiment Management, Simulation Intelligence, Scientific Collaboration, Research Analytics, Innovation Management, Publication Intelligence, Research Governance, Discovery Evolution.
3. Federate with P223, P234, P217/biotechnology, P228, P227, P229, P224, P230, P241, Documents via ACL/events — never replace them; never merge hospital/clinic clinical SoRs.
4. Inference only via P214-Z; wet-lab execute via Workflow + ethics + Integration lab adapters; publications via Document Exchange IDs; simulation ≠ wet-lab; subject privacy via P230.
5. Never ungated instrument/LIMS SDKs in domain; never module-local LLM; never document blobs in schema; never silent consent override; never opaque unexplainable scientific claims.
6. Roadmap: P242 foundation → P242-A…D (scientific domain → AI/KG/twin → autonomous assist → civilization-scale gated discovery intel).

## Consequences
Positive: governed research control-tower intelligence federated with innovation, education and bio peers.  
Negative: innovation portfolios, LMS outcomes, clinical bio SoRs and document binaries remain peer-owned — EASRDIP stores research models, hypotheses, experiment plans and peer/document refs only.

## Links
Law: `ENTERPRISE_AUTONOMOUS_SCIENTIFIC_RESEARCH_DISCOVERY_INTELLIGENCE_PLATFORM.md` · Prior: ADR 601 · Next: P242-A · Peer: ADR 603 (P243 EAIVIP)
