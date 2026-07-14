# Digital Twin Observability — Administrator Guide

**ADR-210 · Prompt 199-D2.2**

## Enable scrapes & dashboards

1. Ensure Helm ServiceMonitor includes `/api/v1/identity-twins/metrics`.  
2. Deploy Prometheus rules `digital-twin.yml` and scrape job `marpich-iam-twin`.  
3. Confirm Grafana folder **Marpich Digital Twin** provisions overview/sync/intelligence boards.  

## Alert routing

Alertmanager → Notification Platform templates (`twin.alert.*`).  
Configure on-call `platform-twin` and maintenance windows via Policy `twin.alerts.maintenance`.

## AIOps

Do not deploy twin-local ML. Wire anomaly events to Observability AI Health and Twin Intelligence consumers.

## Access control

Grafana/Prom RBAC + tenant isolation on Analytics twin KPIs. Never share cross-tenant raw logs.

## Acceptance checklist

- [ ] `up{job="marpich-iam-twin"} == 1`  
- [ ] Test alert reaches Notification Center  
- [ ] Sync lag dashboard renders  
- [ ] DR drill report filed this quarter  
