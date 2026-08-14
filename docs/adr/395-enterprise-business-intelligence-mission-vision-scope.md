# ADR-395: Enterprise BI — Mission, Vision & Scope (P213-B)

## Status

Accepted — P213-B Mission, Vision & Enterprise Decision Intelligence Scope

## Context

ADR-394 established SoR `analytics` as Enterprise BI Fabric. P213-B defines mission, vision, strategic objectives, decision-intelligence scope, capability map, operating/governance models, AI evolution, maturity, graph/twin alignment, and enterprise roadmap — without sibling BI BCs.

**Mission:** MEOS Enterprise Intelligence mission is to transform trusted enterprise data into actionable knowledge, predictive insights, and intelligent decisions.

## Decision

1. SoR remains `analytics`
2. Surfaces under `/api/v1/analytics/mission*`
3. Law: `ENTERPRISE_BUSINESS_INTELLIGENCE_MISSION_VISION_SCOPE.md`
4. Catalogs: `BI_MVS_*.v1.yaml`
5. Runtime: `bi_platform_mission_scope.py`; aggregates; ACL; foundation
6. Aligns with P212-J knowledge graph and P212-L digital twin; AI via Enterprise AI only

## Consequences

- P213-C catalogs DDD bounded contexts and aggregates on the same SoR
- Forbidden siblings unchanged

## References

ADR-394 · ADR-392 · ADR-393 · ADR-402 · ADR-404 · P212 series
