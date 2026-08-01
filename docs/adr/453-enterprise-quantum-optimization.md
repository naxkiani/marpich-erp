# ADR 453 — Enterprise Quantum Optimization, Simulation & Scientific Intelligence (P215-G)

## Status

Accepted

## Context

P215-A–F establish foundation through Quantum AI. Enterprises need a hybrid quantum-classical layer for combinatorial optimization, scientific simulation, and discovery intelligence — without sibling scientific/optimization BCs and without duplicating P213 decisions or P214 knowledge/AGI platforms.

## Decision

1. SoR remains **`quantum`** (`CAP-PLT-QC-001`).
2. Fabric: **`meos_quantum_scientific_intelligence_fabric`**.
3. API surface: **`/api/v1/quantum/optimization*`**.
4. Five logical BCs (BC-01–BC-05) remain inside SoR `quantum`.
5. Discovery binds to **P214-G/V**; decisions to **P213**; execution to **P215-D/E/F**; data to **P212**; governance to **P215-K**.
6. Principle: *MEOS Quantum Optimization Platform SHALL transform complex enterprise problems into optimized solutions through quantum algorithms, AI intelligence and hybrid computational architectures.*
7. Forbidden siblings: `quantum_optimization_platform`, `quantum_simulation_platform`, `scientific_intelligence_platform`, `quantum_discovery_platform`.
8. PQC cryptography remains **`secrets` (P209)** — not owned here; trust bindings deepen in P215-H.

## Consequences

- Catalog + aggregates + ACL + readiness live under `contexts/quantum` (`qc_platform_optimization`, `qc_optimization_*`).
- P215-H can deepen quantum security, PQC bindings, and trust architecture on this scientific fabric.
- Research reproducibility and ethics conform to P215-K.

## Alternatives considered

| Option | Rejected because |
|---|---|
| New `contexts/quantum_optimization` BC | Violates single SoR / sibling BC ban |
| Own decision outcomes in quantum | Duplicates P213 |
| Embed RAG/LLM for discovery | Violates AI Platform Standard / P214-G |
| Local HPC metrics store | Violates Observability Platform |
