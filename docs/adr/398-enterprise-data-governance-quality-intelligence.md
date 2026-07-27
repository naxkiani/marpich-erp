# ADR-398: Data Governance — Data Quality Intelligence (P212-E)

## Status

Accepted — P212-E Enterprise Data Quality Intelligence Platform

## Context

ADR-392–393 and ADR-397 established SoR `data_governance` through ownership/stewardship. P212-E delivers the **MEOS Enterprise Data Trust Engine**: quality dimensions, rule engine, measurement/scoring, continuous monitoring, remediation, AI quality intelligence, KG/twin bindings, and data-mesh quality contracts — as a logical surface under `data_governance`, not a sibling `data_quality_platform` BC.

**Hard laws:** SoR remains `data_governance`. Surfaces under `/data-governance/quality*`. Trusted intelligence requires trusted data. Never incomplete quality intelligence architecture. Never missing DDD, rule/measurement architectures, AI quality intelligence, mesh/KG/twin, CQRS/event sourcing, microservices, or enterprise scalability. Ownership/stewardship via P212-D. Identity P207; PDP P208; crypto P209; cyber P210; security/privacy P211; AI via Enterprise AI; approvals via Workflow; policies via Policy Engine.

## Decision

1. SoR remains `data_governance`
2. Surfaces under `/api/v1/data-governance/quality*`
3. Law: `ENTERPRISE_DATA_GOVERNANCE_QUALITY_INTELLIGENCE.md`
4. Catalogs: `DATA_GOVERNANCE_QUALITY_*.v1.yaml`
5. Runtime: `dg_platform_quality.py`; aggregates; ACL; foundation
6. Quality gates enforce complete quality intelligence, DDD, rules, measurement, AI, mesh, KG, twin, CQRS, events, microservices, scalability

## Consequences

- Foundation for P212-F mesh/products quality contracts
- Forbidden siblings: `data_quality_platform`, `quality_rule_engine`, `quality_monitoring_platform`, `quality_remediation_platform`

## References

ADR-392 · ADR-393 · ADR-397 · AI_PLATFORM_STANDARD.md · P207–P211
