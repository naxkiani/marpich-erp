# Enterprise Cyber Security — Security Operations Center (SOC) — P210-D

**Prompt:** P210-D · **ADR:** [364](../adr/364-enterprise-cyber-security-soc.md)  
**Builds on:** P210-A–C (ADR-361–363)  
**SoR:** `cyber_security` · **Forbidden:** sibling `soc_platform` BC  
**API:** `/api/v1/cyber-security/soc*`

---

## Mission

Create an AI-native Security Operations Center capable of continuous security monitoring, enterprise-wide threat detection, automated incident response orchestration, threat hunting, digital investigations, cross-platform security orchestration, and enterprise cyber resilience.

## Vision

Create an Autonomous SOC where every security event is observed, every alert is correlated, every incident is prioritised, every investigation is AI-assisted, every response is orchestrated, and every lesson improves future defence.

## Architecture layers

Security Telemetry → Collection → Normalization → Correlation → Detection → Threat Intelligence → Investigation → Response → Recovery → Executive Reporting

## Hard laws

- Never SOC is not capable of 24×7 operation
- Never alerts cannot be correlated
- Never AI assistance is absent
- Never incident response is manual only
- Never threat hunting is missing
- Never metrics are incomplete
- Never knowledge graph integration is absent
- Never invent sibling `soc_platform` BC
- Never duplicate IR lifecycle (SoR remains `security_incident`)

## Distinct from peers

| Peer | Boundary |
|---|---|
| `security_incident` | IR lifecycle SoR — SOC handoffs intents/events |
| P210-E `/siem*` | SIEM signal plane (planned) |
| P210-F `/soar*` | SOAR playbook depth (planned) |
| Observability | Telemetry plumbing — not SOC SoR |

## Definition of Done (P210-D)

SOC foundation ENTERPRISE_GRADE: 24×7, correlation, AI, automation, hunting, metrics, KG, `/soc*` API live.
