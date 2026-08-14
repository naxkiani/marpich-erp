# ADR-389: Data Security — CQRS, Events, APIs & Microservices (P211-N)

## Status

Accepted — P211-N CQRS, Events, APIs & Microservices Platform

## Context

ADR-376–388 established SoR `data_security` capability surfaces through twin simulation. P211-N delivers the **distributed technical foundation**: CQRS command/query separation, immutable event catalogue + streaming topics, logical microservice decomposition, API gateway/governance bindings, service mesh (mTLS via P209), knowledge-graph and digital-twin event sync, AI event intelligence — without inventing sibling `data_security_ops` / `ds_event_bus` BCs and without replacing the Enterprise Event Bus or API Gateway.

**Hard laws:** SoR remains `data_security`. Surfaces under `/data-security/ops*`. Never tightly coupled services. Never mutable events. Never unmanaged APIs. Never untraceable security decisions. Never impossible scaling. Never incomplete audit history. Publish via Event Fabric + outbox. Gateway owns auth/rate-limit. Mesh crypto via P209. AuthZ via P208. Builds on P211-A–M and P207–P210.

## Decision

1. SoR remains `data_security`
2. Surfaces under `/api/v1/data-security/ops*`
3. Law: `ENTERPRISE_DATA_SECURITY_OPS.md`
4. Catalogs: `DATA_SECURITY_OPS_*.v1.yaml`
5. Runtime: `ds_platform_ops.py`; aggregates; ACL; foundation
6. Quality gates enforce loose coupling, immutable events, managed APIs, traceability, scalability, complete audit
7. Roadmap: P211-N = CQRS/Events/APIs/Microservices (fulfills deferred `P211-M-OPS`); Deployment/DevSecOps deferred (`/deploy*` as `P211-N-DEPLOY`)

## Consequences

- Distributed nervous system for the Data Security fabric
- Forbidden siblings: `data_security_ops`, `ds_event_platform`, `data_security_microservices`

## References

ADR-376–388 · ENTERPRISE_EVENT_BUS.md · API_GATEWAY_ARCHITECTURE.md · COMMUNICATION_ARCHITECTURE.md · SECURITY_STANDARD.md
