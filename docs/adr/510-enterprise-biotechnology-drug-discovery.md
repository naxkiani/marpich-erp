# ADR 510 — Enterprise Biotechnology Drug Discovery Intelligence Platform (P217-K)

## Status

Accepted

## Context

P217-J established clinical research and AI clinical trials. P217-K defines Drug Discovery Intelligence: AI drug design, molecular discovery, pharmaceutical knowledge graph, drug digital twins and responsible pharmaceutical AI governance — before Biomedical Manufacturing (P217-L).

## Decision

1. SoR remains `biotechnology` / `CAP-PLT-BIO-001` for drug *intelligence* — never pharmacy dispense/EMR/LIMS SoR.
2. Fabric: `meos_drug_intelligence_fabric`.
3. API: `/api/v1/biotechnology/drug-discovery*`.
4. Six drug-discovery layers; AI design, molecular discovery and computational drug intelligence catalogs.
5. All inference via P214-Z ACL only — `no_module_local_llm`.
6. Human scientific oversight mandatory; never unvalidated therapeutic candidate release.
7. Quantum readiness via P215-Z ACL; simulation via P217-G; clinical translation via P217-J.
8. Never replace Core, AI, Quantum, Robotics, hospital EMR, LIMS, pharmacy, prior P217 fabrics including Clinical Research.
9. Foundation for P217-L.

## Consequences

Positive: governed pharmaceutical discovery layer for manufacturing and supply-chain phases.  
Negative: safety prediction / IP protection catalogs must stay aligned as generative chemistry deepens.

## Alternatives rejected

- Sibling `drug_discovery` BC owning pharmacy formulary SoR.
- Module-local LLM or releasing candidates without scientific validation workflow.
- Merging pharmacy operational SoR into biotechnology.

## Related

Law: `ENTERPRISE_BIOTECHNOLOGY_DRUG_DISCOVERY.md` · Prior: ADR 499–509 · Next: P217-L
