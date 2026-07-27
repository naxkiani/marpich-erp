# ADR-401: Data Governance — Data Policy Management & Governance Automation (P212-H)

## Status

Accepted — P212-H Data Policy Management & Governance Automation

## Context

ADR-392–393 and ADR-397–400 established SoR `data_governance` through ownership, quality, mesh, and marketplace. P212-H delivers the **MEOS Enterprise Data Policy Intelligence Fabric**: policy taxonomy, lifecycle, rule engine binding, governance automation, compliance monitoring, AI policy intelligence, KG/twin — as a logical surface under `data_governance`.

**Hard laws:** SoR remains `data_governance`. Surfaces under `/data-governance/policies*`. Enterprise data governance SHALL become policy driven, automated, and continuously intelligent. Decision evaluation delegates to Platform Policy Engine / P208 — never a sibling policy BC or module-local PDP. Approvals via Workflow. AI via Enterprise AI.

## Decision

1. SoR remains `data_governance`
2. Surfaces under `/api/v1/data-governance/policies*`
3. Law: `ENTERPRISE_DATA_GOVERNANCE_DATA_POLICIES.md`
4. Catalogs: `DATA_GOVERNANCE_POLICIES_*.v1.yaml`
5. Runtime: `dg_platform_policies.py`; aggregates; ACL; foundation
6. Quality gates enforce policy completeness across lifecycle, rules, automation, intelligence, AI, KG, twin, CQRS, events, microservices, zero trust, scalability

## Consequences

- Foundation for P212-I intelligence surfaces
- Forbidden siblings: `data_policy_platform` and related fragment BCs remain forbidden
- Policy evaluation via `IPolicyEvaluator` / Policy Engine — not duplicated

## References

ADR-392 · ADR-393 · ADR-397–400 · ENTERPRISE_POLICY_ENGINE.md · P207–P211 · P212-D–G
