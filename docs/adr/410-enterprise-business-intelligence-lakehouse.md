# ADR-410: Analytics — Enterprise Lakehouse Architecture Platform (P213-F)

## Status

Accepted — P213-F Enterprise Lakehouse Architecture Platform

## Context

ADR-394–396 / 408–409 established SoR `analytics` through strategy, MVS, DDD, reporting, and warehouse. P213-F catalogs the **MEOS Enterprise Lakehouse Intelligence Fabric**: medallion layers (bronze/silver/gold/AI), storage fabric, processing engine, data-product infrastructure, streaming intelligence, and AI data foundation — as logical capabilities inside `analytics`, not sibling BCs.

**Principle:** Enterprise Lakehouse becomes the intelligent data foundation where analytics, AI, and decision intelligence converge.

**Hard laws:** Surfaces under `/api/v1/analytics/lakehouse*`. Unifies warehouse + lake + AI data + analytics under unified governance. Reuse Event Fabric, API Gateway, Enterprise AI, Observability, and P212-E/F/G/J/K/L + P213-E via ACL.

## Decision

1. SoR remains `analytics`
2. Surfaces under `/api/v1/analytics/lakehouse*`
3. Law: `ENTERPRISE_BUSINESS_INTELLIGENCE_LAKEHOUSE.md`
4. Catalogs: `BI_LAKEHOUSE_*.v1.yaml`
5. Runtime: `bi_platform_lakehouse.py`; aggregates; ACL; foundation
6. Quality gates enforce lakehouse, unified platform, warehouse/lake/AI foundations, mesh/governance/KG/twin, CQRS, events, microservices, API-first, cloud-native deployment

## Consequences

- P213-G deepens OLAP / semantic / business metrics on the same SoR
- Forbidden siblings unchanged

## References

ADR-394 · ADR-395 · ADR-396 · ADR-408 · ADR-409 · P212-E…O · CORE_PLATFORM.md
