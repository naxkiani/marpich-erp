# ADR 449 — Enterprise Quantum Domain Architecture (DDD) (P215-C)

## Status
Accepted

## Context
P215-A foundation and P215-B mission/vision establish quantum strategy. P215-C must formalize strategic and tactical DDD for the quantum SoR without creating sibling domain platforms.

## Decision
1. SoR remains **`quantum`** (`CAP-PLT-QC-001`).
2. Fabric: **`meos_quantum_domain_operating_model`**.
3. API surface: **`/api/v1/quantum/domain*`**.
4. Eight logical bounded contexts (BC-01–BC-08) remain inside SoR `quantum`.
5. Peer AI/decision/data platforms integrate via ACL only; governance remains P215-K.

## Consequences
- P215-D can deepen infrastructure/cloud on this domain model.
