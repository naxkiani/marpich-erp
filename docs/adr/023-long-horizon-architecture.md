# ADR-023: Long-Horizon Architecture

## Status

Accepted

## Context

Marpich targets enterprise scale (millions of users, thousands of organizations, decades of evolution). Agents and developers often optimize for the immediate ticket, accumulating debt that violates the one-platform, multi-tenant, AI-first charter.

Product leadership mandated a long-horizon mindset: ten years, scale, AI evolution, extensibility — and explicitly forbade sacrificing architecture for speed.

## Decision

Adopt **`docs/architecture/LONG_HORIZON_ARCHITECTURE.md`** as the mindset standard for all code generation.

Enforce via **`.cursor/rules/marpich-long-horizon.mdc`** (`alwaysApply: true`).

Integrate with [DEVELOPMENT_PROTOCOL.md](../architecture/DEVELOPMENT_PROTOCOL.md) step 0.

## Consequences

- PRs should include long-horizon checklist when non-trivial
- Intentional debt requires ADR; silent shortcuts rejected at review
- Refactoring weak areas while touching them is expected

## Alternatives considered

- Implicit in Platform Charter only — not visible enough to agents at codegen time
- Post-launch refactor policy — rejected; debt at scale is too expensive
