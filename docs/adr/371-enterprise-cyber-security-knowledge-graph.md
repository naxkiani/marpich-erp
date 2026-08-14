# ADR-371: Cyber Security — Knowledge Graph & Digital Twin (P210-K)

## Status

Accepted — P210-K Cyber Knowledge Graph & Cyber Security Digital Twin Platform

## Context

ADR-361–370 established SoR `cyber_security` through AI Ops. P210-K delivers the **semantic intelligence foundation**: cyber ontology, entity resolution, knowledge graph, attack graph engine, AI security reasoning, living digital twins, and cyber simulation — without inventing sibling `cyber_graph` / `security_digital_twin` BCs, and without static twins or ungoverned graphs.

**Hard laws:** SoR remains `cyber_security`. Surfaces under `/cyber-security/graph*`. Never security entities without semantic relationships. Never incalculable attack paths. Never static digital twins. Never unavailable AI reasoning. Never missing graph governance. Never inaccurate entity resolution. Never absent simulation. AI reasoning via Enterprise AI Platform; twin sync via events from SOC/SIEM/XDR/ASM/Identity (peer IDs only).

## Decision

1. SoR remains `cyber_security`
2. Surfaces under `/api/v1/cyber-security/graph*`
3. Law: `ENTERPRISE_CYBER_SECURITY_KNOWLEDGE_GRAPH.md`
4. Catalogs: `CYBER_GRAPH_*.v1.yaml`
5. Runtime: `cs_platform_graph.py`; aggregates; ACL; foundation
6. Quality gates enforce semantic relationships, attack paths, living twins, AI reasoning, graph governance, accurate entity resolution, simulation

## Consequences

- Complements P210-D–J as the shared reasoning/graph fabric surface
- Forbidden sibling BCs: `cyber_graph`, `security_digital_twin`, `attack_graph`

## References

ADR-361–370 · STIX 2.x · MITRE ATT&CK · MITRE D3FEND · NIST CSF · NIST ZTA · ISO 27001
