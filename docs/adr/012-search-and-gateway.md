# ADR-012: Search Service and Platform Gateway Middleware

## Status

Accepted

## Context

Phase B requires cross-module discovery (Search) and production-grade request observability at the API edge. Industry modules must not query each other's databases; search indexes are built from integration events.

## Decision

### Search Service (`contexts/search/`)

- **Event-driven indexing** — subscribes to `*` (excluding `search.*`) and upserts denormalized documents
- **In-memory index** for dev/tests; **PostgreSQL** (`search.*` schema) for production
- **REST API** — `/api/v1/search/query`, `/suggest`, `/indices`, `/reindex`
- **Events published** — `search.index.updated`, `search.reindex.completed`

### Platform Gateway Middleware

- `PlatformGatewayMiddleware` adds `X-Request-ID`, propagates correlation ID, logs structured access metrics
- Runs on every HTTP request in the modular monolith (future external API Gateway/BFF compatible)

### Persistence completion

- Notifications and Settings now have PostgreSQL repositories (migrations 004/005)

## Consequences

- Search documents grow with event volume; production should use OpenSearch/Elasticsearch with same event contract
- Reindex clears tenant documents; event replay repopulates index
- Gateway middleware is foundation for OpenTelemetry export in a later phase
