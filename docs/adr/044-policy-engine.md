# ADR-044: Enterprise Policy Engine — Configurable Business Rules

## Status

Accepted

## Context

Business modules must enforce industry-specific rules: university grading, hospital admission, bank lending limits, exchange margin, tax rates, construction safety, government procurement thresholds. Hardcoding these in module code prevents tenant customization, regulatory updates without deploys, and audit-ready change control.

Authorization Service (Identity PDP) answers access control — *may* a user act. It does not replace configurable business rule evaluation.

Settings Service holds tenant preferences — not versioned regulatory policy with approval lifecycle.

## Decision

Adopt **`docs/architecture/ENTERPRISE_POLICY_ENGINE.md`** as canonical policy law.

### Core principles

- Policies are **configurable** — no hardcoded business rules in modules
- Every module reads policies via **`POST /policies/evaluate`** through `IPolicyEvaluator` port
- Full lifecycle: **versioning, effective date, expiration, priority, conditions, exceptions, approval, testing, simulation, rollback**

### Industry domains

University, hospital, bank, exchange, tax, construction, government — seeded from industry packs.

### Separation

| Service | Role |
|---------|------|
| Authorization (Identity) | RBAC/ABAC access |
| Settings | Tenant preferences |
| **Policy Engine** | Versioned business rules |

Policy publish approval uses Workflow Engine; changes audited via Audit Platform.

## Consequences

- New bounded context `contexts/policy/` (planned)
- Modules migrate hardcoded thresholds to policy keys
- CI contract tests for seeded policy packs
- `shared/application/ports/policy.py` port for DI

## Alternatives considered

- Rules in Settings JSON — rejected (no versioning/approval/rollback)
- Module-local rule tables — rejected (fragmentation, no simulation)
- Extend Authorization ABAC only — rejected (mixes access with business outcomes)
