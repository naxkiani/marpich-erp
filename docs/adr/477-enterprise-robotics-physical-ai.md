# ADR 477 — Enterprise Robotics Physical AI Engine (P216-E)

## Status

Accepted

## Context

P216-D established EROS runtime and fleet control. P216-E defines the intelligence layer: perception, Physical AI, cognitive robotics, autonomous decisions, world model, robot memory, knowledge graph, digital twin sync, and responsible AI — preparing for P216-F industrial automation.

## Decision

1. SoR remains `robotics` / `CAP-PLT-RB-001`.
2. Fabric: `meos_physical_ai_intelligence_fabric`.
3. API: `/api/v1/robotics/physical-ai*`.
4. Core domain: Physical AI Intelligence Management; aggregate PhysicalAIAggregate.
5. Seven bounded contexts (perception through memory).
6. All model inference via P214-Z ACL — never embed OpenAI/Anthropic/local LLM SDKs in robotics.
7. Safety-critical autonomy policy-gated; opaque/unexplainable physical decisions forbidden.
8. Never replace Core, AI, Quantum, or P216 foundation through runtime fabrics.

## Consequences

Positive: embodied intelligence with enterprise AI governance.  
Negative: model registry and GPU infra owned by AI Platform / Integration — robotics holds intents and local projections only.

## Alternatives rejected

- Embedding foundation models inside robotics BC.
- Ungated reactive control loops without safety envelopes.
- Sibling physical-ai bounded context outside SoR robotics.

## Related

Law: `ENTERPRISE_ROBOTICS_PHYSICAL_AI.md`  
Roadmap: `robotics/P216_MASTER_SERIES_ROADMAP.v1.yaml`
