# ADR-412: Analytics — Enterprise Self-Service BI Platform (P213-H)

## Status

Accepted — P213-H Enterprise Self-Service BI Platform

## Context

ADR-394–396 / 408–411 established SoR `analytics` through strategy, MVS, DDD, reporting, warehouse, lakehouse, and semantic/OLAP. P213-H catalogs the **MEOS Enterprise Analytics Experience Fabric**: workspaces, no/low-code builders, ad-hoc analytics, collaboration, NL analytics, and AI assistants — as logical capabilities inside `analytics`, not sibling BCs.

**Principle:** Every business user SHALL be capable of creating trusted analytics without compromising governance, security, or enterprise consistency.

**Hard laws:** Surfaces under `/api/v1/analytics/self-service*`. Certified metrics only via P213-G. Reuse Event Fabric, API Gateway, Enterprise AI, Enterprise Search, Observability, and P212-I/J/L + P213-D/G via ACL.

## Decision

1. SoR remains `analytics`
2. Surfaces under `/api/v1/analytics/self-service*`
3. Law: `ENTERPRISE_BUSINESS_INTELLIGENCE_SELF_SERVICE.md`
4. Catalogs: `BI_SELF_SERVICE_*.v1.yaml`
5. Runtime: `bi_platform_self_service.py`; aggregates; ACL; foundation
6. Quality gates enforce self-service, citizen/no/low-code, NL/AI, collaboration, semantic/KG/twin, CQRS, events, microservices, API-first, zero trust, governance, cloud-native deployment

## Consequences

- P213-I deepens advanced analytics on the same SoR
- Forbidden siblings unchanged

## References

ADR-394 · ADR-395 · ADR-396 · ADR-408 · ADR-409 · ADR-410 · ADR-411 · P212 · CORE_PLATFORM.md
