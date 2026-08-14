# ADR-411: Analytics — Enterprise OLAP, Semantic Layer & Business Metrics Platform (P213-G)

## Status

Accepted — P213-G Enterprise OLAP, Semantic Layer & Business Metrics Platform

## Context

ADR-394–396 / 408–410 established SoR `analytics` through strategy, MVS, DDD, reporting, warehouse, and lakehouse. P213-G catalogs the **MEOS Enterprise Semantic Intelligence Fabric**: governed metrics/KPIs, semantic layer, OLAP cubes, dimensions, calculation engine, glossary/taxonomy, and semantic query — as logical capabilities inside `analytics`, not sibling BCs.

**Principle:** Every enterprise decision SHALL be based upon a governed semantic definition instead of isolated calculations.

**Hard laws:** Surfaces under `/api/v1/analytics/olap*`. Single source of truth for metrics and calculations. Reuse Event Fabric, API Gateway, Enterprise AI, Enterprise Search, Observability, and P212-J/L + P213-D/E/F via ACL.

## Decision

1. SoR remains `analytics`
2. Surfaces under `/api/v1/analytics/olap*`
3. Law: `ENTERPRISE_BUSINESS_INTELLIGENCE_OLAP.md`
4. Catalogs: `BI_OLAP_*.v1.yaml`
5. Runtime: `bi_platform_olap.py`; aggregates; ACL; foundation
6. Quality gates enforce semantic layer, metrics, KPI governance, OLAP, glossary, query, KG/twin/AI, CQRS, events, microservices, API-first, zero trust, cloud-native deployment

## Consequences

- P213-H deepens self-service BI on the same SoR
- Forbidden siblings unchanged

## References

ADR-394 · ADR-395 · ADR-396 · ADR-408 · ADR-409 · ADR-410 · P212 · CORE_PLATFORM.md
