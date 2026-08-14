# ADR-380: Data Security — Classification & Labeling (P211-E)

## Status

Accepted — P211-E Enterprise Data Classification & Labeling Platform

## Context

ADR-376–379 established SoR `data_security` through discovery/inventory. P211-E delivers the **classification & labeling intelligence layer**: taxonomy, sensitive detection, AI classification (via Enterprise AI), label management, policy engine (via Policy Engine), continuous classification, KG/twin bindings — without inventing sibling `data_classification` / `label_management` BCs.

**Hard laws:** SoR remains `data_security`. Surfaces under `/data-security/classification*`. Never unclassifiable data. Never unavailable sensitive detection. Never unmanaged labels. Never unexplained AI decisions. Never missing classification policies. Never undefined classification lifecycle. Approvals via Workflow. Inference via Enterprise AI. Policies via Policy Engine. Builds on P211-D inventory.

## Decision

1. SoR remains `data_security`
2. Surfaces under `/api/v1/data-security/classification*`
3. Law: `ENTERPRISE_DATA_SECURITY_CLASSIFICATION.md`
4. Catalogs: `DATA_SECURITY_CLASSIFICATION_*.v1.yaml`
5. Runtime: `ds_platform_classification.py`; aggregates; ACL; foundation
6. Quality gates enforce classifiability, sensitive detection, managed labels, AI explainability, policies, lifecycle

## Consequences

- Decision foundation for protection, DLP, access, privacy, compliance, AI data security (later P211 phases)
- Forbidden siblings: `data_classification`, `label_management`, `sensitive_data_detection`

## References

ADR-376–379 · ENTERPRISE_POLICY_ENGINE.md · AI_PLATFORM_STANDARD.md · ENTERPRISE_WORKFLOW_ENGINE.md
