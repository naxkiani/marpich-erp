# ADR-421: Enterprise AI Platform Foundation (P214-A)

## Status

Accepted — P214-A Enterprise Artificial Intelligence, Machine Learning & Generative AI Platform Foundation

## Context

Volume 06 continues after P212 (data governance) and P213 (BI / decision intelligence). P214 elevates SoR `ai` into the **MEOS Enterprise AI Intelligence Fabric** — AI-PaaS, ML, generative AI, LLM management, vector intelligence, agents, and AI governance — without inventing sibling BCs (`ml_platform`, `generative_ai`, `llm_platform`, …).

**Principle:** Enterprise AI Platform SHALL provide the intelligence foundation enabling every MEOS domain to consume, create, govern and operationalize artificial intelligence.

## Decision

1. SoR remains `ai` (CAP-PLT-AI-001)
2. Surfaces under `/api/v1/ai/foundation*`
3. Law: `ENTERPRISE_AI_PLATFORM_FOUNDATION.md`
4. Catalogs: `AI_FOUNDATION_*.v1.yaml`
5. Runtime: `ai_platform_foundation.py`; aggregates; ACL; foundation validator
6. Consumes P212 data products / KG / twin via ACL; P213-L/M/O via ACL; security via P207–P211
7. Modules consume this SoR only — never embed LLM / vector SDKs (`AI_PLATFORM_STANDARD.md`)
8. Quality gates enforce AI-PaaS, ML, GenAI, LLM, lifecycle, MLOps, vectors, governance, agents, graph/twin, CQRS, events, microservices, API-first, zero trust, cloud-native

## Consequences

- P214-B+ deepen mission, vision, and strategic intelligence scope on the same SoR
- Existing `/api/v1/ai/assist` remains; foundation catalog is additive
- Forbidden siblings unchanged

## References

ADR-394 · ADR-416–419 · AI_PLATFORM_STANDARD.md · CORE_PLATFORM.md · ai context
