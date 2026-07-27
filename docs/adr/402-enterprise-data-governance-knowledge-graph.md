# ADR-402: Data Governance — Data Intelligence Knowledge Graph (P212-J)

## Status

Accepted — P212-J Data Intelligence Knowledge Graph Platform

## Context

ADR-392–393 and ADR-397–401 established SoR `data_governance` through ownership, quality, mesh, marketplace, and policies. P212-J delivers the **MEOS Enterprise Data Intelligence Graph Fabric**: ontology management, semantic entities/relationships, graph analytics, semantic search bindings, AI reasoning, knowledge governance, digital twin — as a logical surface under `data_governance`, not a sibling graph BC.

**Hard laws:** SoR remains `data_governance`. Surfaces under `/data-governance/graph*`. Enterprise intelligence requires connected knowledge, not isolated data. Semantic search via Enterprise Search. AI reasoning via Enterprise AI. Policy/authz via Policy Engine + P208. Never invent sibling `knowledge_graph` / `ontology_platform` BCs.

## Decision

1. SoR remains `data_governance`
2. Surfaces under `/api/v1/data-governance/graph*`
3. Law: `ENTERPRISE_DATA_GOVERNANCE_KNOWLEDGE_GRAPH.md`
4. Catalogs: `DATA_GOVERNANCE_GRAPH_*.v1.yaml`
5. Runtime: `dg_platform_graph.py`; aggregates; ACL; foundation
6. Quality gates enforce KG completeness across ontology, semantic fabric, intelligence, AI reasoning, mesh/metadata/marketplace/policy alignment, twin, CQRS, events, microservices, zero trust, scalability

## Consequences

- Unifies prior P212-D–H KG node/edge bindings into a governed graph fabric
- Foundation for subsequent AI readiness / intelligence phases
- Forbidden siblings remain forbidden

## References

ADR-392 · ADR-393 · ADR-397–401 · ENTERPRISE_SEARCH_ENGINE.md · AI_PLATFORM_STANDARD.md · P207–P211
