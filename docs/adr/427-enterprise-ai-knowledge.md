# ADR-427: Enterprise AI — Knowledge, RAG & Cognitive Intelligence (P214-G)

## Status

Accepted — P214-G Enterprise AI Knowledge, RAG & Cognitive Intelligence Platform

## Context

ADR-421–426 established SoR `ai` through Agents. P214-G catalogs the **MEOS Enterprise Cognitive Knowledge Fabric**: knowledge fabric, ingestion, RAG, vectors, semantic intelligence, graph-enhanced RAG, AI memory, context engine, cognitive reasoning, and knowledge governance — as logical capabilities inside `ai`, not sibling BCs.

**Principle:** Enterprise AI Knowledge Platform SHALL provide the trusted cognitive foundation allowing AI systems to understand enterprise context, retrieve relevant knowledge, reason accurately and generate reliable intelligence.

## Decision

1. SoR remains `ai` (CAP-PLT-AI-001)
2. Surfaces under `/api/v1/ai/knowledge*`
3. Law: `ENTERPRISE_AI_KNOWLEDGE.md`
4. Catalogs: `AI_KNOWLEDGE_*.v1.yaml`
5. Runtime: `ai_platform_knowledge.py`; aggregates; ACL; foundation
6. Aligns with P212 governance, P213-L graph, P214-E GenAI, P214-F agent memory, Documents/Search via ACL
7. Modules never embed vector/embedding SDKs — via Enterprise AI SoR only
8. Documents store `document_id` references only (Document Exchange)

## Consequences

- P214-H deepens AI Governance / Responsible AI / Risk on the same SoR
- Forbidden siblings include `rag_platform`, `vector_intelligence`, `ai_knowledge`, etc.

## References

ADR-421–426 · AI_PLATFORM_STANDARD.md · P212 · P213-L · ENTERPRISE_DOCUMENT_EXCHANGE.md
