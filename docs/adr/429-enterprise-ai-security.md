# ADR-429: Enterprise AI — Security, Adversarial Defense & Protection (P214-I)

## Status

Accepted — P214-I Enterprise AI Security, Adversarial Defense & AI Protection Platform

## Context

ADR-421–428 established SoR `ai` through Governance. P214-I catalogs the **MEOS AI Security Fabric**: asset, model, LLM, prompt, agent protection, adversarial defense, threat intelligence, runtime protection, AI-SOC, security knowledge graph, and security digital twin — as logical capabilities inside `ai`, not sibling BCs.

**Principle:** Enterprise AI Security SHALL protect the intelligence layer of MEOS by securing models, data, agents, prompts, knowledge and autonomous actions against internal and external threats.

## Decision

1. SoR remains `ai` (CAP-PLT-AI-001)
2. Surfaces under `/api/v1/ai/aisec*` (distinct from nested `*/security` catalog routes)
3. Law: `ENTERPRISE_AI_SECURITY.md`
4. Catalogs: `AI_SECURITY_*.v1.yaml`
5. Runtime: `ai_platform_security.py`; aggregates; ACL; foundation
6. Aligns with P207–P211, P210 SIEM/SOAR, P214-E/F/G/H via ACL
7. Model signing via P209; cyber SOC via P210 — no module-local SIEM
8. Modules never implement local AI security stacks

## Consequences

- P214-J deepens AI Operations / AIOps on the same SoR
- Forbidden siblings include `ai_security`, `adversarial_defense`, `llm_security`, etc.

## References

ADR-421–428 · AI_PLATFORM_STANDARD.md · SECURITY_STANDARD.md · P210
