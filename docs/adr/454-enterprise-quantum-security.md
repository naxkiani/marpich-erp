# ADR 454 — Enterprise Quantum Security, PQC Bindings & Quantum Trust (P215-H)

## Status

Accepted

## Context

P215-A–G establish quantum compute through scientific intelligence. MEOS requires a quantum-safe security and trust control plane for quantum workloads, identities, and channels — without owning Post-Quantum Cryptography key material or creating sibling security BCs that would duplicate P209 secrets, P207/P208 identity/authz, or P210 cyber platforms.

## Decision

1. SoR remains **`quantum`** (`CAP-PLT-QC-001`).
2. Fabric: **`meos_quantum_trust_fabric`**.
3. API surface: **`/api/v1/quantum/security*`**.
4. Six logical security BCs (BC-01–BC-06) remain inside SoR `quantum`.
5. **PQC SoR remains `secrets` (P209)** — quantum binds via ACL only; **no local key/PQC store**.
6. Identity/authz via **P207/P208**; cyber threats via **P210**; governance via **P215-K**.
7. Principle: *MEOS Quantum Security Platform SHALL provide a future-ready security architecture protecting enterprise quantum systems, digital identities and cryptographic trust relationships.*
8. Implements Zero Trust Quantum Architecture with continuous verification.
9. Forbidden siblings: `quantum_security_platform`, `quantum_pqc_platform`, `quantum_trust_platform`, `post_quantum_platform`.

## Consequences

- Catalog + aggregates + ACL + readiness live under `contexts/quantum` (`qc_platform_security`, `qc_security_*`).
- Key rotation/migration commands emit events consumed by P209; quantum persists refs only.
- P215-I can deepen quantum data intelligence and data-governance bindings on this trust fabric.

## Alternatives considered

| Option | Rejected because |
|---|---|
| Local PQC/key tables in `quantum` | Violates P209 SoR / "Never Local PQC Store" |
| New `contexts/quantum_security` BC | Sibling BC ban |
| Own identity/authz engines | Duplicates P207/P208 |
| Local SIEM/threat store | Duplicates P210 / Observability |
