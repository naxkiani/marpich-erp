# ADR-405: Data Governance — CQRS, Events, APIs & Microservices Platform (P212-M)

## Status

Accepted — P212-M CQRS, Events, APIs & Microservices Platform

## Context

ADR-392–393 and ADR-397–402/404 established SoR `data_governance` capability surfaces through twin simulation. P212-M delivers the **MEOS Enterprise Data Governance Integration Fabric**: CQRS command/query separation, event sourcing + event bus bindings, event contract governance, hexagonal microservice decomposition, API-first surfaces, multi-tenancy, observability/resilience bindings — without inventing sibling `data_governance_ops` / `dg_event_bus` BCs and without replacing the Enterprise Event Bus or API Gateway.

**Hard laws:** SoR remains `data_governance`. Surfaces under `/data-governance/ops*`. Enterprise governance decisions SHALL be separated from governance intelligence consumption. Commands/events via Event Fabric outbox. AuthZ via P208. Never module-local message brokers or gateway replacements.

## Decision

1. SoR remains `data_governance`
2. Surfaces under `/api/v1/data-governance/ops*`
3. Law: `ENTERPRISE_DATA_GOVERNANCE_OPS.md`
4. Catalogs: `DATA_GOVERNANCE_OPS_*.v1.yaml`
5. Runtime: `dg_platform_ops.py`; aggregates; ACL; foundation
6. Quality gates enforce ops completeness across CQRS, commands, queries, event sourcing, event bus, contracts, microservices, API-first, hexagonal, integrations, multi-tenant, observability, scalability

## Consequences

- Foundation for P212-N deployment/DevSecOps surfaces
- Forbidden siblings remain forbidden

## References

ADR-392 · ADR-397–402 · ADR-404 · ENTERPRISE_EVENT_BUS.md · API_GATEWAY_ARCHITECTURE.md · P207–P211
