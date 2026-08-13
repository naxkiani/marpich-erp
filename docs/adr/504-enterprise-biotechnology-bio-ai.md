# ADR 504 — Enterprise Biotechnology Bio-AI Intelligence Platform (P217-E)

## Status

Accepted

## Context

P217-D established scientific infrastructure. P217-E defines Bio-AI reference architecture, biological foundation models, AI Biology Engine, Computational Life Intelligence Core (CLIC), scientific agents, knowledge graph integration, model lifecycle and responsible governance — before Synthetic Biology (P217-F).

## Decision

1. SoR remains `biotechnology` / `CAP-PLT-BIO-001`.
2. Fabric: `meos_bio_ai_intelligence_fabric`.
3. API: `/api/v1/biotechnology/bio-ai*`.
4. Five Bio-AI layers; five foundation model families; AI Biology Engine + CLIC catalogs.
5. All inference via P214-Z ACL only — `no_module_local_llm`.
6. Explainable decisions required — never opaque unexplainable bio-AI decisions.
7. Never replace Core, AI, Quantum, Robotics, hospital EMR, LIMS, pharmacy, prior P217 fabrics.
8. Foundation for P217-F.

## Consequences

Positive: governed bio intelligence layer for synthetic/digital-health phases.  
Negative: catalog must stay aligned as foundation-model ops deepen.

## Alternatives rejected

- Sibling `bio_ai` BC outside SoR biotechnology.
- Module-local OpenAI/Anthropic SDK.
- Owning EMR clinical decision SoR.

## Related

Law: `ENTERPRISE_BIOTECHNOLOGY_BIO_AI.md` · Prior: ADR 499–503 · Next: P217-F
