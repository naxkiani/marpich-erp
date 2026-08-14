# ADR 520 — Enterprise Biotechnology Bio Autonomous Intelligence Platform (P217-U)

## Status

Accepted

## Context

P217-T established bio future intelligence evolution. P217-U defines Bio Autonomous Intelligence: autonomous biological systems, bio-AI autonomy, self-optimizing ecosystems, closed-loop optimization and governed autonomy — before Bio General Intelligence (P217-V).

## Decision

1. SoR remains `biotechnology` / `CAP-PLT-BIO-001` for autonomous *intelligence*.
2. Fabric: `meos_bio_autonomous_intelligence_fabric`.
3. API: `/api/v1/biotechnology/bio-autonomous*`.
4. Six autonomy layers; autonomous biology OS, bio-AI autonomy engine, self-optimizing ecosystem, autonomous twin, KG, agents.
5. All inference via P214-Z ACL only — `no_module_local_llm`.
6. Human autonomy oversight and responsible bio autonomy controls mandatory; never unsupervised autonomous bio action; never opaque autonomous decisions.
7. Twins via P217-G; future models via P217-T; security via P217-S; robotics via P216-Z; quantum via P215-Z.
8. Never replace Core, AI, Quantum, Robotics, hospital EMR, LIMS, pharmacy, prior P217 fabrics including Bio Future.
9. Foundation for P217-V.

## Consequences

Positive: governed closed-loop autonomy layer for Bio-GI and later civilization autonomy phases.  
Negative: autonomy catalogs must remain under human safety governance as decision authority expands.

## Alternatives rejected

- Sibling `bio_autonomous` BC owning Core or AI platform capabilities.
- Module-local LLM or unsupervised autonomous bio actions without human governance.
- Merging peer SoRs (EMR/LIMS/pharmacy) into biotechnology without ACL peers.

## Related

Law: `ENTERPRISE_BIOTECHNOLOGY_BIO_AUTONOMOUS.md` · Prior: ADR 499–519 · Next: P217-V
