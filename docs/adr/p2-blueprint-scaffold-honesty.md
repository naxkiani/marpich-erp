# ADR-P2: Blueprint Fabrics & Empty Scaffold Honesty

## Status

Accepted — Completeness audit P2

## Context

MEOS accrued large **catalog/docs fabrics** (`quantum`, `robotics`, `biotechnology`, `space`, `civilization`) and **12 empty industry scaffolds**. Treating either as Functional apps inflated readiness scores without login-scoped CRUD depth.

## Decision

1. **Blueprint fabrics** (`BLUEPRINT_CONTEXT_IDS`): architecture/docs/catalog only until a Functional activation. Live OpenAPI registration is **off by default**. Opt-in via `MARPICH_ENABLE_BLUEPRINT_APIS=true` or `MARPICH_APP_PROFILE=blueprint`.
2. **Empty industry scaffolds** (`EMPTY_INDUSTRY_SCAFFOLD_IDS`): remain `coming_soon` / deferred. Do **not** expand placeholder trees or claim ACTIVE/TESTED until a real vertical slice ships.
3. **Stop catalog inflation:** new foundation YAML/capability catalogs for blueprint fabrics do not change readiness. Status in MEOS Application Registry is **`BLUEPRINT`**, never `TESTED` / `PRODUCTION_READY` / `ACTIVE` without a Functional gate.

## Consequences

- Default `full` profile no longer exposes blueprint routers in OpenAPI.
- Architecture tests freeze the 12 empty scaffolds and the five blueprint IDs.
- P3 still owns contract CI for missing router packages.

## References

- Completeness audit canvas P2 todos
- `backend/core/presentation/api/startup_registry.py`
- `docs/meos/execution/MEOS_APPLICATION_REGISTRY.md`
