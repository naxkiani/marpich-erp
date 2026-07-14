# Digital Twin — Disaster Recovery Guide

**Prompt:** V03-C02-P199-D2.2 · **ADR-210**  
**Companion:** [DIGITAL_TWIN_DR_BCP.md](DIGITAL_TWIN_DR_BCP.md) · Topology `TWIN_DEPLOYMENT_TOPOLOGY.v1.yaml`

## Objectives (policy-configurable)

| Mode | RPO | RTO | Notes |
|------|-----|-----|-------|
| Hot | ~0 | ≤ 5m | Banking / government / tax tenants |
| Warm | 5m | 30m | Enterprise default |
| Cold | 1h | 4h | Non-prod / cost-optimized |

## Topology

```text
Primary region: marpich-iam + twin-sync-workers + Postgres + Event Mesh + Redis
DR region:      warm/hot standby + mirrored topics + streaming replica
Edge:           cached projections; offline sync when mesh returns
```

## Failover procedure

1. Confirm Sev1 + GLB health.  
2. Promote DR Postgres / switch mesh consumers (IaC runbook).  
3. Point GLB / DNS to DR ingress.  
4. Publish `identity_twin.dr.failover`.  
5. Run smoke: `/health`, twin list, sync lag probe.  
6. Rebuild corrupt twins via recover API + SoR full sync if needed.  
7. File recovery report (Reporting Platform dataset).

## Recovery verification

- Automated: SyncRun success ratio · lag SLO · scrape `up{job=marpich-iam-twin}`  
- Quarterly: disaster simulation (chaos) + BC test record in ADR-159  

## Immutable backups

Postgres PITR + object-store snapshot encryption + legal hold Policy. Validation restore probe quarterly.
