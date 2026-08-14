# ADR 458 — Enterprise Quantum Integration, API Gateway, Service Mesh & Hybrid Interoperability (P215-M)

## Status

Accepted

## Context

P215-A–L establish quantum foundation through digital twins. MEOS requires an interoperability nervous system for quantum APIs, service mesh policy, hybrid quantum-classical workflows, event routing, and capability federation — without inventing sibling gateway/mesh/integration platforms that duplicate Core Platform API Gateway, Integration Platform, or Event Fabric.

## Decision

1. SoR remains **`quantum`** (`CAP-PLT-QC-001`).
2. Fabric: **`meos_quantum_integration_intelligence_fabric`**.
3. API surface: **`/api/v1/quantum/integration*`**.
4. Six logical integration BCs (BC-01–BC-06) remain inside SoR `quantum`.
5. Quantum API registration binds **Platform API Gateway** (ACL). Connectors bind **Integration Platform**. Events bind **Event Fabric / outbox**. Mesh security binds **P215-H**. Integration governance binds **P215-K**. Twin foresight binds **P215-L**. Software/AI surfaces bind **P215-E / P215-F**.
6. Principle: *MEOS Quantum Integration Platform SHALL provide the intelligent interoperability layer connecting quantum, classical and autonomous enterprise capabilities.*
7. Forbidden: module-local API gateway, message broker, or connector stack inside `quantum`.
8. Forbidden siblings: `quantum_api_gateway_platform`, `quantum_service_mesh_platform`, `quantum_hybrid_integration_platform`, `quantum_capability_federation_platform`.

## Consequences

- Quantum registers routes/capabilities and mesh policies; does not own public ingress or brokers.
- Catalog + aggregates + ACL + readiness live under `contexts/quantum` (`qc_platform_integration`, `qc_integration_*`).
- Next: P215-N Quantum Operations, Quantum AIOps, Autonomous Quantum Management & Self-Healing Infrastructure.

## Alternatives considered

| Option | Rejected because |
|---|---|
| Fork Kong/Envoy inside quantum | Violates Platform API Gateway law |
| Module-local Kafka/RabbitMQ | Violates Event Fabric / outbox |
| Embed vendor connectors in quantum | Violates Integration Platform |
| New sibling gateway BC | Sibling BC ban |
| Bypass P215-K on capability publish | Violates governance trust gate |
