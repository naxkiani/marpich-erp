# ADR-417: Analytics — AI Native Analytics & Autonomous Decision Intelligence (P213-M)

## Status

Accepted — P213-M AI Native Analytics & Autonomous Decision Intelligence Platform

## Context

ADR-394–396 / 408–416 established SoR `analytics` through strategy, MVS, DDD, reporting, warehouse, lakehouse, semantic/OLAP, self-service, advanced, predictive, prescriptive, and decision knowledge graph. P213-M catalogs the **MEOS Autonomous Decision Intelligence Fabric**: agents, multi-agent collaboration, reasoning, executive copilot, autonomy levels, and AI governance — as logical capabilities inside `analytics`, with all inference delegated to Enterprise AI.

**Principle:** Every enterprise decision SHALL be supported by AI reasoning, enterprise knowledge, governance policies and continuous learning.

**Hard laws:** Surfaces under `/api/v1/analytics/ai*`. No module-local LLM SDKs. Federate P212-J/L and P213-G/J/K/L via ACL. Integrate P207–P212 for identity, authz, crypto, cyber, data security, and governance.

## Decision

1. SoR remains `analytics`
2. Surfaces under `/api/v1/analytics/ai*`
3. Law: `ENTERPRISE_BUSINESS_INTELLIGENCE_AI.md`
4. Catalogs: `BI_AI_*.v1.yaml`
5. Runtime: `bi_platform_ai.py`; aggregates; ACL; foundation
6. Quality gates enforce AI native/autonomy/agents/copilot/governance/KG/twin, CQRS, events, microservices, API-first, zero trust, cloud-native deployment

## Consequences

- P213-N deepens CQRS, Events, APIs & Microservices platform surfaces on the same SoR
- Forbidden siblings unchanged

## References

ADR-394 · ADR-395 · ADR-396 · ADR-408–416 · P207–P212 · CORE_PLATFORM.md · AI_PLATFORM_STANDARD.md
