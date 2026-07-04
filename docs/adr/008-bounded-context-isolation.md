# ADR-008: Strict Bounded Context Isolation

## Status

Accepted

## Context

Marpich ERP serves 37+ business domains (banking, hospital, university, manufacturing, etc.). Allowing direct dependencies between domains causes:

- Coupling that prevents independent deployment and scaling
- Shared model corruption (Hospital `Patient` leaking into Banking)
- Circular dependency chains
- Inability to activate industry packs independently

## Decision

1. Each bounded context lives in `backend/contexts/{name}/` with full Clean Architecture layers
2. **No compile-time imports** between business context domain layers
3. Cross-context communication **only** via versioned **Integration Events** on Kafka
4. Every event consumer implements an **Anti-Corruption Layer** in `infrastructure/acl/`
5. Cross-context references use **IDs only** — never foreign aggregate objects
6. `Analytics`, `Search`, and `Notifications` subscribe broadly but never call back synchronously

## Consequences

### Positive
- Independent deploy, scale, and team ownership per context
- Industry packs activate contexts without code forks
- Event replay enables analytics and audit
- Clear published language per context

### Negative
- Eventual consistency — sagas required for cross-context workflows
- More boilerplate (ACL, outbox, schemas)
- Schema evolution requires versioned events (`*.v1`, `*.v2`)

## Enforcement

- CI: `lint-imports` blocks `contexts.X.domain` imports from `contexts.Y`
- Code review checklist in `backend/modules/_template/MODULE.md`
- Event schemas registered in `docs/architecture/events/`

## Alternatives Considered

1. **Shared domain model** — Rejected: creates big ball of mud
2. **Synchronous REST between services** — Rejected: tight runtime coupling
3. **Shared database tables** — Rejected: violates context boundaries
