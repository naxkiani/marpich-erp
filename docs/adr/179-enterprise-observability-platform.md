# ADR-179: Enterprise Observability Platform

## Status

Accepted

## Context

Marpich ERP has OpenTelemetry bootstrap (`shared/infrastructure/observability/telemetry.py`), gateway API logs, and Analytics business metrics — but lacks a unified enterprise platform for operational telemetry: distributed tracing, centralized logging, infrastructure metrics, health probes, queue/API/workflow/AI monitoring, alerting, incident management, service dependency graphs, and operational dashboards.

Architecture law: [ENTERPRISE_OBSERVABILITY_PLATFORM.md](../architecture/ENTERPRISE_OBSERVABILITY_PLATFORM.md)

## Decision

Implement **Enterprise Observability Platform** at `/api/v1/enterprise-observability`.

### 14 Platform Capabilities

1. Distributed Tracing
2. Centralized Logging
3. Metrics
4. Health Checks
5. Business KPIs
6. Event Monitoring
7. Queue Monitoring
8. API Monitoring
9. Workflow Monitoring
10. AI Monitoring
11. Alerting
12. Incident Management
13. Service Dependency Graph
14. Operational Dashboard

### Aggregates

- `ObservabilityProfile`
- `TraceSpan`
- `LogEntry`
- `MetricSnapshot`
- `HealthCheckResult`
- `MonitoringAlert`
- `ObservabilityIncident`

### Policy Keys

- `enterprise_observability.tracing.enabled`
- `enterprise_observability.tracing.sampling_rate`
- `enterprise_observability.logging.retention_days`
- `enterprise_observability.metrics.enabled`
- `enterprise_observability.health_checks.enabled`
- `enterprise_observability.alerting.enabled`
- `enterprise_observability.incident.auto_create.enabled`

### Events

- `enterprise_observability.alert.triggered`
- `enterprise_observability.incident.created`
- `enterprise_observability.incident.resolved`
- `enterprise_observability.dashboard.generated`

### Delegates

- Business KPIs → `analytics`
- Alert delivery → `notifications`
- Security incidents → `security_incident`
- OTel bootstrap → `shared/infrastructure/observability/telemetry.py`

### Key Endpoints

| Endpoint | Purpose |
|----------|---------|
| `GET /catalog` | 14 capabilities + policy keys |
| `GET /dependency-map` | Platform dependency graph |
| `GET /service-dependency-graph` | Service topology from route registry |
| `GET /operational-dashboard` | System health dashboard |
| `GET /health-dashboard` | Alias for operational dashboard |
| `GET /traces` | Distributed trace spans |
| `GET /logs` | Centralized log entries |
| `GET /metrics` | Metric snapshots |
| `GET /health-checks` | Context readiness probes |
| `GET /business-kpis` | Business KPI tiles |
| `GET /events` | Event throughput monitoring |
| `GET /queues` | Outbox/queue lag monitoring |
| `GET /api-monitoring` | API latency and error rate |
| `GET /workflows` | Workflow completion monitoring |
| `GET /ai-monitoring` | AI request/latency/error metrics |
| `GET/POST /alerts` | Alert rule management |
| `GET/POST /incidents` | Incident lifecycle |

### Permissions

- `enterprise_observability.read`
- `enterprise_observability.write`
- `enterprise_observability.admin`

### Admin portal dashboard

- Route: `/enterprise/observability`
- Client: `enterpriseObservabilityClient.ts`
- Component: `EnterpriseObservabilityDashboardPage.tsx`

## Consequences

- Unified operational telemetry API — modules never implement local metrics stores
- Service dependency graph auto-generated from `route_registry.yaml`
- Operational dashboard follows `HEALTH_DASHBOARD.v1.yaml` schema
- Critical alerts auto-create incidents when policy allows
- All alerts route via integration events to Notification Platform
