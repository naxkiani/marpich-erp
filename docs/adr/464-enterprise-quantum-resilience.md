# ADR 464 — Enterprise Quantum Security, Cyber Defense, Identity, Zero Trust & Resilience (P215-S)

## Status

Accepted

## Context

P215-A–R establish the quantum ecosystem through research and executive strategy. The ecosystem needs a continuous cyber defense, identity assurance, Zero Trust enforcement, SOC, and resilience layer. **P215-H (ADR-454)** already owns quantum security/trust architecture and PQC *bindings* on `/quantum/security*`. PQC key material remains **secrets (P209)**. P215-S must deepen resilience and cyber ops **without** creating a sibling security SoR or forking Identity, Policy Engine, or secrets.

## Decision

1. SoR remains **`quantum`** (`CAP-PLT-QC-001`).
2. Fabric: **`meos_quantum_cyber_trust_fabric`**.
3. API surface: **`/api/v1/quantum/resilience*`** (cyber defense / resilience plane).
4. P215-H remains security/trust gate on **`/quantum/security*`** — S is conformist to H.
5. Six logical security BCs (BC-01–BC-06) remain inside SoR `quantum`.
6. PQC material via **secrets (P209)** only; identity via **Identity / P200-B**; Zero Trust PDP via **Policy Engine**; SOC via **P214-J** + Observability; ops via **P215-N**; ethics via **P215-K**; strategy risk via **P215-R**.
7. Principle: *MEOS Quantum Security Platform SHALL provide a continuous trust, protection and resilience framework for quantum-enabled enterprise operations.*
8. Forbidden: replace P215-H; sibling security BCs; local PQC store; module-local PDP; embed Identity SoR.
9. Future **P215-T** must establish Quantum OS / control plane without replacing platform Core or prior P215 gates.

## Consequences

- Catalog + aggregates + ACL + readiness live under `contexts/quantum` (`qc_platform_resilience`, `qc_resilience_*`).
- Defense/SOC consume peer events; trust posture decisions remain H-gated; keys remain P209.
- Next: P215-T Quantum Operating System / Control Plane / MEOS Quantum Intelligence Core.

## Alternatives considered

| Option | Rejected because |
|---|---|
| New `contexts/quantum_security_ops` BC | Sibling BC ban |
| Replace `/security*` with `/resilience*` | Breaks P215-H security gate |
| Local PQC / key store in quantum | Violates secrets/P209 |
| Module-local Zero Trust PDP | Violates Policy Engine law |
| Fork Identity users into quantum schema | Violates Identity / P200-B SoR |
| Module-local SOC metrics store | Violates Observability / P214-J |
