# ADR-373: Cyber Security — AI Security Governance & Compliance (P210-M)

## Status

Accepted — P210-M AI Security Governance & Enterprise Cyber Compliance Platform

## Context

ADR-361–372 established SoR `cyber_security` through the ops fabric. P210-M delivers the **AI governance & trust layer**: AI asset/model registry, responsible AI, AI security controls, policy enforcement (via Policy Engine), AI risk management, agent governance, continuous monitoring, audit/compliance automation (NIST AI RMF, ISO 42001, EU AI Act, …), KG/twin bindings — without inventing sibling `ai_governance` / `ai_compliance` BCs, without embedding LLMs, and without local approval engines.

**Hard laws:** SoR remains `cyber_security`. Surfaces under `/cyber-security/gov*`. Never uninventoried AI models. Never unauditable AI decisions. Never unmeasurable AI risks. Never ungoverned AI agents. Never unenforceable policies. Never non-generatable compliance evidence. Never unavailable human oversight. Inference/model lifecycle via Enterprise AI Platform; policies via Policy Engine; HITL via Workflow; compliance orchestration via Compliance Framework; crypto via P209.

## Decision

1. SoR remains `cyber_security`
2. Surfaces under `/api/v1/cyber-security/gov*`
3. Law: `ENTERPRISE_CYBER_SECURITY_AI_GOVERNANCE.md`
4. Catalogs: `CYBER_GOV_*.v1.yaml`
5. Runtime: `cs_platform_gov.py`; aggregates; ACL; foundation
6. Quality gates enforce inventory, auditability, risk measurement, agent governance, policy enforcement, compliance evidence, human oversight

## Consequences

- Complements P210-J AI Ops (operations) with governance/trust controls
- Forbidden sibling BCs: `ai_governance`, `ai_compliance`, `responsible_ai`

## References

ADR-361–372 · AI_PLATFORM_STANDARD.md · ENTERPRISE_POLICY_ENGINE.md · ENTERPRISE_COMPLIANCE_FRAMEWORK.md · NIST AI RMF · ISO/IEC 42001 · EU AI Act
