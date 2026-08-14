# ADR 621 — MEOS Enterprise Knowledge Graph & Semantic Intelligence Platform (P264)

## Status
Accepted

## Context
P263 established MEDIMOP over P229 data mesh. P264 productizes Knowledge Graph and Semantic Intelligence as the MEOS Cognitive Knowledge Operating Layer. P228 EKGSIP already owns `knowledge_graph` and `/api/v1/knowledge-graph*`; Enterprise Search owns query/index execution. MEKGSI must federate those SoRs — never fork the KG API, never stand up a second graph SoR, and never bypass Search for enterprise discovery. P265 is planned for Digital Twin Intelligence productization over P227.

## Decision
1. SoR `semantic_knowledge`; fabric `meos_enterprise_knowledge_graph_semantic_intelligence_operating_platform_framework`; API `/api/v1/semantic-knowledge*`; capability `CAP-PLT-MEKGSI-001`; acronym **MEKGSI**.
2. Logical BCs inside one SoR: Knowledge Management operating, Semantic Intelligence, Enterprise Memory, Ontology Evolution, Semantic Search Experience, Knowledge Governance.
3. Federate with P228, Search, P229/P263, P227, P261, P262, P257–P260, P214-Z, Documents, Policy, Audit — never replace them; never dual-write `knowledge_graph_*`; never module-local graph DB or search engine.
4. Inference only via P214-Z; explainability mandatory for gated reasoning; inference ≠ execute; ontology publish via Validate + Workflow.
5. Roadmap: P264 foundation → P264-A…D; unblocks P265.

## Consequences
Positive: governed Knowledge OS (explorer, reasoning, memory) over canonical KG.  
Negative: graph/ontology truth remains P228-owned — MEKGSI stores operating campaigns, sessions, projections and peer refs only.

## Links
Law: `ENTERPRISE_MEOS_KNOWLEDGE_GRAPH_SEMANTIC_INTELLIGENCE_PLATFORM.md` · Prior: ADR 620 · Next: P264-A · Peer: ADR 622 (P265 MEDTIP) · Canonical: P228 EKGSIP
