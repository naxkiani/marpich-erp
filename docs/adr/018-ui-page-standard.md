# ADR-018: UI Page Standard

## Status

Accepted

## Context

Engineering Quality Standard requires accessibility, dark mode, and RTL/LTR but did not enumerate the full enterprise UI surface: command palette, global search, notification center, AI assistant, smart tables/forms, export/import, and other patterns expected on every Marpich page.

Product leadership mandated a complete per-page checklist so agents and developers do not ship minimal CRUD screens.

## Decision

Adopt **`docs/architecture/UI_PAGE_STANDARD.md`** defining:

- **App Shell** responsibilities (global widgets)
- **Page content** responsibilities (data UX patterns)
- Shared component library locations
- PR checklist with all 23 requirements

Enforce via **`.cursor/rules/marpich-ui-page-standard.mdc`** (`alwaysApply: true`).

Update `frontend/README.md` to reference the standard.

## Consequences

- All Next.js apps use `AppShell` from `frontend/core/shell/`
- Shared components built once in `frontend/shared/components/`
- Page PRs without checklist completion may be rejected

## Alternatives considered

- Fold into Engineering Quality Standard only — UI checklist is large enough for dedicated doc
- Per-app standards — rejected; one platform, one UI law
