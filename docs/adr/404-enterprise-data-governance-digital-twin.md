# ADR-404: Data Governance — Digital Twin & Simulation Platform (P212-L)

## Status

Accepted — P212-L Data Governance Digital Twin & Simulation Platform

## Context

ADR-392–393 and ADR-397–402 established SoR `data_governance` through ownership, quality, mesh, marketplace, policies, and knowledge graph. P212-L delivers the **MEOS Enterprise Data Governance Digital Twin Fabric**: living governance state model, simulation engine, what-if analysis, risk forecasting, optimization intelligence, KG/AI readiness bindings — as a logical surface under `data_governance`, not a sibling twin BC.

**Hard laws:** SoR remains `data_governance`. Surfaces under `/data-governance/twin*`. Enterprise governance SHALL not only observe reality, it SHALL simulate and optimize future states. AI via Enterprise AI. AuthZ via P208. Policies via P212-H + Policy Engine. Graph sync via P212-J. Quality via P212-E. Mesh via P212-F. AI readiness via P212-K bindings (surface may be planned). Never invent sibling `governance_twin` / `governance_simulation` BCs.

## Decision

1. SoR remains `data_governance`
2. Surfaces under `/api/v1/data-governance/twin*`
3. Law: `ENTERPRISE_DATA_GOVERNANCE_DIGITAL_TWIN.md`
4. Catalogs: `DATA_GOVERNANCE_TWIN_*.v1.yaml`
5. Runtime: `dg_platform_twin.py`; aggregates; ACL; foundation
6. Quality gates enforce twin completeness across state model, simulation, what-if, risk, optimization, AI/KG/mesh/policy integration, CQRS, events, microservices, zero trust, scalability

## Consequences

- Foundation for P212-M CQRS/events/API ops surfaces
- Forbidden siblings remain forbidden

## References

ADR-392 · ADR-393 · ADR-397–402 · P207–P211 · AI_PLATFORM_STANDARD.md
