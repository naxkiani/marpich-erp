# ADR 505 — Enterprise Biotechnology Synthetic Biology Intelligence Platform (P217-F)

## Status

Accepted

## Context

P217-E established Bio-AI foundation models and the AI Biology Engine. P217-F defines Synthetic Biology Intelligence: bio design, engineering automation, synthetic life lifecycle, bio manufacturing intelligence, digital twin integration and responsible bioengineering governance — before Biological Simulation (P217-G).

## Decision

1. SoR remains `biotechnology` / `CAP-PLT-BIO-001`.
2. Fabric: `meos_synthetic_biology_intelligence_fabric`.
3. API: `/api/v1/biotechnology/synthetic*`.
4. Five synthetic architecture layers; design engine + automation domains + lifecycle phases catalogs.
5. All inference via P214-Z ACL only — `no_module_local_llm`.
6. Laboratory automation via P216-Z ACL only — never duplicate robotics SoR.
7. Human approval required for synthetic release — never unsupervised synthetic release.
8. Never replace Core, AI, Quantum, Robotics, hospital EMR, LIMS, pharmacy, prior P217 fabrics including Bio-AI.
9. Foundation for P217-G.

## Consequences

Positive: governed synthetic engineering layer for simulation and digital-health phases.  
Negative: safety/ethics catalogs must stay aligned as automation deepens.

## Alternatives rejected

- Sibling `synthetic_biology` BC outside SoR biotechnology.
- Module-local LLM or direct lab-device control.
- Unsupervised release without Workflow approval.

## Related

Law: `ENTERPRISE_BIOTECHNOLOGY_SYNTHETIC.md` · Prior: ADR 499–504 · Next: P217-G
