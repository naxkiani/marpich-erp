# ADR 623 — MEOS Enterprise AI Agent Orchestration & Autonomous Intelligence Platform (P266)

## Status
Accepted

## Context
P265 established MEDTIP over P227 digital twin. P266 productizes AI Agent Orchestration as the MEOS Autonomous Intelligence Operating Layer. AI Platform / P214-F already own `/api/v1/ai/agents*` and CAP-PLT-AI-001; P214-Z is the sole inference gateway. MEAAOI must federate those SoRs — never fork `/api/v1/ai*`, never embed module-local LLM clients, and never ungated critical autonomous actions. P267 is planned for Autonomous Operations & Self-Healing productization over P225.

## Decision
1. SoR `ai_agent_orchestration`; fabric `meos_enterprise_ai_agent_orchestration_autonomous_intelligence_platform_framework`; API `/api/v1/ai-agent-orchestration*`; capability `CAP-PLT-MEAAOI-001`; acronym **MEAAOI**.
2. Logical BCs inside one SoR: AI Agent Management, AI Orchestration, AI Governance operating, Collaboration, Learning & Evolution, Agent Marketplace.
3. Federate with AI Platform / P214-F / P214-Z, AI Governance, P257–P265 peers, Workflow, Policy, Feature Flags, Audit — never replace them; never dual-write AI agent/model catalogs.
4. Inference only via P214-Z; plan/recommendation ≠ execute; critical actions require human approval + Workflow; explainability and responsible AI mandatory.
5. Roadmap: P266 foundation → P266-A…D; unblocks P267.

## Consequences
Positive: governed multi-agent OS (plans, collaboration, marketplace, safety campaigns) over canonical AI Platform.  
Negative: agent/model/inference truth remains AI Platform-owned — MEAAOI stores orchestration plans, sessions, governance campaigns and peer refs only.

## Links
Law: `ENTERPRISE_MEOS_AI_AGENT_ORCHESTRATION_AUTONOMOUS_INTELLIGENCE_PLATFORM.md` · Prior: ADR 622 · Next: P266-A · Peer: ADR 624 (P267 MEAOSH) · Canonical: `ENTERPRISE_AI_AGENTS.md` / P214-Z
