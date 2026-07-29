# ADR-391: Data Security — Testing, Governance, Compliance & DoD (P211-P)

## Status

Accepted — P211-P Enterprise Testing, Governance, Compliance Validation & Definition of Done Platform

## Context

ADR-376–390 established the full SoR `data_security` capability and operational surfaces through deploy. P211-P delivers the **continuous assurance & Definition of Done layer**: quality engineering, security/privacy/AI validation, compliance automation, governance ownership, quality gates, evidence/risk tracking, production certification — without inventing sibling `data_security_qa` BCs and without replacing platform Compliance, Audit, or Cyber Security.

**Hard laws:** SoR remains `data_security`. Surfaces under `/data-security/qa*`. Never manual-only testing. Never unavailable compliance evidence. Never missing security validation. Never unclear governance ownership. Never untrackable risks. Never undefined production readiness. Evidence via Audit Platform events. Formal compliance orchestration via Compliance BC (ACL). Consent ledger remains `consent`. Builds on P211-A–O and P207–P210.

## Decision

1. SoR remains `data_security`
2. Surfaces under `/api/v1/data-security/qa*`
3. Law: `ENTERPRISE_DATA_SECURITY_QA.md`
4. Catalogs: `DATA_SECURITY_QA_*.v1.yaml`
5. Runtime: `ds_platform_qa.py`; aggregates; ACL; foundation
6. Quality gates enforce automated testing, evidence, security validation, ownership, risk tracking, production readiness
7. Roadmap: P211-P = QA/Governance/DoD (fulfills deferred `P211-O-QA`); series P211 **complete** (graph deepening `/graph*` remains optional deferred)

## Consequences

- Finalizes the P211 Data Security & Privacy Intelligence Platform lifecycle with continuous assurance
- Forbidden siblings: `data_security_qa`, `ds_assurance_platform`, `data_security_compliance_validation`

## References

ADR-376–390 · ENTERPRISE_COMPLIANCE_FRAMEWORK.md · ENTERPRISE_AUDIT_PLATFORM.md · ENGINEERING_QUALITY_STANDARD.md · NIST AI RMF · ISO 27001 / 27701 · GDPR
