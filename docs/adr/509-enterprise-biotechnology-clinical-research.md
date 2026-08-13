# ADR 509 — Enterprise Biotechnology Clinical Research Intelligence Platform (P217-J)

## Status

Accepted

## Context

P217-I established precision medicine and genomics AI. P217-J defines Clinical Research Intelligence: AI clinical trials, scientific discovery, biomedical research automation, research knowledge graph and clinical innovation governance — before Drug Discovery (P217-K).

## Decision

1. SoR remains `biotechnology` / `CAP-PLT-BIO-001` for research *intelligence* — never EMR/LIMS/pharmacy SoR.
2. Fabric: `meos_clinical_innovation_intelligence_fabric`.
3. API: `/api/v1/biotechnology/clinical-research*`.
4. Six clinical-research layers; AI trial OS, discovery engine and research automation catalogs.
5. All inference via P214-Z ACL only — `no_module_local_llm`.
6. Clinical trials require ethics approval — never autonomous clinical trial without ethics approval.
7. Human researcher oversight mandatory for discovery and trial decisions.
8. Never replace Core, AI, Quantum, Robotics, hospital EMR, LIMS, pharmacy, prior P217 fabrics including Precision Medicine.
9. Foundation for P217-K.

## Consequences

Positive: governed clinical innovation layer for drug discovery and bio-manufacturing phases.  
Negative: ethics / regulatory catalogs must stay aligned as trial automation deepens.

## Alternatives rejected

- Sibling `clinical_research` BC owning EMR trial records.
- Module-local LLM or autonomous trial launch without Workflow ethics gate.
- Owning hospital/clinic operational SoR.

## Related

Law: `ENTERPRISE_BIOTECHNOLOGY_CLINICAL_RESEARCH.md` · Prior: ADR 499–508 · Next: P217-K
