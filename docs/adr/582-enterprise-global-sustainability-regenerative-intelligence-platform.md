# ADR 582 — Enterprise Global Sustainability & Regenerative Intelligence Platform (P222)

## Status
Accepted

## Context
P221 established EGRCMP (global resilience & crisis). P222 opens the Enterprise Global Sustainability & Regenerative Intelligence Platform (EGSRIP) for sustainability intelligence, regenerative transformation, ecological optimization, ESG governance and long-term planetary balance under MEOS 11.0.

## Decision
1. SoR `sustainability`; fabric `meos_enterprise_global_sustainability_regenerative_intelligence_platform_framework`; API `/api/v1/sustainability*`; capability `CAP-PLT-EGSRIP-001`.
2. Ten logical BCs inside one SoR: Sustainability Management, ESG, Carbon, Resources, Circular, Environmental Intelligence, Regenerative Planning, Reporting, Impact, Governance.
3. Federate with P220 EPIP, P219-N Civilization Sustainability, P221 EGRCMP via ACL/events — never replace them.
4. Inference only via P214-Z; transformations via Workflow; policy via Policy Engine; violations via Compliance Platform; audit via Audit.
5. Never module-local LLM; never ungated regenerative/physical actuation; never local ESG violation stores.
6. Roadmap: P222 foundation → P222-A…D (ESG core → AI/carbon/twin → regenerative/circular → civilization-scale assist).

## Consequences
Positive: dedicated sustainability/regenerative intelligence SoR with clear federation to EPIP and Civilization.  
Negative: climate observation and crisis authority remain with P220/P221 — EGSRIP holds refs and impact models only.

## Links
Law: `ENTERPRISE_GLOBAL_SUSTAINABILITY_REGENERATIVE_INTELLIGENCE_PLATFORM.md` · Prior: ADR 581 · Next: P222-A · Peer: ADR 583 (P223 EGIKEP)
