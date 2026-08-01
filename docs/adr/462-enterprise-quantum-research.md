# ADR 462 — Enterprise Quantum Research, Innovation Lab, Scientific Collaboration & Future Intelligence Evolution (P215-Q)

## Status

Accepted

## Context

P215-A–P establish quantum foundation through marketplace economy. MEOS requires a research and discovery intelligence layer for innovation labs, experiments, collaboration, AI-assisted discovery, and future technology radar — without forking P215-G scientific engines, P214-G RAG, Document Exchange, or creating sibling research BCs.

## Decision

1. SoR remains **`quantum`** (`CAP-PLT-QC-001`).
2. Fabric: **`meos_quantum_discovery_intelligence_fabric`**.
3. API surface: **`/api/v1/quantum/research*`**.
4. Six logical research BCs (BC-01–BC-06) remain inside SoR `quantum`.
5. Scientific kernels bind **P215-G**; knowledge/RAG **P214-G**; data **P215-I**; certification **P215-O**; marketplace publish **P215-P**; copilots **P215-F / P214-Z**; publications **Document Exchange**; dual-use ethics **P215-K / Workflow**.
6. Principle: *MEOS Quantum Research Platform SHALL provide the scientific intelligence foundation enabling discovery, experimentation, collaboration and evolution of future quantum capabilities.*
7. Forbidden: module-local LLM SDKs, PDF/blob storage for publications, ungated dual-use research without governance.
8. Forbidden siblings: `quantum_research_platform`, `quantum_innovation_lab_platform`, `quantum_discovery_platform`, `quantum_experiment_platform`, `quantum_future_radar_platform`.
9. Future **P215-R** must deepen executive strategy intelligence **without** replacing P215-K as governance SoR.

## Consequences

- Quantum stores research/experiment/discovery refs and projections; kernels, RAG, and documents remain peer SoRs.
- Catalog + aggregates + ACL + readiness live under `contexts/quantum` (`qc_platform_research`, `qc_research_*`).
- Next: P215-R Quantum Strategy / Executive Intelligence (align with ADR-403).

## Alternatives considered

| Option | Rejected because |
|---|---|
| Fork P215-G solvers in research | Violates scientific SoR reuse |
| Embed OpenAI SDK in research | Violates AI Platform Standard |
| Store publication PDFs in quantum tables | Violates Document Exchange |
| New sibling research BC | Sibling BC ban |
| Bypass P215-K for dual-use experiments | Violates governance trust gate |
