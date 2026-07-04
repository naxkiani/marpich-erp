# ADR-015: Engineering Quality Standard

## Status

Accepted

## Context

The Platform Charter defines *what* Marpich is (one platform, modules extend Core). Engineering teams and AI agents also need explicit *how* standards for every line of code and every feature — observability, resilience, tests, accessibility, and i18n/RTL.

Product leadership mandated: no generated code or feature may skip enterprise qualities or the full operational/UI checklist.

## Decision

Adopt **`docs/architecture/ENGINEERING_QUALITY_STANDARD.md`** as mandatory for all code generation and PR review.

Enforce via **`.cursor/rules/marpich-engineering-quality.mdc`** (`alwaysApply: true`).

Include a copy-paste PR checklist in the standard document.

Link from [PLATFORM_CHARTER.md](../architecture/PLATFORM_CHARTER.md).

## Consequences

- Incomplete features (missing tests, tracing, audit, accessibility, etc.) are rejected at review
- Agents must verify Part A + Part B before marking tasks complete
- N/A items (e.g. dark mode on pure API-only change) must be explicitly noted in PR

## Alternatives considered

- Fold into Platform Charter only — document would become too long; split improves discoverability
- Rely on linter/CI only — cannot enforce accessibility, documentation, or AI-readiness automatically yet
