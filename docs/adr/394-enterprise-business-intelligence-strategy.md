# ADR-394: Enterprise BI — Strategy Foundation (P213-A)

## Status

Accepted — P213-A Enterprise Business Intelligence, Analytics & Decision Intelligence Platform Foundation

## Context

Volume 06 continues after P211 (`data_security`) and P212 (`data_governance`). P213 elevates SoR `analytics` into the **MEOS Enterprise Intelligence Fabric** — BI, analytics, metrics, insights, and decision intelligence — without inventing sibling BCs (`business_intelligence`, `reporting_platform`, `decision_intelligence`, …).

**Principle:** Enterprise intelligence transforms trusted data into strategic organizational decisions.

## Decision

1. SoR remains `analytics` (CAP-PLT-BI-001)
2. Surfaces under `/api/v1/analytics/strategy*`
3. Law: `ENTERPRISE_BUSINESS_INTELLIGENCE_STRATEGY.md`
4. Catalogs: `BI_STRATEGY_*.v1.yaml`
5. Runtime: `bi_platform_strategy.py`; aggregates; ACL; foundation
6. Consumes P212 data products / KG / twin via ACL; security/privacy via P211; AI via Enterprise AI only
7. Quality gates enforce BI foundation, analytics, decision intelligence, DDD, CQRS, microservices, API-first, AI-native, graph/twin, governance alignment

## Consequences

- P213-B+ deepen mission, domain DDD, reporting on the same SoR
- Forbidden siblings unchanged

## References

ADR-392 · ADR-393 · ADR-402 · ADR-404 · CORE_PLATFORM.md · AI_PLATFORM_STANDARD.md · analytics context
