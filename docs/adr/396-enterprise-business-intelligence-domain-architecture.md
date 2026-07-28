# ADR-396: Enterprise BI — Domain Architecture / DDD (P213-C)

## Status

Accepted — P213-C Enterprise Business Intelligence Domain Architecture (DDD)

## Context

ADR-394–395 established SoR `analytics` with strategy and MVS. P213-C catalogs the **MEOS Enterprise BI Domain Fabric**: core Enterprise Business Intelligence Management plus supporting logical domains (analytics processing, metrics governance, reporting & visualization, decision intelligence) — as logical subdomains inside `analytics`, not sibling BCs.

**Principle:** Raw enterprise data SHALL be transformed into governed business intelligence assets through DDD boundaries.

**Hard laws:** SoR remains `analytics`. Surfaces under `/analytics/domain*`. Complete DDD map with BC-01…BC-05, aggregates, entities, value objects, domain services, events, CQRS, microservice boundaries, and P212-F/J/L + P207/P208/P211 governance alignment.

## Decision

1. SoR remains `analytics`
2. Surfaces under `/api/v1/analytics/domain*`
3. Law: `ENTERPRISE_BUSINESS_INTELLIGENCE_DOMAIN_ARCHITECTURE.md`
4. Catalogs: `BI_DOMAIN_*.v1.yaml`
5. Runtime: `bi_platform_domain.py`; aggregates; ACL; foundation
6. Quality gates enforce complete DDD BI architecture, loose coupling, clear ownership, events, aggregates, clear integration & platform alignments

## Consequences

- P213-D+ deepen reporting/visualization on the same SoR
- Forbidden siblings unchanged

## References

ADR-394 · ADR-395 · ADR-402 · ADR-404 · DDD_DOMAIN_ARCHITECTURE.md · SERVICE_BOUNDARIES.md · P212
