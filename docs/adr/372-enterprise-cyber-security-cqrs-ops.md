# ADR-372: Cyber Security — CQRS, Events, APIs & Microservices Fabric (P210-L)

## Status

Accepted — P210-L CQRS, Event Driven Architecture, Enterprise APIs & Microservices Platform

## Context

ADR-361–371 established SoR `cyber_security` capability surfaces through Knowledge Graph. P210-L delivers the **technical nervous system catalog** for the cyber fabric: CQRS separation, immutable event sourcing (via platform Event Bus / outbox), API-first surfaces, logical microservice decomposition, service mesh / gateway integration, polyglot persistence map, DevSecOps hooks, and observability — without inventing sibling `cyber_ops` / `security_mesh` BCs, without mutable events, and without tightly coupled in-process peer domain calls.

**Hard laws:** SoR remains `cyber_security`. Surfaces under `/cyber-security/ops*`. Never tightly coupled services. Never mutable events. Never APIs without security controls. Never incomplete CQRS separation. Never non-independently-scalable microservices. Never missing observability. Never impossible AI integration. Never absent event governance. Transport via Enterprise Event Bus; edge security via API Gateway; LLM via AI Platform.

## Decision

1. SoR remains `cyber_security`
2. Surfaces under `/api/v1/cyber-security/ops*`
3. Law: `ENTERPRISE_CYBER_SECURITY_CQRS_OPS.md`
4. Catalogs: `CYBER_OPS_*.v1.yaml`
5. Runtime: `cs_platform_ops.py`; aggregates; ACL; foundation
6. Quality gates enforce loose coupling, immutable events, secured APIs, CQRS, independent scale, observability, AI integrability, event governance

## Consequences

- Documents logical deploy units inside SoR — not new BCs per microservice name
- Complements Core Event Bus, API Gateway, Observability Platform

## References

ADR-361–371 · ENTERPRISE_EVENT_BUS.md · API_GATEWAY_ARCHITECTURE.md · DEPENDENCY_GRAPH.md · PERFORMANCE_STANDARD.md
