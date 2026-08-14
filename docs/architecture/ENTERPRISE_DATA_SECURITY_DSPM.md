# Enterprise Data Security — DSPM Posture Management (P211-F)

**SoR:** `data_security` · **ADR:** 381 · **API:** `/api/v1/data-security/dspm*` · **Capability:** `CAP-PLT-DS-001`

## Mission

Create an intelligent enterprise data security posture platform capable of discovering all enterprise data assets, understanding sensitive data exposure, measuring security posture, identifying misconfigurations, detecting excessive access, prioritizing risks, recommending remediation, and continuously improving security posture.

## Vision

Living Enterprise Data Security Posture Intelligence Fabric: every data asset is visible, every exposure is measurable, every risk has context, every vulnerability has ownership, every remediation action is intelligent, data security becomes proactive instead of reactive.

## Architecture flow

Enterprise Data Estate → Data Discovery Layer → Sensitive Data Intelligence → Security Posture Engine → Risk Analysis Intelligence → Autonomous Remediation Layer → Continuous Security Monitoring

## Hard laws (quality gates)

- Never Data assets are unknown
- Never Security posture cannot be measured
- Never Exposure risks are invisible
- Never Findings have no ownership
- Never Remediation is manual only
- Never Continuous assessment is unavailable

## Boundaries

| Concern | Owner |
|---|---|
| DSPM posture / exposure / risk / remediation catalog | `data_security` |
| Inventory inputs | P211-D discovery surface |
| Classification / sensitivity | P211-E classification surface |
| Access risk analysis | P208 Authorization (+ ACL) |
| Encryption / key material | `secrets` (P209) |
| Threat / cyber signals | `cyber_security` (P210) |
| Risk inference | Enterprise AI |
| Remediation approval | Workflow Engine |
| Policy evaluation | Policy Engine |

## Forbidden

- Sibling BC `dspm`, `dspm_platform`, `posture_management`
- Manual-only remediation with no automation path
- Unowned findings
- Invisible exposure / unknown assets
- Module-local LLM SDKs
