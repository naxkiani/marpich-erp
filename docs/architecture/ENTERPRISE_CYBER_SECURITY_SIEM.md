# Enterprise Cyber Security — SIEM Platform (P210-E)

**SoR:** `cyber_security` · **ADR:** 367 · **API:** `/api/v1/cyber-security/siem*`

## Mission

Collect, normalise, correlate, enrich, analyse, store and investigate security events across MEOS — telemetry into actionable cyber intelligence under Zero Trust.

## Vision

AI-native SIEM: every security event captured, every log becomes intelligence, every alert risk-scored, every anomaly explainable, every investigation data-driven, every security decision evidence-based.

## Architecture layers

Security Sources → Collection → Ingestion → Normalization → Parsing → Enrichment → Correlation → Detection → Risk Analytics → Alert Engine → Investigation → Long-Term Storage → Executive Dashboards

## Hard laws (quality gates)

- Never event normalization is incomplete
- Never correlation cannot span multiple domains
- Never detection rules are not extensible
- Never AI intelligence is absent
- Never telemetry lacks integrity validation
- Never storage is not immutable
- Never platform cannot scale horizontally

## Boundaries

| Concern | Owner |
|---|---|
| Security event telemetry / SIEM analytics | `cyber_security` (this surface) |
| Platform OTel / infra metrics plumbing | Observability |
| Alert triage / SOC ops | P210-D SOC |
| Playbook response | P210-F SOAR |
| Endpoint/network active defence | P210-G XDR |
| IR lifecycle | `security_incident` |
| Connectors | Integration Platform |

## Forbidden

- Sibling BC `siem_platform`
- Incomplete common-event normalization
- Correlation limited to a single domain silo
- Non-extensible detection rule packs
- Absent AI security intelligence
- Telemetry without integrity validation
- Mutable security event store
- Vertically-only (non-horizontal) scale assumptions

## Compliance

ISO 27001 · SOC 2 · PCI DSS · GDPR · NIST CSF
