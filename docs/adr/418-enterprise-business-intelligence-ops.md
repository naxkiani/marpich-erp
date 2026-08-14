# ADR-418: Analytics — CQRS, Events, APIs & Microservices Platform (P213-N)

## Status

Accepted — P213-N CQRS, Events, APIs & Microservices Platform

## Context

P213 SoR remains `analytics` (CAP-PLT-BI-001). P213-N delivers **Enterprise BI CQRS, Events, APIs & Microservices Platform** without inventing sibling BI BCs.

**Hard laws:** Surfaces under `/api/v1/analytics/ops*`. Every business event SHALL become a durable enterprise event; every capability SHALL expose contract-first APIs; every analytics service SHALL remain independently deployable. Reuse Enterprise Event Fabric, API Gateway, Observability, Enterprise AI, and P207–P212 via ACL.

## Decision

1. SoR remains `analytics`
2. Surfaces under `/api/v1/analytics/ops*`
3. Fabric: `meos_enterprise_analytics_integration_fabric`
4. Law: `ENTERPRISE_BUSINESS_INTELLIGENCE_OPS.md`
5. Catalogs: `BI_OPS_*.v1.yaml`
6. Runtime: `bi_platform_ops.py`; aggregates; ACL; foundation
7. Event transport and public edge remain platform-owned (no module-local bus/gateway)

## Consequences

- Extends P213 series with full integration fabric for A–M surfaces
- Forbidden siblings remain forbidden
- P213-O deepens deployment / DevSecOps / observability DoD on the same SoR

## References

ADR-394–417 · prior P213 phases · P207–P212 · ENTERPRISE_EVENT_BUS.md · API_GATEWAY_ARCHITECTURE.md · CORE_PLATFORM.md
