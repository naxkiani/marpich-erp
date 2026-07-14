# Digital Twin — Operator Guide

**ADR-209 · Prompt 199-D1**

## Day-2 operations

| Action | How |
|--------|-----|
| Provision twin kinds for tenant | Activate module + kind catalog seed API |
| Scale sync workers | HPA/KEDA on `twin-sync-workers` or Helm values |
| Pause sync | Feature Flag `twin.sync.enabled=false` or Policy gate |
| Diagnose lag | Grafana twin-sync dashboard · SyncRun events |
| Drain DLQ | Ops runbook `digital-twin-dlq.md` + Orchestration replay |
| Rotate job token | Secrets provider + External Secrets refresh |
| Trigger snapshot | CronJob or `POST .../jobs/snapshot` |

## SLOs (see SRE catalog)

- API availability 99.99%  
- Sync lag p95 ≤ 30s (alert 120s)  
- Graph query p95 ≤ 500ms  
- Prediction p95 ≤ 2000ms (includes AI Platform)

## Forbidden operator actions

- Direct SQL into peer schemas  
- Bypassing GitOps with local `kubectl apply` of unsigned images in production  
- Embedding LLM keys into twin ConfigMaps  

## Escalation

Sev1/Sev2 → platform-twin on-call · postmortem required.
