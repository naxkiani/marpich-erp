# ADR-423: Enterprise AI — Domain Architecture / DDD (P214-C)

## Status

Accepted — P214-C Enterprise AI Domain Architecture (DDD)

## Context

ADR-421–422 established SoR `ai` with foundation and mission/vision/scope. P214-C catalogs the **MEOS Enterprise AI Domain Fabric**: core Enterprise Artificial Intelligence Intelligence Platform plus supporting logical domains and BC-01…BC-08 — as logical subdomains inside `ai`, not sibling BCs.

**Principle:** AI strategy, capabilities, models, data, agents, applications, decisions, and business outcomes SHALL be represented as governed enterprise domains through DDD boundaries.

## Decision

1. SoR remains `ai` (CAP-PLT-AI-001)
2. Surfaces under `/api/v1/ai/domain*`
3. Law: `ENTERPRISE_AI_DOMAIN_ARCHITECTURE.md`
4. Catalogs: `AI_DOMAIN_*.v1.yaml`
5. Runtime: `ai_platform_domain.py`; aggregates; ACL; foundation
6. Aligns with P214-A/B, P212, P213-L, P207–P211 via ACL
7. Quality gates enforce complete DDD AI architecture, aggregates, events, microservice mapping, clear integration & governance

## Consequences

- P214-D deepens MLOps on the same SoR
- Forbidden siblings unchanged

## References

ADR-421 · ADR-422 · ADR-396 · DDD_DOMAIN_ARCHITECTURE.md · SERVICE_BOUNDARIES.md · AI_PLATFORM_STANDARD.md
