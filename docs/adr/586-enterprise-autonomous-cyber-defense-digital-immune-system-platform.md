# ADR 586 — Enterprise Autonomous Cyber Defense & Digital Immune System Platform (P226)

## Status
Accepted

## Context
P225 established EAOSHP (autonomous operations & self-healing). P226 opens the Enterprise Autonomous Cyber Defense & Digital Immune System Platform (EACDISP) for continuous cyber protection, threat prediction, autonomous defense, digital immunity and adaptive security evolution under MEOS 11.0. P210 remains the authoritative Cyber Security SoR (SOC/XDR/SOAR and related fabrics); EACDISP federates immune/autonomous-defense intelligence rather than replacing P210.

## Decision
1. SoR `cyber_defense`; fabric `meos_enterprise_autonomous_cyber_defense_digital_immune_system_platform_framework`; API `/api/v1/cyber-defense*`; capability `CAP-PLT-EACDISP-001`.
2. Ten logical BCs inside one SoR: Cyber Intelligence, Threat Management, Security Operations, Incident Response, Vulnerability Management, Identity Security, Security Analytics, Cyber Resilience, Defense Automation, Governance.
3. Federate with P210, Identity/Zero Trust, Secrets, P225, P224, P221 via ACL/events — never replace them.
4. Inference only via P214-Z; containment via Policy automation levels + Workflow; external controls via Integration Platform; audit via Audit.
5. Never module-local LLM; never secrets in domain tables; never ungated destructive/cross-tenant containment; never vendor security SDKs in domain/application.
6. Roadmap: P226 foundation → P226-A…D (threat core → AI/twin → autonomous defense → immune evolution assist).

## Consequences
Positive: graded digital immune system and autonomous defense orchestration under Zero Trust.  
Negative: SOC/incident ownership stays with P210 — EACDISP stores threats, immune profiles, defense actions and posture projections with peer incident refs only.

## Links
Law: `ENTERPRISE_AUTONOMOUS_CYBER_DEFENSE_DIGITAL_IMMUNE_SYSTEM_PLATFORM.md` · Prior: ADR 585 · Next: P226-A · Peer: ADR 587 (P227 EDTISP)
