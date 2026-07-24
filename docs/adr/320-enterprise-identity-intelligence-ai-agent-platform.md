# ADR-320: Identity Intelligence — Identity AI Agent Platform (P207-E)

## Status

Accepted — P207-E Identity AI Agent Platform

## Context

P207-A–D established strategy, mission, DDD, and autonomous operations on SoR `identity_intelligence`. P207-E delivers the **governed Identity AI Agent Platform**: agent runtime, orchestrator, knowledge/RAG layer, memory, specialized agents (analyst, governance, security, operations, compliance, architecture), tool framework, human–AI collaboration, Zero Trust agent security, CQRS/events, and MLOps governance — without permissionless agents, non-explainable decisions, uncontrolled knowledge, absent human governance, unaudited AI actions, or undefined security boundaries.

**Hard laws:** SoR remains `identity_intelligence`. Surfaces under `/agents*` (distinct from `/autonomous*`). Inference via AI Platform only. Tools permission-scoped. HITL for high-impact. Explainable. Auditable. Workflow for approvals. Never invent sibling agent BC. Never embed LLM SDK. Never chatbot-only.

## Decision

1. SoR remains `identity_intelligence`
2. Surfaces under `/api/v1/identity-intelligence/agents*`
3. Law: `ENTERPRISE_IDENTITY_INTELLIGENCE_AI_AGENT_PLATFORM.md`
4. Catalogs: `II_AGENT_*.v1.yaml`
5. Runtime: `ii_platform_agents.py`; aggregates: `ii_agent_aggregates.py`; ACL: `ii_agent_acl.py`; validator: `ii_agent_foundation.py`
6. Quality gates reject permissionless agents, non-explainable decisions, uncontrolled knowledge, missing human governance, unaudited AI actions, undefined security boundaries, sibling BC, embedded LLM

## Consequences

- Twin/risk/behavior phases consume agent contracts
- AI Platform remains inference SoR; agents are contracts + orchestration projections

## References

ADR-316–319 · AI Platform · AI Governance · Workflow · Policy · Zero Trust · Platform Charter
