# ADR-393: Data Governance — Mission, Vision & Scope (P212-B)

## Status

Accepted — P212-B Mission, Vision & Enterprise Data Governance Scope

## Context

ADR-392 established SoR `data_governance` foundation. P212-B defines the **strategic mission, vision, scope, operating model, maturity model, and MEOS positioning** of the Data Governance Intelligence Layer — bridging Secure Data (P211) and Intelligent Enterprise Operations — without inventing sibling mission/scope BCs.

**Hard laws:** SoR remains `data_governance`. Surfaces under `/data-governance/mission*`. Never undefined mission/vision/scope. Never missing strategic objectives, operating model, maturity model, or AI governance direction. Never missing MEOS integration alignment. Never unclear domain boundaries. Never noncompliant with Enterprise Governance Standard. Out-of-scope crypto/identity/authz/cyber/encryption remain P207–P211.

## Decision

1. SoR remains `data_governance`
2. Surfaces under `/api/v1/data-governance/mission*`
3. Law: `ENTERPRISE_DATA_GOVERNANCE_MISSION_VISION_SCOPE.md`
4. Catalogs: `DATA_GOVERNANCE_MVS_*.v1.yaml`
5. Runtime: `dg_platform_mission_scope.py`; aggregates; ACL; foundation
6. Quality gates enforce mission, vision, scope, objectives, operating model, maturity, AI direction, MEOS alignment, boundaries, EG standard
7. Roadmap: P212-B done; next P212-C Domain Architecture

## Consequences

- Strategic charter for ownership, stewardship, quality, mesh, marketplace, intelligence, AI readiness
- Forbidden siblings unchanged from ADR-392

## References

ADR-392 · P207–P211 · Data Mesh principles · AI_PLATFORM_STANDARD.md
