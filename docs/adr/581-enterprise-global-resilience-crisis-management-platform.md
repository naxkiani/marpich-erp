# ADR 581 — Enterprise Global Resilience & Crisis Management Platform (P221)

## Status
Accepted

## Context
P220 established EPIP (planetary intelligence). P221 opens the Enterprise Global Resilience & Crisis Management Platform (EGRCMP) for prediction, prevention, preparedness, response, recovery and continuous resilience across enterprise, cyber, environmental, economic, social, geopolitical and operational crises under MEOS 11.0.

## Decision
1. SoR `resilience`; fabric `meos_enterprise_global_resilience_crisis_management_platform_framework`; API `/api/v1/resilience*`; capability `CAP-PLT-EGRCMP-001`.
2. Ten logical BCs inside one SoR: Crisis, Incident, Emergency, Recovery, Continuity, Resources, Risk Intelligence, Resilience, Policy Governance, Decision Support.
3. Federate with P210 Cyber, P220 EPIP, P219-Z Unified Control via ACL/events — never replace them.
4. Inference only via P214-Z; activations via Workflow; policy via Policy Engine; audit via Audit; alerts via Notifications.
5. Never module-local LLM; never ungated crisis autonomy; never direct physical actuation from EGRCMP.
6. Roadmap: P221 foundation → P221-A…D (domain → AI/twin → orchestration → learning).

## Consequences
Positive: single governed crisis/resilience fabric across MEOS.  
Negative: peer SoRs remain authoritative for cyber/planetary/domain incidents — EGRCMP holds refs only.

## Links
Law: `ENTERPRISE_GLOBAL_RESILIENCE_CRISIS_MANAGEMENT_PLATFORM.md` · Prior: ADR 580 · Next: P221-A · Peer: ADR 582 (P222 EGSRIP)
