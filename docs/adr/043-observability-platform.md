# ADR-043: Enterprise Observability Platform — Unified Telemetry

## Status

Accepted

## Context

Marpich requires full operational visibility: application logs, API logs, performance and business metrics, distributed tracing, health checks, infrastructure metrics (CPU, memory, database, queue, cache), error/exception tracking, slow query detection, alerting, a system health dashboard, and AI-driven health analysis.

Existing pieces are fragmented:

- ADR-013 OpenTelemetry in `shared/infrastructure/observability/telemetry.py`
- Gateway middleware structured API logs + `http.server.duration`
- Analytics context for business metrics, dashboards, alerts
- Platform `/health` endpoint only
- AI service for insights but no dedicated health analysis API

Audit Platform (ADR-042) covers compliance trails — observability is a separate operational concern.

## Decision

Adopt **`docs/architecture/ENTERPRISE_OBSERVABILITY_PLATFORM.md`** as canonical observability law.

### Unified signal layers

| Layer | Owner |
|-------|-------|
| OTel traces + perf metrics | `shared/infrastructure/observability/` |
| Application + API logs | Structured logging + gateway |
| Business metrics + tenant dashboards | `contexts/analytics/` |
| Health probes | Platform + per-context `/health` |
| Infra metrics (DB, queue, cache, CPU, memory) | OTel + Prometheus exporters |
| Error / slow query | Global handlers + SQLAlchemy hooks |
| Alerting | Analytics rules + Alertmanager → Notifications |
| System Health Dashboard | `HEALTH_DASHBOARD.v1.yaml` |
| AI Health Analysis | AI Service `/ai/health/analyze` |

### Distinction from Audit

Observability: operational, sampled, shorter retention. Audit: immutable compliance.

## Consequences

- Extend OTel with SQLAlchemy, httpx, host metrics
- Implement slow query listener and error export
- Add platform health dashboard API
- Add AI health analysis endpoints
- Modules must not create local metrics stores

## Alternatives considered

- Third-party-only (Datadog-only) — rejected (vendor lock-in; OTel standard)
- Merge observability into Audit — rejected (different retention/compliance model)
- Per-module monitoring stacks — rejected (fragmentation)
