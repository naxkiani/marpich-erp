# ADR 454 — Enterprise Quantum Security, PQC Bindings & Quantum Trust (P215-H)

## Status
Accepted

## Context
P215-A–G establish quantum compute through scientific intelligence. P215-H must deliver quantum security and trust without owning PQC crypto stores or creating sibling security BCs.

## Decision
1. SoR remains **`quantum`** (`CAP-PLT-QC-001`).
2. Fabric: **`meos_quantum_trust_fabric`**.
3. API surface: **`/api/v1/quantum/security*`**.
4. Six logical security BCs (BC-01–BC-06) remain inside SoR `quantum`.
5. **PQC SoR remains `secrets` (P209)** — quantum binds via ACL only; no local key/PQC store.
6. Identity/authz via P207/P208; cyber threats via P210; governance via P215-K.

## Consequences
- P215-I can deepen quantum data intelligence and knowledge/data governance bindings.
