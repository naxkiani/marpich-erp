# Enterprise Data Security — Classification & Labeling (P211-E)

**SoR:** `data_security` · **ADR:** 380 · **API:** `/api/v1/data-security/classification*` · **Capability:** `CAP-PLT-DS-001`

## Mission

Understand enterprise data meaning, automatically identify sensitive information, assign security classifications, apply data labels, enforce protection requirements, support privacy regulations, and provide classification intelligence.

## Vision

Data Intelligence Classification Fabric: every data asset has a security identity, every dataset has a classification level, every sensitive element is automatically detected, every protection requirement is known, every AI system understands data sensitivity, every security decision is context-aware.

## Architecture flow

Data Sources → P211-D Discovery → Data Profiling → AI Classification Engine → Classification Policy Engine → Label Management → Security Control Integration → Continuous Classification Monitoring

## Hard laws (quality gates)

- Never Data cannot be classified
- Never Sensitive data detection is unavailable
- Never Labels are unmanaged
- Never AI decisions are unexplained
- Never Classification policies are missing
- Never Classification lifecycle is undefined

## Boundaries

| Concern | Owner |
|---|---|
| Classification / labels / taxonomy catalog | `data_security` |
| Inventory inputs | P211-D discovery surface |
| Classification inference | Enterprise AI |
| Policy evaluation | Policy Engine |
| Human approval / review | Workflow Engine |
| Crypto for protected labels | `secrets` (P209) |

## Forbidden

- Sibling BC `data_classification`, `label_management`, `sensitive_data_detection`
- Unexplained AI classification in production
- Unmanaged / ad-hoc labels without catalog
- Module-local LLM SDKs
- Hardcoded policies (use Policy Engine)
