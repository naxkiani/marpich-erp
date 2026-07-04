# ADR-031: Module Architecture Consistency

## Status

Accepted

## Context

Marpich has 44+ bounded contexts and a growing module catalog. Without a **single identical folder tree** per module, agents and teams invent alternate layouts (`handlers/` vs `use_cases/`, flat `router.py` vs `rest/`, missing `specifications/`, skipped test tiers). That erodes reviewability, scaffolding, and cross-team navigation.

Product leadership mandated: every module follows identical architecture across Application, Domain, Infrastructure, Presentation, Tests, and Documentation layers.

## Decision

Adopt **`docs/architecture/MODULE_ARCHITECTURE.md`** as the canonical module anatomy.

1. **Implementation root:** `backend/contexts/{module_id}/` with mandatory subfolders:
   - Application: `commands/`, `queries/`, `dto/`, `validators/`, `use_cases/`
   - Domain: `aggregates/` (or `entities/`), `value_objects/`, `services/`, `ports/`, `events/`, `specifications/`
   - Infrastructure: `persistence/`, `messaging/`, `caching/`, `storage/`, `external_apis/`
   - Presentation: `rest/`, `websocket/`, `reports/`, `dashboard/`
   - Tests: `unit/`, `integration/`, `performance/`
   - Documentation: `docs/api/`, `docs/architecture/`

2. **Scaffold:** `backend/contexts/_template/` — copy for every new module.

3. **Enforcement:** `.cursor/rules/marpich-module-architecture.mdc` (`alwaysApply: true`).

4. **Legacy:** Existing modules may keep `application/service.py` and `presentation/router.py` until migrated; **new modules must use the full tree**.

5. **N/A folders:** Mandatory folders remain; mark unused with `README.md` (e.g. WebSocket).

**Law: Never violate module consistency.**

## Consequences

- PRs that omit mandatory folders or rename layers are architecture rejections
- `MODULE_STRUCTURE_STANDARD.md` defers layer detail to `MODULE_ARCHITECTURE.md`
- Incremental migration of hospital, clinic, etc. — no big-bang refactor required

## Alternatives considered

- Codegen-only enforcement — insufficient for human contributors and AI agents without doc + rule
- Merge into SERVICE_BOUNDARIES — boundaries address ownership; this addresses internal layout
- Optional folders — rejected; consistency requires identical trees
