# ADR-358: Secrets — AI Security, Cryptographic Governance & Compliance (P209-M)

## Status

Accepted — P209-M AI Security, Cryptographic Governance & Compliance Platform

## Context

ADR-345–357 delivered cryptographic trust capabilities and the CQRS/ops fabric. P209-M adds the **governance intelligence layer**: AI security governance, cryptographic policy stewardship, continuous compliance automation, risk intelligence, and responsible AI controls — still under SoR `secrets`, never a sibling `governance_platform` / `crypto_compliance_platform` BC.

**Hard laws:** SoR remains `secrets`. Surfaces under `/secrets/gov*`. Never unexplainable AI security decisions. Never unmanaged cryptographic policies. Never manual-only compliance evidence. Never unmeasurable risks. Never undefined governance ownership. Never incomplete audit trails. Never non-automatable remediation.

## Decision

1. SoR remains `secrets`
2. Surfaces under `/api/v1/secrets/gov*`
3. Law: `ENTERPRISE_SECRETS_GOVERNANCE.md`
4. Catalogs: `SECRETS_GOV_*.v1.yaml`
5. Runtime: `secrets_platform_gov.py`; aggregates; ACL; foundation
6. Policy via Policy Engine (`IPolicyEvaluator`); Compliance via Compliance Platform; AI via AI Platform; Workflow for human oversight; Audit Platform for trails
7. Extends P209 series beyond ops closeout with governance intelligence

## Consequences

- Distinct from `/ops*` (software fabric) vs `/gov*` (governance / compliance / AI security)
- Does not replace GRC / Compliance / Policy Engine SoRs — orchestrates via ACL + events
- Logical microservices are deployable units under `secrets`, not sibling BCs

## References

ADR-345–357 · ENTERPRISE_COMPLIANCE_FRAMEWORK · ENTERPRISE_POLICY_ENGINE · AI_PLATFORM_STANDARD · NIST AI RMF
