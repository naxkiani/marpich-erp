# ADR-425: Enterprise AI — Generative AI & LLM Platform (P214-E)

## Status

Accepted — P214-E Enterprise Generative AI & Large Language Model (LLM) Platform

## Context

ADR-421–424 established SoR `ai` foundation, mission/scope, DDD, and MLOps. P214-E catalogs the **MEOS Enterprise Cognitive Intelligence Layer**: foundation models, LLMOps, prompts, RAG, vectors, assistants/copilots, multimodal, and GenAI governance — as logical capabilities inside `ai`, not sibling BCs.

**Principle:** Enterprise Generative AI SHALL provide the cognitive interface allowing humans, applications and AI agents to communicate with enterprise knowledge and intelligence.

## Decision

1. SoR remains `ai` (CAP-PLT-AI-001)
2. Surfaces under `/api/v1/ai/genai*`
3. Law: `ENTERPRISE_AI_GENERATIVE_LLM.md`
4. Catalogs: `AI_GENAI_*.v1.yaml`
5. Runtime: `ai_platform_genai.py`; aggregates; ACL; foundation
6. Aligns with P212 RAG/data, P213-L knowledge graph, P213-O deploy, P214-A/C/D, P207–P211 via ACL
7. Quality gates enforce GenAI/LLM stack, CQRS, events, microservices, zero trust, cloud-native
8. Modules never embed LLM/vector SDKs — inference via Enterprise AI SoR only

## Consequences

- P214-F deepens AI Agent & Autonomous Intelligence on the same SoR
- Forbidden siblings include generative_ai, llm_platform, vector_intelligence, etc.

## References

ADR-421 · ADR-422 · ADR-423 · ADR-424 · AI_PLATFORM_STANDARD.md · P212 · P213-L
