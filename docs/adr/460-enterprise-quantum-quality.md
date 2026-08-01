# ADR 460 — Enterprise Quantum Testing, Validation, Benchmarking, QA & Certification (P215-O)

## Status

Accepted

## Context

P215-A–N establish quantum foundation through autonomous operations. MEOS requires a quality intelligence layer for quantum software testing, algorithm validation, hardware benchmarking, QA automation, and certification — without sibling testing/certification BCs or forking P214-O AI Testing & Evaluation, Workflow, or Audit platforms.

## Decision

1. SoR remains **`quantum`** (`CAP-PLT-QC-001`).
2. Fabric: **`meos_quantum_quality_intelligence_fabric`**.
3. API surface: **`/api/v1/quantum/testing*`**.
4. Six logical quality BCs (BC-01–BC-06) remain inside SoR `quantum`.
5. Software under test binds **P215-E**; QAI eval **P215-F**; scientific oracles **P215-G**; hardware **P215-D**; security cert **P215-H**; certification governance **P215-K** + **Workflow**; ops quality gates **P215-N**; twin foresight **P215-L**; AI QA patterns **P214-O** via ACL.
6. Principle: *MEOS Quantum Quality Platform SHALL provide the trust, measurement and validation foundation required for enterprise-scale quantum computing adoption.*
7. Forbidden: module-local certification authority replacing Workflow/Audit; ungated production promotion; sibling testing/certification BCs.
8. Forbidden siblings: `quantum_testing_platform`, `quantum_validation_platform`, `quantum_benchmarking_platform`, `quantum_certification_platform`, `quantum_qa_platform`.

## Consequences

- Quantum stores test/benchmark/certificate refs and quality projections; evidence ledger remains Audit Platform.
- Catalog + aggregates + ACL + readiness live under `contexts/quantum` (`qc_platform_quality`, `qc_quality_*`).
- Completes P215 A–O quality plane; next: P215-P Quantum Marketplace / Economy.

## Alternatives considered

| Option | Rejected because |
|---|---|
| New `contexts/quantum_testing` BC | Sibling BC ban |
| Fork P214-O AI QA inside quantum | Violates AI Platform / P214-O SoR |
| Local certificate approval FSM | Violates Workflow Engine |
| Module-local audit of cert evidence | Violates Audit Platform |
| Promote without P215-K gate | Violates governance trust gate |
