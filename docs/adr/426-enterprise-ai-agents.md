# ADR-426: Enterprise AI — Agent & Autonomous Intelligence Platform (P214-F)

## Status

Accepted — P214-F Enterprise AI Agent & Autonomous Intelligence Platform

## Context

ADR-421–425 established SoR `ai` foundation through GenAI/LLM. P214-F catalogs the **MEOS Autonomous Intelligence Fabric**: agent lifecycle, identity, memory, reasoning, tools, multi-agent orchestration, autonomous workflows, digital twins, and agent governance — as logical capabilities inside `ai`, not sibling BCs.

**Principle:** Enterprise AI Agents SHALL become intelligent digital workers capable of understanding goals, reasoning over enterprise knowledge, executing approved actions and continuously improving enterprise operations.

## Decision

1. SoR remains `ai` (CAP-PLT-AI-001)
2. Surfaces under `/api/v1/ai/agents*`
3. Law: `ENTERPRISE_AI_AGENTS.md`
4. Catalogs: `AI_AGENTS_*.v1.yaml`
5. Runtime: `ai_platform_agents.py`; aggregates; ACL; foundation
6. Aligns with P207–P211 identity/trust, P212 data, P213-L graph, P213-O deploy, P214-E GenAI, Workflow Engine via ACL
7. Quality gates enforce agent stack, CQRS, events, microservices, zero trust, cloud-native
8. Modules never embed local agent runtimes — autonomy via Enterprise AI SoR only
9. Human approval for privileged actions via Workflow Engine — never module-local approval engines

## Consequences

- P214-G deepens Knowledge / RAG / Cognitive Intelligence on the same SoR
- Forbidden siblings include `ai_agent_platform`, `agent_platform`, `autonomous_intelligence`, etc.

## References

ADR-421–425 · AI_PLATFORM_STANDARD.md · ENTERPRISE_WORKFLOW_ENGINE.md · P212 · P213-L
