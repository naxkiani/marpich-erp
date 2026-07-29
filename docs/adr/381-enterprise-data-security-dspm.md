# ADR-381: Data Security — DSPM Posture Management (P211-F)

## Status

Accepted — P211-F Data Security Posture Management (DSPM) Platform

## Context

ADR-376–380 established SoR `data_security` through discovery and classification. P211-F delivers the **DSPM posture intelligence layer**: continuous visibility, posture scoring, exposure management, access risk analysis, AI risk intelligence, remediation automation, KG/twin bindings — without inventing sibling `dspm` / `dspm_platform` BCs.

**Hard laws:** SoR remains `data_security`. Surfaces under `/data-security/dspm*`. Never unknown data assets. Never unmeasurable security posture. Never invisible exposure risks. Never findings without ownership. Never remediation that is manual-only. Never unavailable continuous assessment. Builds on P211-D inventory and P211-E classification. Access risk via P208. Crypto via P209. Threat context via P210. Remediation approvals via Workflow. Inference via Enterprise AI.

## Decision

1. SoR remains `data_security`
2. Surfaces under `/api/v1/data-security/dspm*`
3. Law: `ENTERPRISE_DATA_SECURITY_DSPM.md`
4. Catalogs: `DATA_SECURITY_DSPM_*.v1.yaml`
5. Runtime: `ds_platform_dspm.py`; aggregates; ACL; foundation
6. Quality gates enforce asset visibility, measurable posture, visible exposure, owned findings, autonomous remediation path, continuous assessment
7. Roadmap: P211-F = DSPM; protection controls deferred to P211-I (`/protection*`)

## Consequences

- Data risk intelligence foundation connecting discovery → classification → DLP/privacy → access → protection → intelligence (later phases)
- Forbidden siblings: `dspm`, `dspm_platform`, `posture_management`

## References

ADR-376–380 · P208 · P209 · P210 · AI_PLATFORM_STANDARD.md · ENTERPRISE_WORKFLOW_ENGINE.md · ENTERPRISE_POLICY_ENGINE.md
