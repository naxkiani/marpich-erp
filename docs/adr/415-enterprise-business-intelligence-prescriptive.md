# ADR-415: Analytics — Enterprise Prescriptive Analytics & Optimization (P213-K)

## Status

Accepted — P213-K Enterprise Prescriptive Analytics & Optimization Intelligence Platform

## Context

ADR-394–396 / 408–414 established SoR `analytics` through strategy, MVS, DDD, reporting, warehouse, lakehouse, semantic/OLAP, self-service, advanced, and predictive analytics. P213-K catalogs the **MEOS Enterprise Decision Optimization Fabric**: optimization engines, recommendation engines, constraints, objectives, AI decision agents, and explainable optimization — as logical capabilities inside `analytics`, not sibling BCs.

**Principle:** Enterprise Prescriptive Analytics SHALL recommend the optimal enterprise action based upon business objectives, enterprise policies, constraints, predictions, and strategic priorities.

**Hard laws:** Surfaces under `/api/v1/analytics/prescriptive*`. Predictive inputs via P213-J. Certified metrics via P213-G. Reuse Event Fabric, API Gateway, Enterprise AI, Observability, and P212-I/J/L via ACL.

## Decision

1. SoR remains `analytics`
2. Surfaces under `/api/v1/analytics/prescriptive*`
3. Law: `ENTERPRISE_BUSINESS_INTELLIGENCE_PRESCRIPTIVE.md`
4. Catalogs: `BI_PRESCRIPTIVE_*.v1.yaml`
5. Runtime: `bi_platform_prescriptive.py`; aggregates; ACL; foundation
6. Quality gates enforce prescriptive/optimization/recommendation/constraint/objective/AI/XAI, KG/twin, CQRS, events, microservices, API-first, zero trust, governance, cloud-native deployment

## Consequences

- P213-L deepens Decision Intelligence Knowledge Graph on the same SoR
- Forbidden siblings unchanged

## References

ADR-394 · ADR-395 · ADR-396 · ADR-408 · ADR-409 · ADR-410 · ADR-411 · ADR-412 · ADR-413 · ADR-414 · P212 · CORE_PLATFORM.md
