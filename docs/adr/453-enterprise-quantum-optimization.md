# ADR 453 — Enterprise Quantum Optimization, Simulation & Scientific Intelligence (P215-G)

## Status
Accepted

## Context
P215-A–F establish foundation through Quantum AI. P215-G must deliver optimization, simulation and scientific discovery intelligence without sibling scientific BCs.

## Decision
1. SoR remains **`quantum`** (`CAP-PLT-QC-001`).
2. Fabric: **`meos_quantum_scientific_intelligence_fabric`**.
3. API surface: **`/api/v1/quantum/optimization*`**.
4. Five logical BCs (BC-01–BC-05) remain inside SoR `quantum`.
5. Discovery binds to P214-G/V; decisions to P213; execution to P215-D/E/F; governance to P215-K.

## Consequences
- P215-H can deepen quantum security, PQC bindings and trust architecture.
