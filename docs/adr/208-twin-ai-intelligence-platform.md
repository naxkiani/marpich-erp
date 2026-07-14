# ADR-208: Twin AI Intelligence Platform — Prediction, Knowledge Graph, Simulation & Reasoning (Prompt 199-C)

## Status

Accepted

## Context

ADR-203 / 203a define Digital Twin projections and kinds. ADR-207 defines Sync Engine and Event Mesh. Prompt **V03-C02-P199-C** requires every twin to become predictive, graph-aware, simulatable, and capable of governed autonomous recommendations.

The platform already owns:

| Capability | Owner |
|------------|-------|
| LLM / inference / embeddings / 14 AI surfaces | AI Platform (`AI_PLATFORM_STANDARD`, `contexts/ai`) |
| Model approval, bias, inference audit, rollback | AI Governance (ADR-172, `ai_governance`) |
| Feature store + MLOps registry / drift training | Financial Data Science (ADR-170) |
| Natural-language analytics / explain | Natural Language Analytics (ADR-171) |
| Identity relationship SoR graph | Directory Identity Graph (ADR-194) |
| Semantic retrieval | Enterprise Search |
| Twin simulation (non-mutating) | `identity_digital_twin` |
| Domain anomaly packs | Banking / FX / Financial Anomaly / AI Security |

Embedding a second ML platform, Neo4j-only SoR, or industry knowledge graphs inside twin would violate Platform Charter, AI Platform Standard, and DDD boundaries.

**Prompt ID:** V03-C02-P199-C · **ADR number:** 208

## Decision

1. Introduce **Twin Intelligence** as a **logical orchestration pack inside** `identity_digital_twin` — not a new AI bounded context and not a new industry KG SoR.  
2. **Prediction:** Twin stores outcome records (`TwinPrediction`); inference executes only via AI Platform; models registered/approved only via AI Governance + FDS feature/model registry.  
3. **Knowledge Graph:** Twin owns **projected edges** (`TwinRelationship`) + ontology catalog; authoritative identity/org/device graph remains Directory (ADR-194); industry subjects remain peer BC refs. Graph query dialects (Cypher/Gremlin/GraphQL) are **adapter ports** over twin graph + directory hydration — no hardcoded graph vendor in domain.  
4. **Simulation:** Expand scenario catalog; runners remain **non-mutating** (`mutation_applied: false`); Monte Carlo / sandbox are configuration profiles, never SoR writers.  
5. **Reasoning / Copilot / Autonomous decisions:** Hybrid plans invoke AI jobs + Policy/AuthZ/Workflow; high-risk actions require Workflow approval — never silent financial/ledger/clinical mutations.  
6. **Anomaly:** Twin anomaly facets are **projections/consumer outcomes**; detection algorithms stay in owning anomaly/AI platforms; twin alert → Notification + Workflow.  
7. **Data platform:** Feature Store / Vector DB / Lake / Warehouse are platform services (FDS, Search embeddings, Analytics/DW); twin never localizes them.  
8. **APIs:** REST under `/api/v1/identity-twins` (+ intelligence sub-resources); GraphQL/gRPC via ADR-198 gateway generation; AsyncAPI from event contracts. Prompt paths `/prediction`, `/simulation`, etc. are **aliases** of twin intelligence operations — not a separate public API surface outside gateway.  
9. Everything configurable: prediction types, ontology, thresholds, simulation rules, reasoning modes, model bindings — **catalog + Policy Engine**. Never hardcode.

## Consequences

- Twin BC grows prediction/graph/intelligence application services; zero OpenAI SDKs or local model weights.  
- Cross-tenant federated learning and analytics require explicit policy + consent gates.  
- Delivery phases C0–C6 defined in architecture law.  
- Consumers on `marpich.twin.intelligence.v1` must stay idempotent.

## References

- [ENTERPRISE_TWIN_AI_INTELLIGENCE_PLATFORM.md](../architecture/ENTERPRISE_TWIN_AI_INTELLIGENCE_PLATFORM.md)  
- ADR-170 · ADR-171 · ADR-172 · ADR-194 · ADR-203 · ADR-203a · ADR-207  
- `AI_PLATFORM_STANDARD.md` · `ENTERPRISE_SEARCH_ENGINE.md`
