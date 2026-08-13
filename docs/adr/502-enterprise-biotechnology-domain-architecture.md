# ADR 502 — Enterprise Biotechnology Domain Architecture (DDD) (P217-C)

## Status

Accepted

## Context

P217-B established strategic architecture. P217-C defines strategic DDD classification, bounded contexts, aggregates, entities, value objects, domain services, repositories, events, CQRS and microservice alignment — before infrastructure (P217-D).

## Decision

1. SoR remains `biotechnology` / `CAP-PLT-BIO-001`.
2. Fabric: `meos_biotechnology_domain_architecture_framework`.
3. API: `/api/v1/biotechnology/domain*`.
4. Core domain: Enterprise Bio Intelligence Domain; six supporting domains; generic domains via Core Platform.
5. Seven bounded contexts (BC-01..BC-07) with one aggregate root each.
6. Never cross-context aggregate mutation; never peer domain imports; ACL + events only.
7. Never replace Core, AI, Quantum, Robotics, hospital EMR, laboratory LIMS, pharmacy, prior P217 fabrics.
8. Foundation for P217-D.

## Consequences

Positive: clear DDD boundaries for bio intelligence series.  
Negative: catalog must stay aligned as P217-D+ runtime deepens.

## Alternatives rejected

- Sibling `bio_ddd` BC outside SoR biotechnology.
- Merging clinical EMR/LIMS ownership into bio aggregates.
- Cross-context ORM joins.

## Related

Law: `ENTERPRISE_BIOTECHNOLOGY_DOMAIN.md` · Prior: ADR 499–501 · Next: P217-D
