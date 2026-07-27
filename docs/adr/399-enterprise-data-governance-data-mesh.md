# ADR-399: Data Governance — Data Mesh & Data Product Platform (P212-F)

## Status

Accepted — P212-F Data Mesh Architecture & Data Product Platform

## Context

ADR-392–393, ADR-397–398 established SoR `data_governance` through ownership and quality. P212-F delivers the **MEOS Enterprise Data Mesh Fabric**: domain ownership, data-as-product lifecycle, contracts, self-service platform, federated computational governance, product intelligence, KG/twin bindings — as a logical surface under `data_governance`, not sibling `data_mesh` / `data_product_platform` BCs.

**Hard laws:** SoR remains `data_governance`. Surfaces under `/data-governance/mesh*`. Data SHALL be managed as a strategic product owned by business domains. Never incomplete mesh or product platform. Never missing DDD, domain model, lifecycle, contracts, quality/ownership integration, AI, KG, twin, CQRS, events, microservices, or scalability. Ownership via P212-D; quality via P212-E; identity P207; PDP P208; crypto P209; cyber P210; security/privacy P211; AI via Enterprise AI.

## Decision

1. SoR remains `data_governance`
2. Surfaces under `/api/v1/data-governance/mesh*`
3. Law: `ENTERPRISE_DATA_GOVERNANCE_DATA_MESH.md`
4. Catalogs: `DATA_GOVERNANCE_MESH_*.v1.yaml`
5. Runtime: `dg_platform_mesh.py`; aggregates; ACL; foundation
6. Quality gates enforce mesh, products, DDD, domains, lifecycle, contracts, quality integration, KG, twin, AI, CQRS, events, microservices, scalability

## Consequences

- Foundation for P212-G marketplace / metadata surfaces
- Forbidden siblings unchanged: `data_mesh`, `data_product_platform`, …

## References

ADR-392 · ADR-393 · ADR-397 · ADR-398 · Data Mesh principles · P207–P211
