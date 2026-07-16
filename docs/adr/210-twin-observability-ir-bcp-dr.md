# ADR-210: Twin Observability, Monitoring, Incident Response, BCP & DR (P199-D2.2)

## Status

Accepted

## Context

ADR-209 delivered Twin Platform Engineering / DevSecOps. Twin SRE catalogs and DR outline exist, but the ecosystem still needs a formal **Observability / IR / BCP / DR profile** wired to Enterprise Observability (ADR-179/043), Notification Platform, Business Continuity (ADR-159), Security Incident (ADR-158), Reporting, and Analytics — without a second Prometheus/Grafana or backup/BC engine inside the twin BC.

**Prompt ID:** V03-C02-P199-D2.2 · **ADR number:** 210

## Decision

1. Twin Observability is a **profile** over Enterprise Observability SoR — metrics, logs, traces, alerts, dashboards extend `infrastructure/observability/` and METRICS_CATALOG; twin domain emits OTel + `/metrics` only.  
2. Alert routing: Prometheus Alertmanager / `enterprise_observability.alert.triggered` → **Notification Platform** (email/SMS/Teams/Slack/in-app). Never module SMTP.  
3. AIOps: use platform AI Health + Twin Intelligence anomaly events — no twin-local LLM ops engine.  
4. Incident Response: severity catalog + war-room workflows; Sev1 identity-security → `security_incident`; ops SLO burn → observability IR + twin runbooks.  
5. Business Continuity / DR: **register** twin continuity functions with ADR-159 engine; topology RPO/RTO from Twin catalogs; twin docs are ops profiles, not a parallel BC/DR product.  
6. Backup: platform backup policies + Postgres PITR + Event Mesh retention — twin stores policy refs only.  
7. Self-healing: Policy-driven automation (HPA/KEDA, cert-manager, queue replay, twin recover APIs) — thresholds never hardcoded in domain.  
8. Reporting: Reporting Platform datasets for SLA/incident/recovery; Analytics for twin business KPIs.  
9. Everything configurable: alert rules, thresholds, recovery/backup/notification/incident policies.

## Consequences

- D3 from ADR-209 roadmap (dashboards/alerts/runbooks) is completed by this ADR’s artifacts.  
- Grafana/Prometheus files become canonical twin ops wiring.  
- Acceptance: scrape twin metrics job healthy; alerts fire to Notification; DR drill documented quarterly.

## References

- [ENTERPRISE_TWIN_OBSERVABILITY_IR_BCP_DR.md](../architecture/ENTERPRISE_TWIN_OBSERVABILITY_IR_BCP_DR.md)  
- ADR-043 · 158 · 159 · 179 · 203 · 207 · 208 · 209 · 201d · 202e
