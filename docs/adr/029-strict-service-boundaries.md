# ADR-029: Strict Service Boundaries

## Status

Accepted

## Context

Marpich decomposes into 44+ bounded contexts and 29 platform services. Without explicit boundary law, teams introduce:

- Shared tables and cross-schema JOINs
- Global mutable caches across contexts
- Duplicated auth, workflow, tax, and notification logic
- Direct domain-layer imports between services

ADR-008 established event-only cross-context communication. Product leadership now requires a complete **service ownership model** covering database, rules, events, API, permissions, jobs, reports, AI config, and module configuration — plus absolute prohibitions on shared mutable state, cross-service queries, and logic duplication.

## Decision

1. Publish **Strict Service Boundaries** at `docs/architecture/SERVICE_BOUNDARIES.md`.
2. Each service (bounded context) **exclusively owns** nine assets: Database, Business Rules, Events, API, Permissions, Background Jobs, Reports, AI Models/Config, Configuration.
3. **Never allow:**
   - Shared mutable state between services
   - Cross-service database queries or ORM imports
   - Business logic duplication (Core or peer services)
4. **Communication only through:**
   - REST APIs
   - Domain / Integration Events
   - Message Broker (Kafka / outbox)
   - Application Contracts (schemas, DTOs, JSON event definitions)
5. Mandatory **Anti-Corruption Layer** on all event consumers.
6. Cursor rule: `.cursor/rules/marpich-service-boundaries.mdc`.

## Consequences

### Positive

- Independent deploy, scale, and team ownership
- Clear audit trail for architecture reviews
- Contracts are the only coupling surface

### Negative

- Eventual consistency and saga design required
- More ACL and schema maintenance
- No "quick JOIN" shortcuts for reports — use read models

## Compliance

- Extends ADR-008 (bounded context isolation)
- Referenced from DDD_DOMAIN_ARCHITECTURE, PLATFORM_CHARTER, CHIEF_ARCHITECT_MANDATE
