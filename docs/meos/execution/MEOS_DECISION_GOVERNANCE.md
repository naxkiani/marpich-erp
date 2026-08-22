# MEOS Decision Governance

**Date:** 2026-08-19T07:10:00Z  
**Fabric SoR:** [MEOS_DECISION_FABRIC.md](./MEOS_DECISION_FABRIC.md)  
**Registry SoR:** [MEOS_DECISION_REGISTRY.v1.yaml](./MEOS_DECISION_REGISTRY.v1.yaml)  
**P338 overlay.** Not a duplicate workflow or policy product.

## Law

Material decisions require **human authorization**. AI must not approve budget, employment, security policy, or high-impact actions. Evidence must precede recommendation display.

## Decision object (when runtime exists)

Fields: DECISION_ID · TITLE · OWNER · DOMAIN · OBJECTIVE · CONTEXT · OPTIONS · RECOMMENDATION · EVIDENCE · RISK · EXPECTED_OUTCOME · ACTUAL_OUTCOME · STATUS · TIMESTAMP.

**Current:** four YAML phase records at lifecycle **DECIDE**. Owners **NOT_AVAILABLE**. Runtime store **NOT_IMPLEMENTED**.

## Decision rights & escalation

| Risk class | Target path | Actual |
|------------|-------------|--------|
| LOW | Local decision | AuthZ on domain APIs |
| MEDIUM | Managerial review | Workflow **catalog** exists; binding **NOT_AVAILABLE** |
| HIGH | Executive/governance | Policy evaluate + audit; no production exec queue |

Unauthorized users must not approve decisions — enforce via existing JWT + `require_permissions`.

## AI decision safety

AI **MUST NOT** independently: APPROVE_MATERIAL_DECISIONS · CHANGE_BUDGET · CHANGE_EMPLOYMENT · CHANGE_SECURITY_POLICY · OVERRIDE_RISK_CONTROLS · EXECUTE_HIGH_IMPACT_ACTIONS.

Stub `/api/v1/ai/assist` is **not** evidence. Confidence: **NOT_AVAILABLE**. Inferred lineage/classification: **INFERRED_UNVERIFIED**.

## Audit

Record: DECISION · EVIDENCE · ACTOR · TIME · AUTHORITY · ACTION · RESULT. For AI-assisted paths add MODEL · INPUT · RECOMMENDATION · HUMAN_DECISION.

**Current:** git + YAML for phase gates. No runtime mutation audit stream for decisions.

## Privacy

DATA_MINIMIZATION · PURPOSE_LIMITATION · role-scoped executive views. No workforce/customer PII in decision overlay YAML.
