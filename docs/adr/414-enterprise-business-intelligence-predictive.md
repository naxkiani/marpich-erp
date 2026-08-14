# ADR-414: Analytics — Enterprise Predictive Analytics & Forecasting (P213-J)

## Status

Accepted — P213-J Enterprise Predictive Analytics & Forecasting Platform

## Context

ADR-394–396 / 408–413 established SoR `analytics` through strategy, MVS, DDD, reporting, warehouse, lakehouse, semantic/OLAP, self-service, and advanced analytics. P213-J catalogs the **MEOS Enterprise Predictive Intelligence Fabric**: forecast management, predictive modeling, scenario prediction, time-series intelligence, XAI, and AI forecast agents — as logical capabilities inside `analytics`, not sibling BCs.

**Principle:** Enterprise Predictive Analytics SHALL enable MEOS to anticipate future business conditions before they become operational realities.

**Hard laws:** Surfaces under `/api/v1/analytics/predictive*`. Certified metrics via P213-G. Advanced analytics via P213-I. Reuse Event Fabric, API Gateway, Enterprise AI, Observability, and P212-I/J/L + P213-E/F via ACL.

## Decision

1. SoR remains `analytics`
2. Surfaces under `/api/v1/analytics/predictive*`
3. Law: `ENTERPRISE_BUSINESS_INTELLIGENCE_PREDICTIVE.md`
4. Catalogs: `BI_PREDICTIVE_*.v1.yaml`
5. Runtime: `bi_platform_predictive.py`; aggregates; ACL; foundation
6. Quality gates enforce predictive/forecasting/modeling/scenario/time-series/XAI, KG/twin, CQRS, events, microservices, API-first, zero trust, governance, cloud-native deployment

## Consequences

- P213-K deepens prescriptive analytics & optimization on the same SoR
- Forbidden siblings unchanged

## References

ADR-394 · ADR-395 · ADR-396 · ADR-408 · ADR-409 · ADR-410 · ADR-411 · ADR-412 · ADR-413 · P212 · CORE_PLATFORM.md
