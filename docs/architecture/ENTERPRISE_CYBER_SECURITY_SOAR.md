# Enterprise Cyber Security — SOAR Platform — P210-F

**Prompt:** P210-F · **ADR:** [365](../adr/365-enterprise-cyber-security-soar.md)  
**Builds on:** P210-A–D (ADR-361–364); P210-E SIEM planned  
**SoR:** `cyber_security` · **Forbidden:** sibling `soar_platform` BC  
**API:** `/api/v1/cyber-security/soar*`

---

## Mission

Create an enterprise SOAR platform capable of orchestrating security operations, automating repetitive tasks, coordinating multi-system incident response, reducing MTTR, standardising response procedures, enabling AI-assisted decision making, and supporting autonomous cyber defence under Zero Trust.

## Vision

Create an Autonomous SOAR Platform where every alert launches intelligent workflows, every incident follows approved playbooks, every response is coordinated, every action is fully auditable, every recommendation is AI-assisted and explainable, and every automation continuously improves.

## Architecture layers

Security Alerts → Incident Intake → Playbook Engine → Decision Engine → Orchestration → Automation → Execution → Verification → Evidence Collection → Reporting

## Hard laws

- Never playbooks cannot be versioned
- Never automation is not auditable
- Never human approval is unavailable
- Never AI recommendations are not explainable
- Never rollback capability is absent
- Never connectors are tightly coupled
- Never incident evidence cannot be preserved
- Never invent sibling `soar_platform` BC
- Never duplicate IR lifecycle (SoR remains `security_incident`)
- Never embed vendor connector SDKs (Integration Platform only)
- Never implement local approval engines (Workflow Engine only)

## Distinct from peers

| Peer | Boundary |
|---|---|
| P210-D `/soc*` | Operational command center |
| P210-E `/siem*` | Signal/analytics plane (planned) |
| Workflow | Human approval gates |
| Integration | Vendor connectors |
| `security_incident` | IR lifecycle SoR |

## Definition of Done (P210-F)

SOAR foundation ENTERPRISE_GRADE: versioned playbooks, auditable automation, HITL, explainable AI, rollback, Integration-only connectors, evidence preservation, `/soar*` API live.
