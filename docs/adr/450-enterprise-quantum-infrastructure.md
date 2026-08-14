# ADR 450 — Enterprise Quantum Computing Infrastructure & Quantum Cloud (P215-D)

## Status
Accepted

## Context
P215-A–C establish foundation, mission, and DDD domain model. P215-D must deliver the computational infrastructure fabric (hardware abstraction, quantum cloud, runtime, resources, workloads, hybrid compute) without sibling infrastructure BCs.

## Decision
1. SoR remains **`quantum`** (`CAP-PLT-QC-001`).
2. Fabric: **`meos_quantum_infrastructure_fabric`**.
3. API surface: **`/api/v1/quantum/infrastructure*`**.
4. Seven logical infrastructure BCs (BC-01–BC-07) remain inside SoR `quantum`.
5. Zero-trust security binds to P209/P210 via ACL; governance remains P215-K; PQC stays in `secrets`.

## Consequences
- P215-E can deepen algorithm/software on this infrastructure fabric.
