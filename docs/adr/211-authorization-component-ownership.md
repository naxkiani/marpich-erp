# ADR-211: Authorization Component Ownership — Rule Compiler, ReBAC, Cache

## Status

Accepted

## Context

Authorization PDP (ADR-182) evaluates ABAC conditions inline. Operators and APIs
need compile-time validation of `{attribute, operator, value}` without adopting
Cedar/Rego/OPA or duplicating Policy Engine business rules. Registry also claims
ReBAC and decision cache which were previously gaps.

## Decision

1. **Rule Compiler** lives inside `contexts/authorization` (`domain/services/rule_compiler.py`).
2. Supported operators: `eq|ne|in|not_in|gte|lte|gt|lt|matches`.
3. `create_abac_policy` and `POST /authorization/rules/compile` compile before persist/dry-run.
4. Runtime ABAC evaluation uses the same compiler evaluate path.
5. **ReBAC** uses tenant-scoped `RelationTuple` edges (`rebac_engine.py`); cascade order:
   `deny_override → rbac → rebac → abac → pbac → default`.
6. **Decision cache** is tenant-keyed TTL (`authz_decision_cache_backend=memory|redis`);
   invalidated on relation write/revoke and ABAC create.
7. Policy Engine remains owner of business outcomes; AuthZ remains owner of Permit/Deny.

## Consequences

- Invalid ABAC conditions fail closed at write time (`invalid_abac_conditions:*`).
- No new bounded context; no Cedar/Rego dependency.
- ReBAC allow can grant object access when RBAC permission is missing but a matching tuple exists.
- Redis cache falls back to memory when unavailable.
