# ADR-182: Enterprise Authorization PDP (Phase P1)

## Status

Accepted

## Context

Marpich defines authorization in ADR-009 and `SECURITY_STANDARD.md` as a separate plane from authentication, but only inline `require_permissions()` RBAC existed in `contexts/identity/`. There was no `POST /authorization/check` PDP for unified RBAC + ABAC + PBAC evaluation across Banking, Exchange, Tax, ERP, and industry modules.

## Decision

Implement **Authorization PDP** at `/api/v1/authorization` as bounded context `authorization`.

### 8 Platform Capabilities

1. RBAC Evaluation
2. ABAC Evaluation
3. PBAC Evaluation
4. Batch Check
5. Decision Simulation
6. Decision Audit
7. Policy-Driven PDP
8. Authorization Dashboard

### Aggregates

- `AuthorizationProfile`
- `AbacPolicy`
- `AccessDecision`

### Policy Keys

- `authorization.rbac.enabled`
- `authorization.abac.enabled`
- `authorization.pbac.enabled`
- `authorization.default_decision`
- `authorization.pbac.policy_key_prefix`

### Events

- `authorization.access.granted`
- `authorization.access.denied`
- `authorization.dashboard.generated`

### API Endpoints

- `POST /authorization/check` — single PDP decision
- `POST /authorization/check/batch` — batch decisions
- `POST /authorization/simulate` — what-if without audit record
- `GET /authorization/policies/abac` — tenant ABAC policies
- `GET /authorization/decisions` — decision audit trail

### Delegates

- Principal permissions → `identity`
- PBAC rules → `policy` (`IPolicyEvaluator`)

### Evaluation Order

`deny_override` → `rbac` → `abac` → `pbac` → `default_deny`

## Consequences

- Modules can call centralized PDP instead of duplicating authz logic
- ABAC policies stored in authorization context; PBAC delegates to policy engine
- Identity permission catalog extended with `authorization.*` permissions
- Phase P2: Permission Registry API; Phase P3: centralized frontend auth provider
