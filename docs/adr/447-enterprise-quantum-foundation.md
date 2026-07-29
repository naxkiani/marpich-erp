# ADR 447 — Enterprise Quantum Computing Foundation (P215-A)

## Status
Accepted

## Context
P214 completed the MEOS AI evolution series. P215 introduces the post-classical computational layer. P215-K already delivered quantum governance as the trust gate; P215-A establishes the quantum computing foundation inside SoR `quantum`.

## Decision
1. SoR remains **`quantum`** (`CAP-PLT-QC-001`).
2. Fabric: **`meos_quantum_intelligence_fabric`**.
3. API surface: **`/api/v1/quantum/foundation*`**.
4. Seven logical bounded contexts remain inside SoR `quantum`.
5. Quantum AI integrates with P214-V via ACL; control/orchestration with P214-T/Z; governance with P215-K.
6. Post-quantum cryptography remains owned by `secrets` (P209).

## Consequences
- P215-B can deepen mission/vision on this foundation.
- No module may create sibling quantum computing platforms outside SoR `quantum`.
