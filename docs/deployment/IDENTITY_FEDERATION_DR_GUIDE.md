# Identity Federation — Disaster Recovery Guide

**ADR:** [225](../adr/225-enterprise-identity-federation-deployment-observability-devsecops.md) · **Targets:** RPO ≤ 5 min · RTO ≤ 30 min

## 1. Failure modes

| Mode | Detection | Primary action |
|------|-----------|----------------|
| API pod crash | HPA / readiness fail | Mesh + K8s restart / scale |
| Region outage | Multi-AZ health + synthetic login | Failover DNS / active-passive promote |
| Postgres primary loss | Patroni/HA alarms | Promote standby + JWKS still from Redis |
| Outbox backlog | `sli.outbox_lag` | Scale dispatcher · replay |
| IdP connector down | Health probe | Integration Platform retry / secondary IdP |

## 2. Backup & restore

1. Continuous WAL / PITR for `federation` schema  
2. Cross-region snapshot daily (verify weekly)  
3. Redis session: ephemeral — re-auth acceptable within RTO  
4. Secrets: Vault — never restore from Git  

## 3. Failover drill checklist

1. Freeze non-critical deploys (error budget policy)  
2. Announce drill via Notification Platform  
3. Promote standby / flip geo DNS  
4. Verify `/api/v1/federation/ops/health` + login synthetic  
5. Replay pending outbox  
6. Record drill in `/federation/ops/dr/drill`  
7. Failback plan documented before prod cutover  

## 4. Contacts

Platform SRE on-call · Identity Federation owners · Security Operations
