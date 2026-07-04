# ADR-026: Bounded Contexts Registry

## Status

Accepted

## Context

Marpich requires an authoritative catalog of bounded contexts with independence guarantees (terminology, schema, rules, permissions, workflows, events, docs). Several user-facing domains (Clinic, Municipality, POS, Localization) were missing from the code registry. Finance and healthcare clusters risked conceptual merging.

## Decision

Publish **`docs/architecture/BOUNDED_CONTEXTS_REGISTRY.md`** as master catalog.

Register new contexts in `backend/contexts/registry.py`:
- `clinic`, `municipality`, `pos`, `localization`

Split Localization from Settings description (settings = config; localization = translations).

Add `context.yaml` manifests for new contexts.

Total registered contexts: **44** (42 user-listed + organization + audit).

## Consequences

- Hospital and Clinic remain separate evolving contexts
- Government and Municipality are separate
- POS separate from Sales/Retail back-office
- Localization evolves independently of Settings

## Alternatives considered

- Clinic as submodule of hospital — rejected; violates independent evolution
- Localization inside Settings — rejected; user mandate for separate context
