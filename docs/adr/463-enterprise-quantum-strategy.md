# ADR 463 — Enterprise Quantum Strategy, Compliance, Risk & Executive Intelligence (P215-R)

## Status

Accepted

## Context

P215-A–Q establish quantum foundation through research/discovery. Executives need strategy, investment, compliance operations, risk intelligence, and decision dashboards. **P215-K (ADR-403)** already owns ethics, regulation, and responsible quantum computing as the continuous trust gate. P215-R must deepen executive intelligence **without** creating a sibling governance SoR or forking Policy Engine, Audit, or P213.

## Decision

1. SoR remains **`quantum`** (`CAP-PLT-QC-001`).
2. Fabric: **`meos_quantum_executive_intelligence_fabric`**.
3. API surface: **`/api/v1/quantum/strategy*`** (executive plane).
4. P215-K remains trust gate on **`/quantum/governance*`** — R is conformist to K.
5. Six logical executive BCs (BC-01–BC-06) remain inside SoR `quantum`.
6. Policy evaluation via **Policy Engine**; decisions via **P213**; certification via **P215-O**; ops/security risk via **P215-N / P215-H**; approvals via **Workflow**; audit via **Audit Platform**.
7. Principle: *MEOS Quantum Governance Platform SHALL provide the strategic intelligence and governance foundation that ensures quantum adoption remains secure, compliant, valuable and aligned with enterprise objectives.*
8. Forbidden: replace P215-K; sibling governance/strategy BCs; module-local PDP or metrics stores.
9. Future **P215-S** must deepen security/resilience **without** replacing **P215-H** or secrets/P209 PQC SoR.

## Consequences

- Catalog + aggregates + ACL + readiness live under `contexts/quantum` (`qc_platform_strategy`, `qc_strategy_*`).
- Executive dashboards consume peer events; ethics decisions remain K-gated.
- Next: P215-S Quantum Security / Zero Trust / Resilience (align with ADR-454).

## Alternatives considered

| Option | Rejected because |
|---|---|
| New `contexts/quantum_strategy` BC | Sibling BC ban |
| Replace `/governance*` with `/strategy*` | Breaks P215-K trust gate |
| Module-local Policy Engine | Violates Policy Engine law |
| Fork P213 decision store in quantum | Violates Decision Intelligence SoR |
| Executive metrics in module DB | Violates Observability/Analytics platforms |
