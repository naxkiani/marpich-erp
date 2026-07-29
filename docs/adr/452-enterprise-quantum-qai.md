# ADR 452 — Enterprise Quantum AI & Quantum Machine Learning (P215-F)

## Status
Accepted

## Context
P215-A–E establish foundation through algorithm/software intelligence. P215-F must deliver the Quantum AI / QML layer without sibling AI/ML BCs, extending MEOS AI via ACL to P214-* peers.

## Decision
1. SoR remains **`quantum`** (`CAP-PLT-QC-001`).
2. Fabric: **`meos_quantum_ai_intelligence_fabric`**.
3. API surface: **`/api/v1/quantum/qai*`**.
4. Eight logical QAI BCs (BC-01–BC-08) remain inside SoR `quantum`.
5. Model lifecycle binds to P214-L; agents to P214-F; features to P212; runtime to P215-D; algorithms to P215-E; governance to P215-K.

## Consequences
- P215-G can deepen optimization/simulation/scientific intelligence on this QAI fabric.
