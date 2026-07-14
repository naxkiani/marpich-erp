# Digital Twin — Incident Response Runbook

**SLO burn / Sev classification · ADR-210**

| Sev | Example | Action |
|-----|---------|--------|
| Sev1 | Twin API down multi-region · compromise burst · AuthZ facet corruption | Page on-call · Security Incident if compromise · check Ingress/mesh · rollback Helm · BC activate |
| Sev2 | Sync lag p95 > 120s · DLQ depth high | Scale workers · check Event Mesh · pause noncritical consumers · self-heal policy |
| Sev3 | Prediction error budget · graph latency | Circuit-break AI · hop budget · Governance check |
| Sev4 | Single-tenant drift | Tenant ops · recover API |

## Triage checklist

1. `kubectl -n marpich get pods,hpa`  
2. Grafana: twin-overview / twin-sync / twin-intelligence  
3. Confirm Feature Flags and Policy gates  
4. Check DLQ depth `marpich.twin.dlq.v1`  
5. If canary: rollback weight to 0 / `helm rollback`  
6. Open `identity_twin.incident.opened` when Sev1/2 confirmed  

## War room

- Primary: Notification Center + on-call `platform-twin`  
- Security Sev1: hand off to Security Incident Platform (ADR-158)  
- Stakeholders: Notification templates (tenant admins, platform leadership)

## Post-incident

Sev1/Sev2 require PIR + lessons learned linked to BC improvement items.

## Communications

Update status page · notify tenant admins for Sev1 identity-adjacent impact.
