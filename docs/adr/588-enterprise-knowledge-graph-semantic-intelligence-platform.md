# ADR 588 — Enterprise Knowledge Graph & Semantic Intelligence Platform (P228)

## Status
Accepted

## Context
P227 established EDTISP (digital twin intelligence & simulation). P228 opens the Enterprise Knowledge Graph & Semantic Intelligence Platform (EKGSIP) as the MEOS foundational semantic layer for knowledge representation, ontology, relationship discovery, reasoning and enterprise memory. Search remains the enterprise search SoR; P219-I and P223 remain civilization/innovation knowledge SoRs — EKGSIP federates them into a governed graph fabric.

## Decision
1. SoR `knowledge_graph`; fabric `meos_enterprise_knowledge_graph_semantic_intelligence_platform_framework`; API `/api/v1/knowledge-graph*`; capability `CAP-PLT-EKGSIP-001`.
2. Ten logical BCs inside one SoR: Knowledge Management, Semantic Modeling, Ontology Governance, Entity Management, Relationship Intelligence, Knowledge Discovery, Reasoning Services, Governance, Enterprise Memory, Intelligence Federation.
3. Federate with Search, Documents, P219-I, P223, P227, P224, P213 via ACL/events — never replace them.
4. Inference only via P214-Z; graph ingest via integration events only; search via Search Platform; blobs via Documents; policy via Policy Engine; audit via Audit.
5. Never module-local LLM/search; never cross-schema SQL for graph build; never fail-open graph reads; never document blobs in graph tables.
6. Roadmap: P228 foundation → P228-A…D (graph core → AI/ontology → federation → civilization-scale gated evolution).

## Consequences
Positive: trusted semantic network for agents and autonomous platforms.  
Negative: query UX and permission ranking remain Search-owned; peer SoRs remain authoritative for domain knowledge — EKGSIP stores graph projections and ontologies with peer refs only.

## Links
Law: `ENTERPRISE_KNOWLEDGE_GRAPH_SEMANTIC_INTELLIGENCE_PLATFORM.md` · Prior: ADR 587 · Next: P228-A · Peer: ADR 589 (P229 EFDMIFP)
