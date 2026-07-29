# ADR-364: Cyber Security — Enterprise SOC Platform (P210-D)

## Status

Accepted — P210-D Enterprise Security Operations Center (SOC)

## Context

ADR-361–363 established SoR `cyber_security` strategy, MVS, and DDD domain model. P210-D delivers the **operational SOC command center**: 24×7 monitoring, alert lifecycle, threat hunting, case/investigation orchestration, AI-assisted operations, automated response intents, dashboards/KPIs, KG/Twin surfaces — without inventing a sibling `soc_platform` BC and without absorbing IR SoR `security_incident`.

**Hard laws:** SoR remains `cyber_security`. Surfaces under `/cyber-security/soc*`. Never non-24×7 SOC. Never uncorrelated alerts. Never absent AI assistance. Never manual-only incident response. Never missing threat hunting. Never incomplete metrics. Never missing knowledge-graph integration. IR lifecycle remains `security_incident` (SOC publishes handoffs / orchestrates intents). Vendor agents via Integration Platform only.

## Decision

1. SoR remains `cyber_security`
2. Surfaces under `/api/v1/cyber-security/soc*`
3. Law: `ENTERPRISE_CYBER_SECURITY_SOC.md`
4. Catalogs: `CYBER_SOC_*.v1.yaml`
5. Runtime: `cs_platform_soc.py`; aggregates; ACL; foundation
6. Quality gates enforce 24×7, correlation, AI, automation, hunting, metrics, KG

## Consequences

- Complements P210-E SIEM / P210-F SOAR / P210-G XDR as logical follow-ons
- Peer IR via events/ACL only

## References

ADR-361–363 · ADR-158 · NIST CSF · SOC-as-a-Platform patterns
