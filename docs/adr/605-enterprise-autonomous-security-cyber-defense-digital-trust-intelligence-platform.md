# ADR 605 — Enterprise Autonomous Security, Cyber Defense & Digital Trust Intelligence Platform (P246)

## Status
Accepted

## Context
P244 established EAFIEEP (economic evolution). P246 opens the Enterprise Autonomous Security, Cyber Defense & Digital Trust Intelligence Platform (EASC-DTIP) for integrated security–trust posture intelligence, Zero Trust assist, threat/risk quantification and gated response orchestration under MEOS 11.0. P226 already owns SoR `cyber_defense`; P230 owns `privacy_trust`; P210 owns operational SOC/XDR/SOAR — EASC-DTIP must not fork those SoRs and must never issue ungated containment or silent consent overrides.

## Decision
1. SoR `security_trust_intelligence` (not `cyber_defense` / `privacy_trust`); fabric `meos_enterprise_autonomous_security_cyber_defense_digital_trust_intelligence_platform_framework`; API `/api/v1/security-trust-intelligence*`; capability `CAP-PLT-EASCDTIP-001`.
2. Ten logical BCs inside one SoR: Cyber Security Management, Threat Intelligence, Identity Security, Vulnerability Management, Incident Management, Security Operations, Digital Trust, Risk Management, Cyber Simulation, Security Governance.
3. Federate with P226, P230, P210, Identity, AuthZ, Secrets, P225, P221, P240, P241, P228, P227, P229, P224 via ACL/events — never replace them; never dual-write peer tables; never fork `/api/v1/cyber-defense*` or `/api/v1/privacy-trust*`.
4. Inference only via P214-Z; respond via Workflow + P210/Identity adapters; trust/consent via P230; simulation ≠ respond.
5. Never ungated SOAR/EDR/firewall SDKs in domain; never local consent vaults; never module-local LLM; never opaque unexplainable security actions; never silent consent override.
6. Roadmap: P246 foundation → P246-A…D (security domain → AI/KG/twin → autonomous assist → civilization-scale gated cyber-trust intel).

## Consequences
Positive: governed integrated security–trust control-tower intelligence federated with cyber immune, privacy/trust and SOC peers.  
Negative: SOC cases, immune models and consent ledgers remain peer-owned — EASC-DTIP stores posture models, trust-scored risks and peer refs only.

## Links
Law: `ENTERPRISE_AUTONOMOUS_SECURITY_CYBER_DEFENSE_DIGITAL_TRUST_INTELLIGENCE_PLATFORM.md` · Prior: ADR 604 · Next: P246-A · Peer: ADR 606 (P247 EASIEP)
