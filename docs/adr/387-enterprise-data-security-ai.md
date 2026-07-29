# ADR-387: Data Security — AI Intelligence & Autonomous Protection (P211-L)

## Status

Accepted — P211-L Data Security AI Intelligence & Autonomous Data Protection Platform

## Context

ADR-376–386 established SoR `data_security` through discovery, classification, DSPM, DLP, access, privacy, protection, and intelligence graph. P211-L delivers the **autonomous AI security intelligence layer**: risk prediction, behavioral analytics, specialized security agents, ML models, policy optimization, autonomous actions (with human oversight), responsible AI governance, KG/twin bindings — without inventing sibling `ai_data_security` BCs and without module-local LLM/ML runtimes.

**Hard laws:** SoR remains `data_security`. Surfaces under `/data-security/ai-data*`. Never unexplained AI decisions. Never uncontrolled autonomous actions. Never unpredictable data risks. Never missing learning loop. Never absent AI security governance. Never impossible human oversight. Inference via Enterprise AI. Approvals/overrides via Workflow. Policies via Policy Engine. Crypto via P209. AuthZ via P208.

## Decision

1. SoR remains `data_security`
2. Surfaces under `/api/v1/data-security/ai-data*`
3. Law: `ENTERPRISE_DATA_SECURITY_AI.md`
4. Catalogs: `DATA_SECURITY_AI_*.v1.yaml`
5. Runtime: `ds_platform_ai.py`; aggregates; ACL; foundation
6. Quality gates enforce explainability, controlled autonomy, risk prediction, learning loop, AI governance, human oversight
7. Roadmap: P211-L = AI Autonomous Security; Knowledge Graph/Twin deepening deferred (`/graph*`); fulfills deferred K-AI

## Consequences

- Autonomous intelligence layer connecting Identity → AuthZ → Crypto → Cyber → Data Security fabric
- Forbidden siblings: `ai_data_security`, `autonomous_data_protection`, `data_security_ai`

## References

ADR-376–386 · AI_PLATFORM_STANDARD.md · ENTERPRISE_WORKFLOW_ENGINE.md · ENTERPRISE_POLICY_ENGINE.md · NIST AI RMF · ISO/IEC 42001
