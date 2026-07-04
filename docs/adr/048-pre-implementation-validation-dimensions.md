# ADR-048: Pre-Implementation Validation — Fifteen Dimensions Realignment

## Status

Accepted

## Context

ADR-033 established the architecture validation gate with fifteen dimensions focused on modularity, SOLID, caching, cloud readiness, and developer experience. Product leadership now mandates explicit validation of platform dimensions before any feature: Architecture, DDD, Security, Scalability, Performance, Testing, AI Integration, Documentation, Accessibility, Localization, Observability, Workflow, Audit, Policy Compliance, and Plugin Compatibility.

The enterprise platform stack now includes Audit, Observability, Workflow, Policy Engine, Compliance, Feature Flags, and Plugin Platform — each must be validated in design, not discovered in review.

## Decision

1. Realign **`docs/architecture/ARCHITECTURE_VALIDATION.md`** to the fifteen dimensions above.

2. Update **`scripts/validate-architecture.py`** dimension list and critical dimensions:
   - Critical: Architecture, DDD, Security, Audit (all ≥ 4)

3. Update **`.cursor/rules/marpich-architecture-validation.mdc`** and **`marpich-development-protocol.mdc`** to enforce:
   - **If any validation fails → STOP implementation**
   - **Recommend architectural improvements**
   - **Only then generate production code**

4. ADR-033 remains valid for the gate mechanism; this ADR supersedes its dimension list.

## Consequences

- Agents must score all fifteen dimensions before writing production code
- Platform services (workflow, audit, policy, plugins) are design-time requirements
- Accessibility and localization validated at architecture phase for UI features
- Scorecard template updated in validation script and docs

## Alternatives considered

- Keep ADR-033 dimensions + add platform as appendix — rejected (two competing checklists)
- Fully automated fifteen-dimension scoring — rejected (nuance requires judgment)
- Post-merge quality gate only — rejected (does not prevent bad design)
