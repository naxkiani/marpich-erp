# ADR-409: Analytics — Enterprise Data Warehouse & Analytical Data Platform (P213-E)

## Status

Accepted — P213-E Enterprise Data Warehouse & Analytical Data Platform

## Context

ADR-394–396 / 408 established SoR `analytics` through strategy, MVS, DDD, and reporting experience. P213-E catalogs the **MEOS Enterprise Analytical Intelligence Data Fabric**: warehouse core, dimensional modeling, ingestion/CDC, historical intelligence, data marts, and semantic layer — as logical capabilities inside `analytics`, not sibling BCs.

**Principle:** Enterprise Data Warehouse SHALL become the historical intelligence memory of MEOS.

**Hard laws:** Surfaces under `/api/v1/analytics/warehouse*`. Transforms governed data products into trusted analytical intelligence assets. Reuse Event Fabric, API Gateway, Enterprise AI, Observability, and P212-E/F/J/K/L via ACL.

## Decision

1. SoR remains `analytics`
2. Surfaces under `/api/v1/analytics/warehouse*`
3. Law: `ENTERPRISE_BUSINESS_INTELLIGENCE_WAREHOUSE.md`
4. Catalogs: `BI_WAREHOUSE_*.v1.yaml`
5. Runtime: `bi_platform_warehouse.py`; aggregates; ACL; foundation
6. Quality gates enforce warehouse, dimensional modeling, integration, semantic layer, governance, AI readiness, KG, twin, CQRS, events, microservices, API-first, cloud-native deployment

## Consequences

- P213-F deepens lakehouse serving on the same SoR
- Forbidden siblings unchanged

## References

ADR-394 · ADR-395 · ADR-396 · ADR-408 · P212-E…O · CORE_PLATFORM.md
