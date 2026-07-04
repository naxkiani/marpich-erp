# ADR-025: DDD Domain Architecture

## Status

Accepted

## Context

Marpich uses DDD tactically (layers, events) but needed a single canonical document for strategic domain types (Core, Supporting, Generic), complete per-domain ownership, and hard isolation rules: no shared tables, no logic outside domain, communication only via events, public APIs, and application contracts.

## Decision

Adopt **`docs/architecture/DDD_DOMAIN_ARCHITECTURE.md`** as the full DDD law.

Enforce via **`.cursor/rules/marpich-ddd-domains.mdc`** (`alwaysApply: true`).

Retain [DDD_ARCHITECTURE.md](../architecture/DDD_ARCHITECTURE.md) as tactical/context-map reference with link to canonical doc.

Integrate with [CHIEF_ARCHITECT_MANDATE.md](../architecture/CHIEF_ARCHITECT_MANDATE.md).

## Consequences

- Cross-schema queries and shared ORM models are rejected
- New domains must complete DDD checklist
- ACL required on all inbound integration events

## Alternatives considered

- Only DDD_ARCHITECTURE.md — lacked explicit Core/Supporting/Generic ownership matrix and DB isolation law
