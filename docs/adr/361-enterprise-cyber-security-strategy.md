# ADR-361: Cyber Security — Strategy Foundation (P210-A)

## Status

Accepted — P210-A Enterprise Cyber Security & Threat Defense Platform strategy foundation

## Context

Volume 05 requires a centralized **cyber security control plane** spanning SOC, SIEM, SOAR, XDR/EDR/NDR, threat intelligence, hunting, ASM/CTEM, forensics, and AI-native security operations. `security_incident` (ADR-158) owns IR lifecycle and already consumes `security.attack.detected`, but cyber detection/correlation/SOC strategy has no authoritative SoR. Observability owns telemetry plumbing, not threat defense. P209 owns crypto trust; PAM/II own privileged and identity analytics.

**Hard laws:** SoR is `cyber_security`. Surfaces under `/cyber-security/strategy*`. Zero Trust required. Enterprise-scale SOC required. AI security required. Threat intelligence must not be isolated. Incident response must not be manual-only. Telemetry must be complete. Controls must be measurable. Architecture must be cloud-native. Never invent sibling SOC/SIEM/SOAR/XDR BCs. Vendor agents via Integration Platform only. IR lifecycle remains in `security_incident`.

## Decision

1. New platform SoR `backend/contexts/cyber_security/` (schema `cyber_security`)
2. Series roadmap: `P210_MASTER_SERIES_ROADMAP.v1.yaml` (A done; B–O planned)
3. Surfaces under `/api/v1/cyber-security/strategy*`
4. Law: `ENTERPRISE_CYBER_SECURITY_STRATEGY.md`
5. Catalogs: `CYBER_STRATEGY_*.v1.yaml`
6. Runtime: `cs_platform_strategy.py`; aggregates; ACL; foundation validator
7. Publishes strategy/capability contracts; detection events deepen in later phases (including `security.attack.detected`)
8. Forbidden siblings: `cyber_defense`, `soc_platform`, `siem_platform`, `soar_platform`, `xdr`, `edr`, `ndr`, `security_ops`

## Consequences

- P210-B–O deepen mission, domain, SOC, SIEM, SOAR, XDR, intel, ASM, AI-ops, KG/Twin, ops, gov, deploy, QA on the same SoR
- Complements — does not replace — `security_incident`, Observability, Secrets, AuthZ, PAM, II

## References

ADR-021 · ADR-158 · ADR-179 · ADR-345 · NIST CSF · Zero Trust Architecture · MITRE ATT&CK
