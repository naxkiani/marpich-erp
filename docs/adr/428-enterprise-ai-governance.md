# ADR-428: Enterprise AI — Governance, Responsible AI & Risk (P214-H)

## Status

Accepted — P214-H Enterprise AI Governance, Responsible AI & AI Risk Management Platform

## Context

ADR-421–427 established SoR `ai` through Knowledge/RAG. P214-H catalogs the **MEOS Trusted AI Governance Fabric**: policy, risk, responsible AI, explainability, transparency, compliance, audit, trust scores, and governance digital twin — as logical capabilities inside `ai`, not sibling BCs.

**Principle:** Enterprise AI Governance SHALL provide the trust framework that enables MEOS to deploy powerful AI capabilities while maintaining security, transparency, compliance and human accountability.

## Decision

1. SoR remains `ai` (CAP-PLT-AI-001)
2. Surfaces under `/api/v1/ai/governance*`
3. Law: `ENTERPRISE_AI_GOVERNANCE.md`
4. Catalogs: `AI_GOVERNANCE_*.v1.yaml`
5. Runtime: `ai_platform_governance.py`; aggregates; ACL; foundation
6. Policy evaluation via Policy Engine; approvals via Workflow; trails via Audit; regulated evidence via Compliance
7. Aligns with P207–P211, P214-D/E/F/G via ACL
8. Modules never implement local AI governance / approval engines

## Consequences

- P214-I deepens AI Security / Adversarial Defense on the same SoR
- Forbidden siblings include `ai_governance`, `responsible_ai`, `ai_risk`, etc.

## References

ADR-421–427 · AI_PLATFORM_STANDARD.md · ENTERPRISE_POLICY_ENGINE.md · ENTERPRISE_AUDIT_PLATFORM.md · ENTERPRISE_COMPLIANCE_FRAMEWORK.md
