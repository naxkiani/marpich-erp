# ADR 459 — Enterprise Quantum Operations, AIOps, Autonomous Management & Self-Healing (P215-N)

## Status
Accepted

## Context
P215-A–M establish quantum foundation through interoperability. P215-N must deliver autonomous operations without inventing sibling observability/AIOps platforms that duplicate Core Observability or P214-J Enterprise AIOps.

## Decision
1. SoR remains **`quantum`** (`CAP-PLT-QC-001`).
2. Fabric: **`meos_quantum_autonomous_operations_fabric`**.
3. API surface: **`/api/v1/quantum/operations*`**.
4. Seven logical operations BCs (BC-01–BC-07) remain inside SoR `quantum`.
5. Telemetry binds **Observability Platform (OTel)**. AIOps binds **P214-J** (+ P215-F). Automation policies bind **Policy Engine / P215-K**. Recovery workflows bind **Workflow**. Twin foresight binds **P215-L**. Infrastructure signals bind **P215-D**.

## Consequences
- No module-local metrics stores, AIOps engines, or approval state machines inside `quantum`.
- Next: P215-O Quantum Testing, Validation, Benchmarking, QA & Certification.
