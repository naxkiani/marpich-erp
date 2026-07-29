# Enterprise Data Security — Data Loss Prevention / DLP (P211-G)

**SoR:** `data_security` · **ADR:** 382 · **API:** `/api/v1/data-security/dlp*` · **Capability:** `CAP-PLT-DS-001`

## Mission

Create an intelligent DLP platform capable of preventing sensitive data leakage, detecting unauthorized data transfer, protecting confidential information, controlling data movement, reducing insider risk, protecting AI data interactions, and automating security response.

## Vision

Autonomous Data Protection Fabric: every data movement is understood, every transfer is risk evaluated, every sensitive asset is protected, every user action is context analysed, every leakage attempt is detected, every violation is automatically handled.

## Architecture flow

Enterprise Data Assets → P211-D Discovery → P211-E Classification → DLP Policy Intelligence → Data Monitoring & Detection → Enforcement & Response → Security Operations → Continuous Improvement

## Hard laws (quality gates)

- Never Sensitive data cannot be identified
- Never Data movement cannot be monitored
- Never Policies cannot be enforced
- Never AI leakage is unmanaged
- Never Insider risk is invisible
- Never Violations cannot be investigated
- Never Automated response is unavailable

## Boundaries

| Concern | Owner |
|---|---|
| DLP policy / transfer / violation / incident catalog | `data_security` |
| Inventory / classification context | P211-D / P211-E |
| Posture / exposure context | P211-F DSPM |
| Authorization decisions | P208 |
| Encrypt / crypto actions | P209 `secrets` |
| SOC / SIEM / SOAR | P210 `cyber_security` |
| Identity / insider signals | P207 / Identity |
| Policy evaluation | Policy Engine |
| Approval / quarantine workflows | Workflow Engine |
| Risk / anomaly inference | Enterprise AI |

## Forbidden

- Sibling BC `dlp`, `data_loss_prevention`, `exfiltration_prevention`
- Unmanaged AI prompt/training leakage
- Manual-only response with no automation path
- Module-local LLM SDKs
- Local SIEM/SOAR stacks (use P210)
