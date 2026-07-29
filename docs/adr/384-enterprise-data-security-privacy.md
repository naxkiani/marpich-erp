# ADR-384: Data Security — Privacy Intelligence (P211-I)

## Status

Accepted — P211-I Data Privacy Intelligence Platform

## Context

ADR-376–383 established SoR `data_security` through discovery, classification, DSPM, DLP, and access governance. P211-I delivers the **privacy intelligence layer**: personal data intelligence, consent orchestration (via `consent` SoR), DSAR automation signals, privacy risk/DPIA, regulatory mapping, AI privacy governance, KG/twin bindings — without inventing sibling `privacy_intelligence` / `data_privacy_platform` BCs and without absorbing the `consent` ledger.

**Hard laws:** SoR remains `data_security`. Surfaces under `/data-security/privacy*`. Never undiscoverable personal data. Never untracked consent. Never unmeasurable privacy risk. Never invisible processing. Never unmapped regulatory obligations. Never unmanaged AI privacy risks. Consent ledger / DSAR / DPIA records remain owned by `consent` (peer IDs + ACL only). Crypto via P209. AuthZ via P208. Identity via P207. Inference via Enterprise AI. Approvals via Workflow. Policies via Policy Engine.

## Decision

1. SoR remains `data_security`
2. Surfaces under `/api/v1/data-security/privacy*`
3. Law: `ENTERPRISE_DATA_SECURITY_PRIVACY.md`
4. Catalogs: `DATA_SECURITY_PRIVACY_*.v1.yaml`
5. Runtime: `ds_platform_privacy.py`; aggregates; ACL; foundation
6. Quality gates enforce personal-data discovery, consent tracking, measurable risk, visible processing, mapped obligations, managed AI privacy
7. `consent` BC remains SoR for consent ledger / DSAR / DPIA evidence

## Consequences

- Privacy intelligence foundation connecting discovery → classification → DSPM → DLP → access → protection/graph (later)
- Forbidden siblings: `privacy_intelligence`, `data_privacy_platform`, `personal_data_platform`

## References

ADR-376–383 · `consent` context · P207–P210 · AI_PLATFORM_STANDARD.md · ENTERPRISE_COMPLIANCE_FRAMEWORK.md · ENTERPRISE_WORKFLOW_ENGINE.md
