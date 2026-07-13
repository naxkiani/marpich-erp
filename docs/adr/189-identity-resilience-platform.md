# ADR-189: Identity Resilience Platform (Phase P8)

## Status

Accepted

## Context

Phases P1–P7 delivered the full MEIAAP IAM stack including directory sync workers (P6) and AI-assisted identity risk scoring (P7). ADR-187/188 follow-up requires **multi-region high availability** for directory sync and risk scoring workers — leader election, heartbeat monitoring, failover orchestration, and replication health without coupling to the general `business_continuity` DR platform.

## Decision

Implement **Identity Resilience Platform** at `/api/v1/identity-resilience` as bounded context `identity_resilience`.

### 10 Platform Capabilities

1. Region Catalog
2. Worker Registry
3. Directory Sync Worker HA
4. Risk Scoring Worker HA
5. Leader Election
6. Failover Orchestration
7. Replication Health
8. Policy-Driven Resilience
9. Resilience Dashboard
10. Identity Resilience API

### Aggregates

- `ResilienceProfile`
- `RegionDescriptor`
- `WorkerDeployment`
- `FailoverEvent`

### Policy Keys

- `identity_resilience.multi_region.enabled`
- `identity_resilience.failover.auto_trigger`
- `identity_resilience.worker.heartbeat_timeout_seconds`
- `identity_resilience.replication.lag_threshold_seconds`

### Events

- `identity_resilience.worker.registered`
- `identity_resilience.failover.initiated`
- `identity_resilience.failover.completed`
- `identity_resilience.region.health_changed`

### Events Subscribed

- `directory.sync.completed` (leader heartbeat)
- `identity_risk.score.computed` (leader heartbeat)

### API Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/identity-resilience/catalog` | Capability catalog |
| POST | `/identity-resilience/seed` | Bootstrap regions + profile |
| GET | `/identity-resilience/dashboard` | HA dashboard |
| GET/POST | `/identity-resilience/regions` | Region registry |
| GET/POST | `/identity-resilience/workers` | Worker deployment registry |
| POST | `/identity-resilience/workers/{ref}/heartbeat` | Worker heartbeat |
| GET | `/identity-resilience/replication` | Replication lag health |
| POST | `/identity-resilience/failover` | Manual/auto failover |
| POST | `/identity-resilience/health-check` | Stale leader detection + failover |
| POST | `/identity-resilience/workers/directory-sync/run` | HA-gated directory sync |
| GET | `/identity-resilience/failovers` | Failover history |

### Worker delegation

- Directory sync: delegates to `DirectoryApplicationService.run_sync_worker()` only when local region matches elected leader (`MARPICH_REGION_ID`).
- Risk scoring: event-driven via `identity_risk`; HA layer tracks leader heartbeats on `identity_risk.score.computed`.

### Default regions (seed)

- `eu-west-1` (primary)
- `us-east-1` (standby)

## Consequences

- **Positive:** MEIAAP workers survive regional leader failure with explicit failover audit trail.
- **Positive:** Replication lag monitoring per region with health change events.
- **Neutral:** Leader election is registry-based in P8; distributed consensus (Raft/etcd) deferred.
- **Follow-up:** Gateway routing by region; cross-region read replicas for identity Postgres.

## References

- ADR-187 Enterprise Directory Platform
- ADR-188 Identity Risk Platform
- ADR-159 Enterprise Business Continuity Platform
