# ADR-382: Data Security — Data Loss Prevention / DLP (P211-G)

## Status

Accepted — P211-G Enterprise Data Loss Prevention (DLP) Platform

## Context

ADR-376–381 established SoR `data_security` through discovery, classification, and DSPM. P211-G delivers the **DLP enforcement layer**: channel protection (endpoint/network/cloud/email/AI), exfiltration detection, insider risk, policy engine, real-time enforcement, incident lifecycle, KG/twin bindings — without inventing sibling `dlp` / `data_loss_prevention` BCs.

**Hard laws:** SoR remains `data_security`. Surfaces under `/data-security/dlp*`. Never unidentified sensitive data. Never unmonitored data movement. Never unenforceable policies. Never unmanaged AI leakage. Never invisible insider risk. Never uninvestigable violations. Never unavailable automated response. Builds on P211-D/E/F. Enforcement integrates P208/P209/P210. Approvals via Workflow. Inference via Enterprise AI. Policies via Policy Engine.

## Decision

1. SoR remains `data_security`
2. Surfaces under `/api/v1/data-security/dlp*`
3. Law: `ENTERPRISE_DATA_SECURITY_DLP.md`
4. Catalogs: `DATA_SECURITY_DLP_*.v1.yaml`
5. Runtime: `ds_platform_dlp.py`; aggregates; ACL; foundation
6. Quality gates enforce identification, monitoring, enforcement, AI leakage management, insider visibility, investigation, automated response
7. Roadmap: P211-G = DLP; Privacy Intelligence deferred to P211-I (`/privacy*`)

## Consequences

- Enforcement layer between classification/DSPM and cyber/authz/crypto controls
- Forbidden siblings: `dlp`, `data_loss_prevention`, `exfiltration_prevention`

## References

ADR-376–381 · P208 · P209 · P210 · AI_PLATFORM_STANDARD.md · ENTERPRISE_WORKFLOW_ENGINE.md · ENTERPRISE_POLICY_ENGINE.md
