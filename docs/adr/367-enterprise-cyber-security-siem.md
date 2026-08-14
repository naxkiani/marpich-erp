# ADR-367: Cyber Security — Enterprise SIEM Platform (P210-E)

## Status

Accepted — P210-E Enterprise Security Information & Event Management (SIEM)

## Context

ADR-361–366 established SoR `cyber_security` through SOC, SOAR, and XDR. P210-E delivers the **enterprise security telemetry, analytics & detection engine**: collection, ingestion, normalization, enrichment, correlation, detection, risk analytics, alert lifecycle, storage tiers, KG/Twin surfaces — without inventing a sibling `siem_platform` BC, without incomplete normalization, and without replacing Observability (platform telemetry plumbing), SOAR (response orchestration), or `security_incident` (IR lifecycle).

**Hard laws:** SoR remains `cyber_security`. Surfaces under `/cyber-security/siem*`. Never incomplete event normalization. Never single-domain-only correlation. Never non-extensible detection rules. Never absent AI intelligence. Never telemetry without integrity validation. Never non-immutable storage. Never non-horizontally-scalable platform. Alerts escalate to SOC (P210-D); multi-system response via SOAR (P210-F); endpoint/network detection signals integrate with XDR (P210-G).

## Decision

1. SoR remains `cyber_security`
2. Surfaces under `/api/v1/cyber-security/siem*`
3. Law: `ENTERPRISE_CYBER_SECURITY_SIEM.md`
4. Catalogs: `CYBER_SIEM_*.v1.yaml`
5. Runtime: `cs_platform_siem.py`; aggregates; ACL; foundation
6. Quality gates enforce normalization, multi-domain correlation, extensible rules, AI, telemetry integrity, immutable storage, horizontal scale

## Consequences

- Complements P210-D SOC, P210-F SOAR, P210-G XDR
- Forbidden sibling BC: `siem_platform`

## References

ADR-361–366 · ENTERPRISE_EVENT_BUS.md · INTEGRATION_PLATFORM.md · ENTERPRISE_OBSERVABILITY_PLATFORM.md · NIST CSF · ISO 27001
