# ADR-183: Enterprise Permission Registry (Phase P2)

## Status

Accepted

## Context

Phase P1 delivered Authorization PDP at `/api/v1/authorization`, but permissions were hardcoded in `identity` memory store with no module registration API, role management endpoints, or role binding lifecycle. Route registry listed `/api/v1/permissions` under identity without implementation.

## Decision

Implement **Permission Registry** at `/api/v1/permissions` as bounded context `permission_registry`.

### 10 Platform Capabilities

1. Permission Catalog
2. Module Registration
3. Role Management
4. Role Binding
5. Permission Sets
6. Principal Resolution
7. Namespace Governance
8. Policy-Driven Registry
9. Registry Dashboard
10. Registry API

### Aggregates

- `RegistryProfile`
- `Permission`
- `RegistryRole`
- `RoleBinding`
- `PermissionSet`

### Policy Keys

- `permission_registry.module_registration.enabled`
- `permission_registry.custom_roles.enabled`
- `permission_registry.binding.expiry.enabled`

### Events

- `permission_registry.permission.registered`
- `permission_registry.role.created`
- `permission_registry.role.assigned`
- `permission_registry.dashboard.generated`

### API Endpoints

- `GET /permissions` — list catalog (filter by module)
- `POST /permissions/register` — register module permissions
- `GET|POST /permissions/roles` — role management
- `POST /permissions/roles/{ref}/bindings` — assign role to principal
- `DELETE /permissions/role-bindings/{ref}` — revoke binding
- `GET|POST /permissions/sets` — permission bundles
- `GET /permissions/principals/{id}/permissions` — resolve effective permissions

### Delegates

- Role sync + principal bindings → `identity` (InMemoryRoleRepository / User.role_ids)
- PDP consumers → `authorization`

## Consequences

- Modules register `module.resource.action` permissions without code changes
- Roles and bindings sync to identity for JWT permission resolution
- System permissions bootstrapped from identity `PERMISSION_CODES`
- Phase P3: centralized `@marpich/auth-provider` frontend
