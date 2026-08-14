# ADR 503 — Enterprise Biotechnology Bio Intelligence Infrastructure (P217-D)

## Status

Accepted

## Context

P217-C established DDD domain model. P217-D defines scientific-grade infrastructure — computing, cloud, data, AI compute, laboratory integration, security, observability, resilience and deployment — before Bio-AI platform (P217-E).

## Decision

1. SoR remains `biotechnology` / `CAP-PLT-BIO-001`.
2. Fabric: `meos_bio_intelligence_infrastructure_fabric`.
3. API: `/api/v1/biotechnology/infrastructure*`.
4. Five infrastructure layers; scientific computing, bio cloud, data, AI compute, lab integration catalogs.
5. Observability via platform only — no module-local metrics stores.
6. Laboratory devices via Integration Platform — never direct vendor SDK in domain.
7. Never replace Core, AI, Quantum, Robotics, hospital EMR, LIMS, pharmacy, prior P217 fabrics.
8. Foundation for P217-E.

## Consequences

Positive: cloud-native scientific foundation for bio AI/synthetic phases.  
Negative: infrastructure catalog must stay aligned with P217-E+ compute surfaces.

## Alternatives rejected

- Sibling `bio_infra` BC outside SoR biotechnology.
- Embedding clinical data lakes as EMR SoR.
- Module-local Prometheus/OTel stores.

## Related

Law: `ENTERPRISE_BIOTECHNOLOGY_INFRASTRUCTURE.md` · Prior: ADR 499–502 · Next: P217-E
