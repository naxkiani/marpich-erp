# ADR-159: Enterprise Business Continuity Platform

## Status

Accepted

## Context

Disaster recovery, business continuity planning, backup strategy, RPO/RTO management, failover, high availability, replication, emergency operations, and recovery testing are not unified in a single orchestration layer. Capabilities are fragmented across data protection (backup encryption), security incident (emergency ops), and workflow (emergency lock).

Requirements:
- Unified BCP/DR plan management with RPO and RTO tracking
- Backup strategy with delegation to data protection
- Failover and HA status monitoring
- Replication lag tracking
- Recovery testing with pass/fail against RPO/RTO targets
- Continuity dashboard

## Decision

Implement **Enterprise Business Continuity Platform** at `/api/v1/business-continuity`.

### New bounded context

`backend/contexts/business_continuity/` — orchestration layer over DR/BCP capabilities.

### Capabilities (11)

| Capability | Feature |
|------------|---------|
| Disaster Recovery | DR plans with recovery steps |
| Business Continuity Plan | BCP for business functions |
| Backup Strategy | Backup schedules with RPO (delegates encryption to data_protection) |
| Recovery Point Objective | RPO tracking per plan and backup |
| Recovery Time Objective | RTO tracking per plan |
| Failover | Failover initiation and completion |
| High Availability | HA status and availability monitoring |
| Replication | Replication lag and sync status |
| Emergency Operations | EOC activation (delegates to security_incident) |
| Recovery Testing | Scheduled and executed DR tests |
| Continuity Dashboard | Unified continuity overview |

### Aggregates

- `ContinuityTenantProfile` — default RPO/RTO, HA settings, test frequency
- `ContinuityPlan` — BCP/DR/emergency ops plans
- `BackupStrategy` — backup configuration
- `FailoverRecord` — failover events
- `RecoveryTest` — test runs with RPO/RTO results

### Policy Keys (domain: `tax`)

- `continuity.rpo.default_hours`
- `continuity.rto.default_hours`
- `continuity.failover.auto_trigger_threshold`
- `continuity.testing.frequency_days`
- `continuity.ha.replication_lag_threshold`

### Events

- `continuity.plan.created`
- `continuity.failover.initiated`
- `continuity.failover.completed`
- `continuity.test.completed`
- `continuity.emergency_ops.activated`

### API Surface

- `GET /catalog`, `GET /dependency-map`, `POST /seed`
- `GET /dashboard`
- `GET/POST /plans`
- `GET/POST /backups`
- `GET /rpo-rto`, `GET /high-availability`, `GET /replication`
- `POST/GET /failover`
- `POST /emergency-ops`
- `POST/GET /tests`, `POST /tests/{ref}/run`

### Permissions

- `continuity.read`, `continuity.write`, `continuity.test`

## Consequences

- Seed registers 4 plans (DR, BCP, treasury BCP, EOC) and 3 backup strategies
- Recovery tests simulate RPO/RTO achievement deterministically
- Backup encryption delegated to data_protection — no local encryption logic
- Emergency ops delegated to security_incident — no duplicate incident response

## Alternatives considered

- Extend data_protection only — rejected (backups ≠ full BCP/DR lifecycle)
- Per-module DR only — rejected (fragmentation)
- Autonomous failover — rejected (human-initiated failover only)
