# ADR-024: Chief Enterprise Architect Mandate

## Status

Accepted

## Context

Marpich documentation covered platform law, modules, security, and long-horizon scale, but did not establish a single **architect role** and **design-first** thinking model: capabilities and domains before CRUD, pages, or tables.

Agents defaulting to page/CRUD/table-first design violate DDD and the composable platform charter.

## Decision

Adopt **`docs/architecture/CHIEF_ARCHITECT_MANDATE.md`** as the governing architect mindset.

Enforce via **`.cursor/rules/marpich-chief-architect.mdc`** (`alwaysApply: true`) — highest-level design rule alongside Platform Charter.

Require architecture brief before implementation for non-trivial work.

## Consequences

- Agents identify as Chief Enterprise Architect when designing Marpich
- Implementation without architecture brief may be rejected at review
- Complements DEVELOPMENT_PROTOCOL (reuse) and LONG_HORIZON_ARCHITECTURE (time/scale)

## Alternatives considered

- Merge into DEVELOPMENT_PROTOCOL only — architect mandate deserves explicit role framing
- Implicit in DDD doc only — not enforced for agents at codegen time
