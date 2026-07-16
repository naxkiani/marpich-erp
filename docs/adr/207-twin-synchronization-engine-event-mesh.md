# ADR-207: Twin Synchronization Engine & Event Mesh Profile (Prompt 199-B)

## Status

Accepted

## Context

ADR-203 / 203a define the Digital Twin Platform and kind catalog. Continuous multi-industry synchronization requires a formal **Twin Synchronization Engine** (modes, workers, conflict, delta, recovery) and an **Event Mesh** for durable fan-out. The platform already has Event Fabric (ADR-010), Enterprise Event Bus (ADR-175), Message Orchestration (ADR-178), and Integration connectors (ADR-036). Rebuilding these inside the twin BC would violate the Platform Charter.

**Prompt ID:** V03-C02-P199-B · **ADR number:** 207

## Decision

1. Place the Twin Synchronization Engine as a **logical pack inside** `identity_digital_twin` (coordinator, SyncRun, workers, conflict/delta/state/version/snapshot/recovery).  
2. Define **Event Mesh** as a **binding/governance profile** over Fabric + Bus + Orchestration — not a new bounded context.  
3. Extend transport registry for Pulsar / Azure Event Grid where missing; keep Kafka/NATS/Rabbit/EventBridge/Pub/Sub as configured bindings.  
4. External connectors remain **Integration Platform only**; twin provides ACL mappers from normalized events to sync commands.  
5. Sync modes, topics, routing, retries, and conflict strategies are **catalog + Policy Engine** driven.  
6. Expand twin event catalog with synchronization lifecycle, conflict, facet-change, merge/split, and anomaly events.  
7. REST remains OpenAPI 3.1 under `/api/v1/identity-twins`; GraphQL/gRPC via ADR-198; AsyncAPI generated from event YAML (no parallel contract truth).  
8. Errors use **RFC 9457** Problem Details.

## Consequences

- Twin workers must not open vendor HTTP or peer DB connections.  
- Cross-tenant/cross-region sync requires explicit policy grants.  
- Observability metrics are mandatory for every SyncRun.  
- Incremental delivery phases B0–B5 in architecture law doc.

## References

- [ENTERPRISE_TWIN_SYNCHRONIZATION_EVENT_MESH.md](../architecture/ENTERPRISE_TWIN_SYNCHRONIZATION_EVENT_MESH.md)  
- [ENTERPRISE_IDENTITY_DIGITAL_TWIN_PLATFORM.md](../architecture/ENTERPRISE_IDENTITY_DIGITAL_TWIN_PLATFORM.md)  
- ADR-010, ADR-036, ADR-175, ADR-178, ADR-198, ADR-203, ADR-203a
