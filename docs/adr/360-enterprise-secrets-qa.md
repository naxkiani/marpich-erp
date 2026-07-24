# ADR-360: Secrets — Testing, Governance, Security Validation & DoD (P209-O)

## Status

Accepted — P209-O Enterprise Testing, Governance, Security Validation & Definition of Done Platform

## Context

ADR-345–359 delivered cryptographic trust capabilities through deploy/ops/gov. P209-O is the **assurance and Definition of Done layer**: enterprise testing, cryptographic security validation, governance operating model, compliance evidence, and production acceptance gates — still under SoR `secrets`, never a sibling `qa_platform` / `crypto_assurance_platform` BC.

**Hard laws:** SoR remains `secrets`. Surfaces under `/secrets/qa*`. Never incomplete security testing. Never unavailable compliance evidence. Never unvalidated cryptographic controls. Never undefined production readiness. Never missing governance ownership. Never incomplete audit trails. Never security failures that cannot block deployment.

## Decision

1. SoR remains `secrets`
2. Surfaces under `/api/v1/secrets/qa*`
3. Law: `ENTERPRISE_SECRETS_QA.md`
4. Catalogs: `SECRETS_QA_*.v1.yaml`
5. Runtime: `secrets_platform_qa.py`; aggregates; ACL; foundation
6. Compliance via Compliance Platform; Policy via Policy Engine; Workflow for release approval; Audit for trails; AI for risk prediction; Deploy gates via P209-N
7. Completes continuous assurance for the P209 cryptographic trust fabric

## Consequences

- Distinct from `/gov*` (governance intelligence) vs `/qa*` (testing / validation / DoD gates)
- Distinct from `/deploy*` (runtime ops) vs `/qa*` (assurance that blocks bad releases)
- Security failures **must** be able to reject deployment (quality gate)

## References

ADR-345–359 · ENTERPRISE_COMPLIANCE_FRAMEWORK · ENGINEERING_QUALITY_STANDARD · ARCHITECTURE_VALIDATION · P209-N deploy gates
