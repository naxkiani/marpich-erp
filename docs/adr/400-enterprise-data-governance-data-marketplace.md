# ADR-400: Data Governance — Enterprise Data Marketplace (P212-G)

## Status

Accepted — P212-G Enterprise Data Marketplace Platform

## Context

ADR-392–393 and ADR-397–399 established SoR `data_governance` through ownership, quality, and mesh/products. P212-G delivers the **MEOS Enterprise Data Marketplace Fabric**: catalog, semantic discovery, consumer experience, access governance, subscriptions, marketplace intelligence, KG/twin bindings — as a logical surface under `data_governance`, not a sibling `data_marketplace` BC.

**Hard laws:** SoR remains `data_governance`. Surfaces under `/data-governance/marketplace*`. Enterprise data SHALL become discoverable, understandable, accessible, and valuable through governed digital experiences. Never incomplete marketplace, catalog, discovery, consumption, access governance, AI recommendations, mesh alignment, KG, twin, CQRS, events, microservices, zero trust, or scalability. Products via P212-F; ownership P212-D; quality P212-E; authz P208; search via Enterprise Search; AI via Enterprise AI; approvals via Workflow.

## Decision

1. SoR remains `data_governance`
2. Surfaces under `/api/v1/data-governance/marketplace*`
3. Law: `ENTERPRISE_DATA_GOVERNANCE_DATA_MARKETPLACE.md`
4. Catalogs: `DATA_GOVERNANCE_MARKETPLACE_*.v1.yaml`
5. Runtime: `dg_platform_marketplace.py`; aggregates; ACL; foundation
6. Quality gates enforce marketplace completeness across catalog, discovery, consumption, access, AI, mesh, KG, twin, CQRS, events, microservices, zero trust, scalability

## Consequences

- Foundation for P212-H policy management surfaces
- Forbidden siblings: `data_marketplace` and related fragment BCs remain forbidden

## References

ADR-392 · ADR-393 · ADR-397 · ADR-398 · ADR-399 · ENTERPRISE_SEARCH_ENGINE.md · P207–P211
