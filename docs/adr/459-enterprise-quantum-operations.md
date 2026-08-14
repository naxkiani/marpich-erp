# ADR 459 — Enterprise Quantum Operations, AIOps, Autonomous Management & Self-Healing (P215-N)

## Status

Accepted

## Context

P215-A–M establish quantum foundation through interoperability. MEOS requires an autonomous operations intelligence layer for monitoring, AIOps-assisted prediction, incident automation, self-healing, and reliability engineering — without inventing sibling observability/AIOps platforms that duplicate Core Observability or P214-J Enterprise AIOps.

## Decision

1. SoR remains **`quantum`** (`CAP-PLT-QC-001`).
2. Fabric: **`meos_quantum_autonomous_operations_fabric`**.
3. API surface: **`/api/v1/quantum/operations*`**.
4. Seven logical operations BCs (BC-01–BC-07) remain inside SoR `quantum`.
5. Telemetry binds **Observability Platform (OTel)**. AIOps binds **P214-J** (+ **P215-F**). Automation policies bind **Policy Engine / P215-K**. Recovery workflows bind **Workflow**. Twin foresight binds **P215-L**. Infrastructure signals bind **P215-D**. Security incidents bind **P215-H**.
6. Principle: *MEOS Quantum Operations Platform SHALL provide an autonomous operational intelligence layer capable of monitoring, predicting, optimizing and healing quantum enterprise infrastructure.*
7. Forbidden: module-local metrics stores, AIOps engines, or approval state machines inside `quantum`.
8. Forbidden siblings: `quantum_operations_platform`, `quantum_aiops_platform`, `quantum_self_healing_platform`, `quantum_observability_platform`.

## Consequences

- Quantum emits OTel and stores operational projections/`ref`s; does not own metrics backends or AIOps SoR.
- High-impact self-healing requires Policy Engine / human oversight.
- Catalog + aggregates + ACL + readiness live under `contexts/quantum` (`qc_platform_operations`, `qc_operations_*`).
- Next: P215-O Quantum Testing, Validation, Benchmarking, QA & Certification.

## Alternatives considered

| Option | Rejected because |
|---|---|
| Module-local Prometheus/ELK | Violates Observability Platform |
| Fork Enterprise AIOps in quantum | Violates P214-J |
| Local approval FSM for healing | Violates Workflow Engine |
| Ungated autonomous recovery | Violates P215-K / Policy Engine |
| New sibling ops/observability BC | Sibling BC ban |
