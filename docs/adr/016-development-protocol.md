# ADR-016: Development Protocol — Analyze and Reuse Before Code

## Status

Accepted

## Context

Platform Charter forbids duplication; Engineering Quality Standard lists what every feature must include. Neither document prescribed a mandatory **pre-code workflow** for agents and developers: systematic discovery, reuse analysis, architecture improvement before features, and explicit decision documentation.

Without this, new code often reimplements existing services, APIs, events, and permissions.

## Decision

Adopt **`docs/architecture/DEVELOPMENT_PROTOCOL.md`** as mandatory step zero before any implementation.

Enforce via **`.cursor/rules/marpich-development-protocol.mdc`** (`alwaysApply: true`).

Require reuse analysis and architectural decision explanation in PRs and agent responses.

Link from Platform Charter, Engineering Quality Standard, and README.

## Consequences

- Feature PRs without reuse analysis may be rejected
- Agents must search registry, routers, event catalog, and shared infra before creating new artifacts
- Weak patterns must be refactored before extension (or documented as a separate improvement task)

## Alternatives considered

- Merge into Platform Charter — charter already long; dedicated protocol improves discoverability
- CI-only enforcement — cannot automate "did you read context map" without rule + review culture
