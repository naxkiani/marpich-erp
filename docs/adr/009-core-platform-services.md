# ADR-009: Core Platform Service Decomposition

## Status

Accepted

## Context

Marpich ERP must serve 25+ industries through one composable platform. Every industry module needs identity, documents, notifications, audit, and other cross-cutting capabilities without duplicating implementations.

## Decision

Decompose the **Core Platform** into 19 logical services with:

1. **REST API** per service (`/api/v1/{prefix}`)
2. **Integration events** for all state mutations
3. **No shared domain models** between services or modules
4. **Module manifest registration** for permissions and event subscriptions

Logical services may be deployed as:

- Modular monolith (current Python backend)
- Grouped deployables (identity plane, data plane, ops plane)
- Full microservices at enterprise scale

### Identity plane split

| Service | Responsibility |
|---------|----------------|
| Identity | User profile lifecycle |
| Authentication | Tokens, login, MFA, SSO |
| Permission | Catalog, roles, assignments |
| Authorization | RBAC/ABAC policy evaluation |

These four may share a database schema (`identity`) but maintain separate application boundaries.

### Storage split

| Service | Responsibility |
|---------|----------------|
| File Storage | Raw blobs, presigned URLs |
| Media | Transcoding, variants |
| Document | Business metadata, versions, signatures |

Document Service references File Storage object IDs; Media Service processes File Storage commits.

## Consequences

### Positive

- Every module reuses the same platform contracts
- Services scale independently at enterprise tier
- Event catalog enables integration without coupling
- Clear ownership for security (auth plane) vs content (data plane)

### Negative

- More services to operate in full microservice mode
- Identity plane split adds latency unless co-located
- Event fan-out (audit, search, analytics) requires careful Kafka partitioning

## Compliance

- All tables include `tenant_id`
- All REST endpoints require authorization except explicit public routes
- All mutations emit audit + outbox events
