# ADR-030: Shared Kernel

## Status

Accepted

## Context

Marpich has 44+ bounded contexts that need common primitives (money, addresses, pagination, API envelopes) without coupling business domains. Without a defined Shared Kernel, teams duplicate value objects or place business rules in `shared/`.

## Decision

1. Publish **Shared Kernel** at `docs/architecture/SHARED_KERNEL.md`.
2. Code lives under `backend/shared/` with strict rules: **no business logic**, only reusable enterprise components.
3. Kernel includes: Money, Currency, Address, Country, Language, TimeZone, Measurement, date utilities, audit metadata models, pagination/sorting/filtering, validation helpers, permissions evaluator, user/tenant context, localization helpers, common exceptions, response models, base repository port, entity/aggregate root, base application service marker, base DTO, Result type.
4. Bounded contexts may import `shared.*`; `shared` must never import `contexts.*`.
5. Cursor rule: `.cursor/rules/marpich-shared-kernel.mdc`.

## Consequences

### Positive

- Single source for money, pagination, API envelope
- Clear line between kernel and business domains

### Negative

- Kernel changes affect all services — require careful versioning
- Must resist pressure to add industry-specific "helpers" to shared

## Compliance

- Unit tests: `backend/shared/tests/`
- Extends SERVICE_BOUNDARIES (shared is not a service — no DB ownership)
