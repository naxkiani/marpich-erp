# ADR-013: OpenTelemetry Observability

## Status

Accepted

## Context

Production deployments need distributed tracing and request metrics across the modular monolith. The platform gateway middleware already logs access events but lacks vendor-neutral export to Grafana Tempo, Jaeger, Datadog, or similar backends.

## Decision

Add optional **OpenTelemetry** integration:

| Component | Role |
|-----------|------|
| `shared/infrastructure/observability/telemetry.py` | Provider bootstrap, FastAPI instrumentation |
| `PlatformGatewayMiddleware` | Span attributes + `http.server.duration` histogram |
| Settings | `OTEL_ENABLED`, `OTEL_EXPORTER_OTLP_ENDPOINT`, etc. |

### Configuration

```env
OTEL_ENABLED=true
OTEL_SERVICE_NAME=marpich-backend
OTEL_SERVICE_VERSION=0.1.0
OTEL_ENVIRONMENT=production
OTEL_EXPORTER_OTLP_ENDPOINT=http://127.0.0.1:4318
OTEL_CONSOLE_EXPORT=false
OTEL_EXCLUDED_URLS=/api/v1/health,/api/docs,/api/redoc,/api/openapi.json
```

### Export modes

- **Disabled (default)** — zero overhead; used in unit/integration tests
- **OTLP HTTP** — production path to collector (Grafana Alloy, OTel Collector, etc.)
- **Console** — local dev when `OTEL_CONSOLE_EXPORT=true`

### Dependencies

Optional extra: `pip install marpich-backend[observability]`

Included in `dev` dependencies for CI validation.

## Consequences

- FastAPI routes auto-instrumented when enabled
- Health/docs endpoints excluded from trace noise by default
- SQLAlchemy/httpx instrumentation can be added in a follow-up
- Shutdown flushes spans/metrics on app lifespan exit
