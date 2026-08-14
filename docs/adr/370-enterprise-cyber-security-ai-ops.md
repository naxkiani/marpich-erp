# ADR-370: Cyber Security — AI Security Operations & Autonomous SOC (P210-J)

## Status

Accepted — P210-J AI Security Operations & Autonomous SOC Platform

## Context

ADR-361–369 established SoR `cyber_security` through SOC, SIEM, SOAR, XDR, Threat Intelligence, and ASM/CTEM. P210-J delivers the **cognitive intelligence layer**: multi-agent security operations, security copilots, reasoning engine, enterprise security knowledge memory, autonomous incident response with human oversight, AI detection engineering, predictive analytics, digital twins, and AI governance — without inventing sibling `ai_ops` / `autonomous_soc` BCs, and without embedding LLM SDKs in the module (Enterprise AI Platform only).

**Hard laws:** SoR remains `cyber_security`. Surfaces under `/cyber-security/ai-ops*`. Never unexplained AI decisions. Never absent human oversight. Never unsupported agent collaboration. Never disconnected knowledge graph. Never unaudited autonomous actions. Never incomplete AI governance. Never missing model lifecycle management. Inference via AI Platform ACL; approvals via Workflow; response orchestration via SOAR; agent isolation / prompt security via platform + P209.

## Decision

1. SoR remains `cyber_security`
2. Surfaces under `/api/v1/cyber-security/ai-ops*`
3. Law: `ENTERPRISE_CYBER_SECURITY_AI_OPS.md`
4. Catalogs: `CYBER_AI_OPS_*.v1.yaml`
5. Runtime: `cs_platform_ai_ops.py`; aggregates; ACL; foundation
6. Quality gates enforce explainability, HITL, agent collaboration, KG, audited autonomy, AI governance, model lifecycle

## Consequences

- Complements P210-D–I; does not replace SOC Ops or AI Platform
- Forbidden sibling BCs: `ai_ops`, `autonomous_soc`, `security_copilot`

## References

ADR-361–369 · AI_PLATFORM_STANDARD.md · NIST AI RMF · EU AI Act · MITRE ATT&CK · MITRE D3FEND
