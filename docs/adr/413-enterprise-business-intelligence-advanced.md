# ADR-413: Analytics — Enterprise Advanced Analytics Platform (P213-I)

## Status

Accepted — P213-I Enterprise Advanced Analytics Platform

## Context

ADR-394–396 / 408–412 established SoR `analytics` through strategy, MVS, DDD, reporting, warehouse, lakehouse, semantic/OLAP, and self-service BI. P213-I catalogs the **MEOS Enterprise Advanced Analytics Fabric**: statistical intelligence, data science workbench, experimentation, pattern discovery, root-cause analytics, insight management, and AI-assisted advanced analytics — as logical capabilities inside `analytics`, not sibling BCs.

**Principle:** Advanced Analytics SHALL transform enterprise data into scientific business intelligence that supports strategic decision making.

**Hard laws:** Surfaces under `/api/v1/analytics/advanced*`. Certified metrics via P213-G. Reuse Event Fabric, API Gateway, Enterprise AI, Observability, and P212-I/J/L + P213-E/F/G/H via ACL.

## Decision

1. SoR remains `analytics`
2. Surfaces under `/api/v1/analytics/advanced*`
3. Law: `ENTERPRISE_BUSINESS_INTELLIGENCE_ADVANCED.md`
4. Catalogs: `BI_ADVANCED_*.v1.yaml`
5. Runtime: `bi_platform_advanced.py`; aggregates; ACL; foundation
6. Quality gates enforce advanced analytics, statistical/experimentation/pattern/RCA/insight, AI, KG/twin, CQRS, events, microservices, API-first, zero trust, governance, cloud-native deployment

## Consequences

- P213-J deepens predictive analytics & forecasting on the same SoR
- Forbidden siblings unchanged

## References

ADR-394 · ADR-395 · ADR-396 · ADR-408 · ADR-409 · ADR-410 · ADR-411 · ADR-412 · P212 · CORE_PLATFORM.md
