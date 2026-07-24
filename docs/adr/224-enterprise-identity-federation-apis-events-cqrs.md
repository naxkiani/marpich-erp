# ADR-224: EIFTP Open Host Service — APIs, Events, CQRS & Integration Surface (P200-B10)

## Status

Accepted — Official EIFTP OHS / Integration Surface baseline (V03-C03)

## Context

P200-B5–B9 delivered federation engines, trust fabric, IdPs, cross-tenant trust, and the security control plane with REST + CQRS handlers. P200-B10 packages the **Open Host Service (OHS)** contract: versioned APIs (REST/GraphQL/gRPC), event catalog, CQRS buses, outbox/inbox, saga orchestration for federation workflows, and governance — without replacing the platform Integration BC or Event Fabric.

## Decision

1. Law: `docs/architecture/ENTERPRISE_IDENTITY_FEDERATION_APIS_EVENTS_CQRS.md`
2. Catalogs: `docs/architecture/identity/eiftp/OHS_*.v1.yaml`
3. **Separate Ways** from `contexts/integration/` (external connectors) and AuthZ PDP
4. Communication uses platform Event Fabric via **outbox**; no direct service-to-service domain calls
5. CQRS: `FederationCommandBus` + `FederationQueryBus` with tenant / idempotency / correlation middleware
6. GraphQL subgraph + gRPC contracts under `backend/shared/contracts/` are first-class OHS (no longer deferred)
7. Saga orchestrator for multi-step federation workflows (trust establishment, provider activation) with compensation
8. REST OHS registry: `/api/v1/federation/ohs/*`
9. Deep Kafka ops / multi-region deploy → B11

## Consequences

- Consumers discover federation capabilities via OHS catalog, not private imports
- Event versioning required for all new `federation.*` events
- Idempotency keys mandatory on mutating commands at the bus boundary

## References

ADR-216–223 · ENTERPRISE_EVENT_BUS · INTEGRATION_PLATFORM · COMMUNICATION_ARCHITECTURE · API_GATEWAY_ARCHITECTURE
