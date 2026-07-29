# ADR-385: Data Security — Encryption, Tokenization & Protection (P211-J)

## Status

Accepted — P211-J Enterprise Data Encryption, Tokenization & Protection Platform

## Context

ADR-376–384 established SoR `data_security` through discovery, classification, DSPM, DLP, access, and privacy. P211-J delivers the **data-centric protection layer**: encryption (rest/transit/use), tokenization, masking, anonymization, protection policies/decisions, confidential computing bindings, KG/twin — without inventing sibling `data_protection_platform` BCs and without absorbing P209 KMS/key material.

**Hard laws:** SoR remains `data_security`. Surfaces under `/data-security/protection*`. Never unprotected sensitive data. Never undefined encryption policies. Never missing token lifecycle. Never unavailable key integration (via P209). Never non-auditable protection decisions. Never incomplete privacy controls. Keys/crypto materials remain in `secrets` (P209) — peer key references only. AuthZ via P208. Inference via Enterprise AI. Approvals via Workflow. Policies via Policy Engine.

## Decision

1. SoR remains `data_security`
2. Surfaces under `/api/v1/data-security/protection*`
3. Law: `ENTERPRISE_DATA_SECURITY_PROTECTION.md`
4. Catalogs: `DATA_SECURITY_PROTECTION_*.v1.yaml`
5. Runtime: `ds_platform_protection.py`; aggregates; ACL; foundation
6. Quality gates enforce protected sensitive data, defined policies, token lifecycle, P209 key integration, auditable decisions, complete privacy controls
7. Roadmap: P211-J = Protection; Data Intelligence deferred (`/intelligence*`) for a dedicated follow-up

## Consequences

- Cryptographic data protection layer connecting P209 ↔ Classification ↔ DSPM ↔ DLP ↔ Access ↔ Cyber Ops
- Forbidden siblings: `data_protection_platform`, `tokenization_platform`, `encryption_platform`

## References

ADR-376–384 · P209 `secrets` · P208 · P210 · AI_PLATFORM_STANDARD.md · ENTERPRISE_WORKFLOW_ENGINE.md · ENTERPRISE_POLICY_ENGINE.md
