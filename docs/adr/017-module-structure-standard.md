# ADR-017: Module Structure Standard

## Status

Accepted

## Context

Marpich modules must be composable and consistent. Without a canonical structure, teams build monolithic contexts (e.g. one `hospital` module owning EMR, lab, pharmacy, and billing) and skip platform integrations (search, workflow, AI hooks).

Product leadership mandated: every business capability is a module; every module has defined layers and Core integrations; monolithic modules are forbidden.

## Decision

Adopt **`docs/architecture/MODULE_STRUCTURE_STANDARD.md`** as the module anatomy law.

Update **`MODULE_SYSTEM.md`** manifest with integration fields (`aiHooks`, `workflowHooks`, `reportTemplates`, `searchEntities`, `localizationNamespace`, `settingsSchema`).

Enforce via **`.cursor/rules/marpich-module-structure.mdc`** (`alwaysApply: true`).

## Consequences

- New capabilities in unrelated aggregates require new modules, not new files in existing monoliths
- Module PRs must complete the integration checklist
- Existing large contexts (e.g. `hospital`) may be split over time into `{namespace}.{capability}` modules

## Alternatives considered

- Fold into Platform Charter only — module structure deserves dedicated doc for scaffolding
- Enforce via codegen only — agents and humans need rule file until scaffolder exists
