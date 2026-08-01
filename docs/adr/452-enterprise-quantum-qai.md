# ADR 452 — Enterprise Quantum AI & Quantum Machine Learning (P215-F)

## Status

Accepted

## Context

P215-A–E establish foundation through algorithm/software intelligence. MEOS requires a Quantum AI / Quantum Machine Learning intelligence layer that combines quantum compute with AI/ML without creating sibling AI/ML bounded contexts, and without embedding LLM SDKs or classical model registries inside `quantum`.

## Decision

1. SoR remains **`quantum`** (`CAP-PLT-QC-001`).
2. Fabric: **`meos_quantum_ai_intelligence_fabric`**.
3. API surface: **`/api/v1/quantum/qai*`**.
4. Eight logical QAI BCs (BC-01–BC-08) remain inside SoR `quantum`.
5. Model lifecycle binds to **P214-L**; agents to **P214-F**; AGI to **P214-V**; master AI to **P214-Z**; features/data to **P212**; decision intelligence to **P213**; runtime to **P215-D**; algorithms to **P215-E**; operational governance to **P215-K**.
6. Principle: *MEOS Quantum AI Platform SHALL combine quantum computational capabilities with artificial intelligence systems to create advanced enterprise intelligence beyond classical machine learning architectures.*
7. Forbidden siblings: `quantum_ai_platform`, `quantum_ml_platform`, `quantum_neural_platform`, `qml_platform`.

## Consequences

- Catalog + aggregates + ACL + readiness live under `contexts/quantum` (`qc_platform_qai`, `qc_qai_*`).
- P215-G deepens optimization/simulation/scientific intelligence on this QAI fabric without forking SoR.
- Classical AI remains platform-owned; Quantum AI is hybrid acceleration + cognitive extension via ACL only.

## Alternatives considered

| Option | Rejected because |
|---|---|
| New `contexts/quantum_ai` BC | Violates single SoR / sibling BC ban |
| Embed OpenAI/Anthropic in quantum | Violates AI Platform Standard |
| Local model registry tables | Duplicates P214-L |
| Skip neural/agent/feature surfaces | Fails P215-F DoD |
