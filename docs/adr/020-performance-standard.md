# ADR-020: Performance Standard

## Status

Accepted

## Context

Engineering Quality Standard lists "Performance Optimization" but did not codify concrete mandatory rules (N+1, pagination, Redis, async, indexes, streaming). Agents and developers need explicit always-on performance law.

Product leadership mandated: always optimize; never load unnecessary data; standard patterns for backend and frontend.

## Decision

Adopt **`docs/architecture/PERFORMANCE_STANDARD.md`** with 13 mandatory rules and PR checklist.

Enforce via **`.cursor/rules/marpich-performance.mdc`** (`alwaysApply: true`).

Link from Engineering Quality Standard and README.

## Consequences

- New list APIs without pagination may be rejected
- PRs should document query plans / indexes for new hot paths
- Heavy work must use background workers, not synchronous HTTP

## Alternatives considered

- Rely on lint/tools only — insufficient until automated N+1 detection exists
- Fold into Engineering Quality only — performance rules deserve dedicated doc
