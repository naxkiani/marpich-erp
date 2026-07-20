# ADR-321: Identity Intelligence — Identity Digital Twin Platform (P207-F)

## Status

Accepted — P207-F Identity Digital Twin Platform

## Context

P207-A–E established strategy, mission, DDD, autonomous ops, and AI agents on SoR `identity_intelligence`. P207-F delivers the **Identity Digital Twin Platform**: twin engine orchestration, real-time synchronization, simulation, impact analysis, predictive intelligence, knowledge-graph integration, and twin AI agents — without treating twins as static data copies, omitting sync/simulation/impact, weak AI, or undefined security.

**Hard laws:** Deployable SoR remains `identity_intelligence`. Twin **storage SoR** remains peer `identity_digital_twin` (orchestrate refs only; never duplicate). Surfaces under `/twins*` (distinct from `/agents*` and `/autonomous*`). Simulation before execution. Impact analysis required. AI via AI Platform. Graph via directory (P205-H). HITL for high-impact mutations. Auditable. Never invent sibling twin BC.

## Decision

1. SoR remains `identity_intelligence` (orchestration / intelligence)
2. Twin persistence SoR remains `identity_digital_twin`
3. Surfaces under `/api/v1/identity-intelligence/twins*`
4. Law: `ENTERPRISE_IDENTITY_INTELLIGENCE_DIGITAL_TWIN_PLATFORM.md`
5. Catalogs: `II_TWIN_*.v1.yaml`
6. Runtime: `ii_platform_twins.py`; aggregates: `ii_twin_aggregates.py`; ACL: `ii_twin_acl.py`; validator: `ii_twin_foundation.py`
7. Quality gates reject data-copy-only twins, absent sync, missing simulation, unavailable impact analysis, weak AI, undefined security, twin SoR duplication

## Consequences

- Risk/behavior/healing phases consume twin simulation & impact contracts
- Authoritative twin state lives in `identity_digital_twin`; II holds orchestration projections and simulation sessions

## References

ADR-316–320 · identity_digital_twin · directory (P205-H) · AI Platform · Workflow · Zero Trust · Platform Charter
