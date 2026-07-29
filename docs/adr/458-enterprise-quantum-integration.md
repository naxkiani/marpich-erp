# ADR 458 — Enterprise Quantum Integration, API Gateway, Service Mesh & Hybrid Interoperability (P215-M)

## Status
Accepted

## Context
P215-A–L establish quantum foundation through digital twins. P215-M must deliver the interoperability nervous system without inventing sibling gateway/mesh/integration platforms that duplicate Core Platform Gateway, Integration Platform, or Event Fabric.

## Decision
1. SoR remains **`quantum`** (`CAP-PLT-QC-001`).
2. Fabric: **`meos_quantum_integration_intelligence_fabric`**.
3. API surface: **`/api/v1/quantum/integration*`**.
4. Six logical integration BCs (BC-01–BC-06) remain inside SoR `quantum`.
5. Quantum API registration binds **Platform API Gateway** (ACL). Connectors bind **Integration Platform**. Events bind **Event Fabric / outbox**. Mesh security binds **P215-H**. Integration governance binds **P215-K**. Twin foresight binds **P215-L**.

## Consequences
- No module-local API gateway, message broker, or connector stack inside `quantum`.
- Next: P215-N Quantum Operations, Quantum AIOps, Autonomous Quantum Management & Self-Healing Infrastructure.
