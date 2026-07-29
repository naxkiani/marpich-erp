# ADR-375: Cyber Security — Testing, Security Validation & Definition of Done (P210-O)

## Status

Accepted — P210-O Enterprise Testing, Security Validation, Quality Assurance & Definition of Done Platform

## Context

ADR-361–374 established SoR `cyber_security` through the deploy/DevSecOps fabric. P210-O delivers the **final continuous assurance layer**: security testing (SAST/DAST/IAST/SCA), penetration testing, red/blue/purple team validation, AI security testing, chaos/resilience, performance, compliance verification, test KG/twin bindings, and production readiness gates — without inventing sibling `qa_platform` / `security_testing` / `red_team` BCs, without replacing Compliance Framework evidence stores, and without executing live attacks against production without Workflow approval.

**Hard laws:** SoR remains `cyber_security`. Surfaces under `/cyber-security/qa*`. Never security testing is manual only. Never no adversarial validation. Never AI systems untested. Never compliance cannot be verified. Never production readiness undefined. Never security controls unmeasurable. Never test evidence unauditable. Approvals for adversarial exercises via Workflow; compliance evidence via Compliance Framework; AI tests via P210-M + Enterprise AI; pipeline hooks via P210-N; detections validated against SIEM/SOAR/XDR; audit via Audit Platform.

## Decision

1. SoR remains `cyber_security`
2. Surfaces under `/api/v1/cyber-security/qa*`
3. Law: `ENTERPRISE_CYBER_SECURITY_QA.md`
4. Catalogs: `CYBER_QA_*.v1.yaml`
5. Runtime: `cs_platform_qa.py`; aggregates; ACL; foundation
6. Quality gates enforce automated testing, adversarial validation, AI testing, compliance verification, production readiness, measurable controls, auditable evidence

## Consequences

- Completes P210 series A–O as continuous assurance fabric
- Forbidden sibling BCs: `qa_platform`, `security_testing`, `red_team`, `penetration_testing`
- Distinct from Compliance Framework (orchestration) and CI runners (execution plumbing)

## References

ADR-361–374 · ENTERPRISE_COMPLIANCE_FRAMEWORK.md · ENTERPRISE_AUDIT_PLATFORM.md · MITRE ATT&CK · NIST CSF · NIST AI RMF · CIS Controls
