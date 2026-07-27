# ADR-397: Data Governance — Ownership, Stewardship & Accountability (P212-D)

## Status

Accepted — P212-D Data Ownership, Stewardship & Accountability Platform

## Context

ADR-392–393 established SoR `data_governance` strategy and MVS. P212-D delivers the **Enterprise Data Accountability Fabric**: ownership registry, steward operating model, accountability dimensions, ownership intelligence, KG/twin bindings, and data-mesh federated ownership — as a logical surface under `data_governance`, not sibling ownership/stewardship BCs.

**Hard laws:** SoR remains `data_governance`. Surfaces under `/data-governance/ownership*`. Every enterprise data asset SHALL have a clear accountable owner. Never incomplete ownership or stewardship architectures. Never missing accountability framework, DDD/CQRS/event sourcing, mesh/KG/twin/AI ownership intelligence, zero-trust alignment, or enterprise scalability. Identity via P207; PDP via P208; crypto via P209; cyber via P210; security/privacy intelligence via P211; AI via Enterprise AI; approvals via Workflow; policies via Policy Engine.

## Decision

1. SoR remains `data_governance`
2. Surfaces under `/api/v1/data-governance/ownership*`
3. Law: `ENTERPRISE_DATA_GOVERNANCE_OWNERSHIP_STEWARDSHIP.md`
4. Catalogs: `DATA_GOVERNANCE_OWNERSHIP_*.v1.yaml`
5. Runtime: `dg_platform_ownership.py`; aggregates; ACL; foundation
6. Quality gates enforce ownership, stewardship, accountability, DDD, CQRS, events, mesh, KG, twin, AI, zero trust, scalability

## Consequences

- Foundation for P212-E quality, F mesh/products, and later intelligence surfaces
- Forbidden siblings: `data_ownership`, `data_stewardship`, `accountability_platform`, `ownership_registry`
- P212-C domain map may land later; ownership surface is capability-complete without sibling BC

## References

ADR-392 · ADR-393 · DATA MESH · AI_PLATFORM_STANDARD.md · P207–P211
