# ADR-021: Security Standard

## Status

Accepted

## Context

Platform Charter requires permissions and audit but did not consolidate security as mandatory, never-optional law with explicit support for RBAC, ABAC, JWT, OAuth2/OIDC, encryption algorithms, zero trust, sessions, threat detection, and rate limiting.

Product leadership mandated: security is not a feature flag.

## Decision

Adopt **`docs/architecture/SECURITY_STANDARD.md`** as canonical security law.

Enforce via **`.cursor/rules/marpich-security.mdc`** (`alwaysApply: true`).

Link from Platform Charter, Engineering Quality Standard, README.

## Consequences

- PRs without auth/authz on new routes are rejected
- Secret scanning and permission checks are review requirements
- OAuth2/OIDC and full ABAC PDP remain implementation work; contract is fixed now

## Alternatives considered

- Rely on identity context code only — insufficient for agents and reviewers
- Optional security for dev — rejected; use test tokens, not disabled auth
