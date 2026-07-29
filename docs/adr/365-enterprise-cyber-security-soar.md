# ADR-365: Cyber Security — Enterprise SOAR Platform (P210-F)

## Status

Accepted — P210-F Enterprise Security Orchestration, Automation & Response (SOAR)

## Context

ADR-361–364 established SoR `cyber_security` through SOC. P210-F delivers the **SOAR automation & orchestration layer**: versioned playbooks, automation engine, incident response workflows, human-in-the-loop approvals, AI-assisted orchestration, connectors, KG/Twin surfaces — without inventing a sibling `soar_platform` BC, without embedding vendor connector SDKs, and without replacing Workflow (approvals) or `security_incident` (IR lifecycle).

**Hard laws:** SoR remains `cyber_security`. Surfaces under `/cyber-security/soar*`. Never unversioned playbooks. Never unauditable automation. Never unavailable human approval. Never unexplained AI recommendations. Never absent rollback. Never tightly coupled connectors (Integration Platform only). Never unpreserved incident evidence. Approvals via Workflow Engine. Destructive execution gated by AuthZ + Workflow.

## Decision

1. SoR remains `cyber_security`
2. Surfaces under `/api/v1/cyber-security/soar*`
3. Law: `ENTERPRISE_CYBER_SECURITY_SOAR.md`
4. Catalogs: `CYBER_SOAR_*.v1.yaml`
5. Runtime: `cs_platform_soar.py`; aggregates; ACL; foundation
6. Quality gates enforce versioning, audit, HITL, explainable AI, rollback, loose connectors, evidence

## Consequences

- Complements P210-D SOC and planned P210-E SIEM / P210-G XDR
- Connectors are Integration Platform refs only

## References

ADR-361–364 · ADR-158 · ENTERPRISE_WORKFLOW_ENGINE.md · INTEGRATION_PLATFORM.md · NIST 800-61
