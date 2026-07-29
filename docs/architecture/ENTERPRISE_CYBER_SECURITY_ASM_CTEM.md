# Enterprise Cyber Security — ASM & CTEM (P210-I)

**SoR:** `cyber_security` · **ADR:** 369 · **API:** `/api/v1/cyber-security/asm*`

## Mission

Continuously discover, classify, assess, prioritize and reduce cyber exposure across assets, identities, workloads, applications, APIs, cloud, AI systems and third-party ecosystems.

## Vision

Autonomous Exposure Management: every asset discovered, every exposure assessed, every attack path visualized, every remediation prioritized, every risk decision intelligence-driven, every asset continuously defensible.

## Architecture layers

Asset Discovery → Asset Inventory → Attack Surface Discovery → Exposure Detection → Vulnerability Intelligence → Attack Path Analysis → Risk Prioritization → Remediation Orchestration → Continuous Validation → Executive Cyber Risk Dashboard

## Hard laws (quality gates)

- Never asset discovery is incomplete
- Never external attack surface is not continuously monitored
- Never risk prioritization ignores business context
- Never attack path analysis is absent
- Never AI recommendations are not explainable
- Never remediation cannot be validated
- Never CTEM lifecycle is not continuous

## Boundaries

| Concern | Owner |
|---|---|
| ASM / EASM / CAASM / CTEM | `cyber_security` (this surface) |
| Remediation playbooks | P210-F SOAR + Workflow approvals |
| Vuln/threat context | P210-H Threat Intelligence |
| Detection signals | P210-E SIEM / P210-G XDR |
| Asset connectors | Integration Platform |
| Enterprise CMDB refs | peer IDs only |

## Forbidden

- Sibling BC `asm`, `ctem`, `easm`, `caasm`
- Incomplete discovery catalogs
- One-shot (non-continuous) external surface scans as the sole model
- Risk scores without business context
- Missing attack path / blast-radius analysis
- Unexplained AI prioritization
- Remediation without verification
- One-pass CTEM (must continuously repeat)

## Compliance

NIST CSF · NIST SP 800-53 · ISO 27001 · CIS Controls · PCI DSS · SOC 2
