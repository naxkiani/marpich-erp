# ADR-034: Communication Architecture — Five Channels, Eight Requirements

## Status

Accepted

## Context

Marpich consists of independent business modules on a shared Core Platform. Modules must never access each other's databases. Prior docs ([SERVICE_BOUNDARIES.md](../architecture/SERVICE_BOUNDARIES.md), [DDD_DOMAIN_ARCHITECTURE.md](../architecture/DDD_DOMAIN_ARCHITECTURE.md)) listed four communication channels but did not unify:

- Scheduled synchronization as a first-class pattern
- The eight cross-cutting requirements on **every** communication (authenticated through observable)
- Communication vs compile-time dependency graphs
- Explicit rejection of direct coupling with diagrams

Product leadership mandated a single **Communication Architecture** reference before implementing inter-module features.

## Decision

Adopt **`docs/architecture/COMMUNICATION_ARCHITECTURE.md`** as canonical inter-module communication law.

### Five allowed methods

1. **REST API** — sync, OpenAPI, `/api/v1/`
2. **Internal Application Contracts** — JSON schemas, DTOs, `shared/contracts/` — no domain sharing
3. **Domain Events** — domain (internal) + integration (cross-module) via outbox
4. **Message Broker** — Kafka / outbox transport (Event Fabric)
5. **Scheduled Synchronization** — cron jobs pulling via REST or replaying events — never cross-schema SQL

### Eight requirements (all channels)

Authenticated · Authorized · Logged · Audited · Versioned · Traceable · Retryable · Observable

### Reject

- Cross-database access
- Peer domain imports
- In-process peer application service calls
- Undocumented service-to-service APIs
- Shared mutable state without contract

### Diagrams

Communication architecture doc includes: platform overview, REST sequence, event/outbox flow, contract flow, broker flow, scheduled sync sequence, rejection map, runtime communication graph.

Compile-time dependency graph remains [DEPENDENCY_GRAPH.md](../architecture/DEPENDENCY_GRAPH.md).

## Consequences

- SERVICE_BOUNDARIES updated to five channels + link to communication doc
- Agents enforce ACL + contracts before cross-module features
- Scheduled jobs must use API/event paths — code review rejects cross-schema queries
- Contract tests and dependency checker remain enforcement backbone

## Alternatives considered

- REST-only microservices — too synchronous; events required for ERP workflows
- Shared database read replicas — violates module ownership
- Four channels without scheduled sync — batch projections lacked canonical pattern
