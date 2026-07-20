# ADR-326: Identity Intelligence — Knowledge Graph Intelligence & Reasoning (P207-K)

## Status

Accepted — P207-K Knowledge Graph Intelligence & Reasoning Engine

## Context

P207-A–J established strategy through access governance on SoR `identity_intelligence`. P207-K delivers the **Knowledge Graph Intelligence & Reasoning Engine**: semantic ontology, relationship intelligence, rule/semantic/AI/GNN reasoning, attack path analysis, semantic search, and explainable graph conclusions — without data-only graphs, undefined relationships, unexplained AI, missing security context, absent ontology governance, or weak II integration.

**Hard laws:** SoR remains `identity_intelligence` (reasoning/intelligence). Graph **storage SoR** remains peer `directory` (P205-H) — orchestrate projections, never duplicate. Surfaces under `/graph*`. Explainable reasoning required. Security context required. Ontology governed. AI via AI Platform. Search via Search Platform ACL. Never invent sibling graph BC. Never embed LLM SDK.

## Decision

1. SoR remains `identity_intelligence`
2. Graph storage peer remains `directory` (P205-H)
3. Surfaces under `/api/v1/identity-intelligence/graph*`
4. Law: `ENTERPRISE_IDENTITY_INTELLIGENCE_KNOWLEDGE_GRAPH_REASONING.md`
5. Catalogs: `II_GRAPH_*.v1.yaml`
6. Runtime: `ii_platform_graph.py`; aggregates: `ii_graph_aggregates.py`; ACL: `ii_graph_acl.py`; validator: `ii_graph_foundation.py`
7. Quality gates reject data-only graph, undefined relationships, unexplained AI, missing security context, absent ontology governance, weak II integration

## Consequences

- Risk/behavior/agents consume graph reasoning contracts
- Authoritative graph persistence lives in `directory`; II holds reasoning sessions and explainable conclusions

## References

ADR-316–325 · directory P205-H · Search Platform · AI Platform · Zero Trust · Platform Charter
