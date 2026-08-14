# Enterprise Data Security — Data Access Governance (P211-H)

**SoR:** `data_security` · **ADR:** 383 · **API:** `/api/v1/data-security/access*` · **Capability:** `CAP-PLT-DS-001`

## Mission

Create an intelligent enterprise data access governance platform capable of discovering data access relationships, managing data entitlements, enforcing least privilege, automating access reviews, preventing excessive permissions, supporting business data ownership, providing continuous authorization intelligence, and protecting sensitive and regulated data.

## Vision

Autonomous Data Access Governance Fabric: every data access path is visible, every permission has an owner, every entitlement has a business purpose, every access request is risk evaluated, every privilege is continuously reviewed, every data access decision is explainable.

## Architecture flow

Data Assets → P211-D Inventory → P211-E Classification Context → Data Access Governance → Policy Decision Intelligence → Authorization Enforcement → Continuous Monitoring

## Hard laws (quality gates)

- Never Data permissions are invisible
- Never Ownership is undefined
- Never Access reviews are manual only
- Never Risk evaluation is missing
- Never AI access is unmanaged
- Never Least privilege cannot be enforced
- Never Authorization decisions are not auditable

## Boundaries

| Concern | Owner |
|---|---|
| Access policy / entitlement / request / review catalog | `data_security` |
| Inventory / classification context | P211-D / P211-E |
| Posture / exposure context | P211-F DSPM |
| DLP enforcement signals | P211-G |
| Identity attributes / lifecycle | P207 / Identity |
| PDP / authorization decisions | P208 |
| Cryptographic binding | P209 |
| Threat / insider signals | P210 |
| Approval / certification workflows | Workflow Engine |
| Policy evaluation | Policy Engine |
| Risk inference | Enterprise AI |

## Forbidden

- Sibling BC `data_access_governance`, `entitlement_management`, `access_certification`
- Replacing P208 PDP inside this module
- Manual-only certification with no automation path
- Unmanaged AI agent entitlements
- Module-local LLM SDKs
