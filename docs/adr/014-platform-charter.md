# ADR-014: Platform Charter

## Status

Accepted

## Context

Marpich targets 25+ industries on one codebase. Without explicit non-negotiable laws, teams and AI agents risk building parallel auth stacks, audit tables, notification senders, and industry-specific APIs — recreating the multi-product ERP antipattern.

Product leadership defined a canonical charter: one platform, modules extend Core, never duplicate cross-cutting concerns, every feature supports configuration, plugins, AI, audit, permissions, localization, multi-currency, multi-language, and multi-tenancy.

## Decision

Adopt **`docs/architecture/PLATFORM_CHARTER.md`** as the single source of truth for product and architecture law.

Enforce for agents via **`.cursor/rules/marpich-platform-charter.mdc`** (`alwaysApply: true`).

Link from `README.md` and `docs/architecture/OVERVIEW.md`.

## Consequences

- New modules must pass charter checklist before merge
- Duplication of Core capabilities is a design review rejection
- Charter updates require explicit ADR amendment or new ADR

## Alternatives considered

- Rely on ADR-005 alone — insufficient detail for day-to-day enforcement
- Wiki-only documentation — not visible to Cursor agents without a rule file
