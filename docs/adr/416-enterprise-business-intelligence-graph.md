# ADR-416: Analytics — Enterprise Decision Intelligence Knowledge Graph (P213-L)

## Status

Accepted — P213-L Enterprise Decision Intelligence Knowledge Graph Platform

## Context

ADR-394–396 / 408–415 established SoR `analytics` through strategy, MVS, DDD, reporting, warehouse, lakehouse, semantic/OLAP, self-service, advanced, predictive, and prescriptive analytics. P213-L catalogs the **MEOS Enterprise Decision Knowledge Fabric**: decision graph, ontology, lineage, memory, graph analytics, and AI reasoning — as logical capabilities inside `analytics`, federating with P212-J (not inventing a sibling `decision_intelligence` BC).

**Principle:** Every enterprise decision SHALL become a governed, connected, explainable, versioned knowledge asset.

**Hard laws:** Surfaces under `/api/v1/analytics/graph*`. Federate with P212-J via ACL. Twin integration via P212-L. Reuse Event Fabric, API Gateway, Enterprise AI, Observability.

## Decision

1. SoR remains `analytics`
2. Surfaces under `/api/v1/analytics/graph*`
3. Law: `ENTERPRISE_BUSINESS_INTELLIGENCE_GRAPH.md`
4. Catalogs: `BI_GRAPH_*.v1.yaml`
5. Runtime: `bi_platform_graph.py`; aggregates; ACL; foundation
6. Quality gates enforce decision KG/ontology/memory/analytics/AI/lineage/federation/twin, CQRS, events, microservices, API-first, zero trust, cloud-native deployment

## Consequences

- P213-M deepens AI Native Analytics & Autonomous Decision Intelligence on the same SoR
- Forbidden siblings unchanged

## References

ADR-394 · ADR-395 · ADR-396 · ADR-402 · ADR-408–415 · P212-J · P212-L · CORE_PLATFORM.md
