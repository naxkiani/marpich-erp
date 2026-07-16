"""Permission Registry application service."""
from __future__ import annotations

import uuid

from contexts.identity.infrastructure.persistence.memory_store import PERMISSION_CODES
from contexts.permission_registry.domain.aggregates.permission_registry_platform import (
    Permission,
    PermissionSet,
    RegistryProfile,
    RegistryRole,
    RoleBinding,
)
from contexts.permission_registry.domain.events.permission_registry_integration_events import (
    PermissionRegisteredIntegration,
    RegistryDashboardGeneratedIntegration,
    RoleAssignedIntegration,
    RoleCreatedIntegration,
)
from contexts.permission_registry.domain.ports.permission_registry_repositories import (
    IIdentityRegistryPort,
    IPermissionRepository,
    IPermissionSetRepository,
    IRegistryProfileRepository,
    IRegistryRoleRepository,
    IRoleBindingRepository,
)
from contexts.permission_registry.domain.services import permission_registry_engine as engine
from shared.application.ports.policy import IPolicyEvaluator
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class PermissionRegistryApplicationService:
    def __init__(
        self,
        profiles: IRegistryProfileRepository,
        permissions: IPermissionRepository,
        roles: IRegistryRoleRepository,
        bindings: IRoleBindingRepository,
        permission_sets: IPermissionSetRepository,
        identity: IIdentityRegistryPort,
        policy_evaluator: IPolicyEvaluator,
    ) -> None:
        self._profiles = profiles
        self._permissions = permissions
        self._roles = roles
        self._bindings = bindings
        self._permission_sets = permission_sets
        self._identity = identity
        self._policy = policy_evaluator

    async def _policy_params(self, tenant_id: str) -> dict:
        profile = await self._profiles.find_by_tenant(tenant_id)
        params = {
            "module_registration_enabled": profile.module_registration_enabled if profile else True,
            "custom_roles_enabled": profile.custom_roles_enabled if profile else True,
            "binding_expiry_enabled": profile.binding_expiry_enabled if profile else True,
        }
        pmap = {
            "permission_registry.module_registration.enabled": ("module_registration_enabled", "enabled"),
            "permission_registry.custom_roles.enabled": ("custom_roles_enabled", "enabled"),
            "permission_registry.binding.expiry.enabled": ("binding_expiry_enabled", "enabled"),
        }
        for key, (target, field) in pmap.items():
            decision = await self._policy.evaluate(tenant_id=tenant_id, domain="platform", policy_key=key, facts={})
            if decision.parameters and field in decision.parameters:
                params[target] = decision.parameters[field]
        return params

    async def _ensure_profile(self, tenant_id: str) -> RegistryProfile:
        profile = await self._profiles.find_by_tenant(tenant_id)
        if profile:
            return profile
        profile = RegistryProfile.create(
            tenant_id=tenant_id,
            profile_ref=self._profiles.next_profile_ref(tenant_id),
        )
        await self._profiles.save(profile)
        return profile

    async def _bootstrap_system_permissions(self) -> None:
        for code in PERMISSION_CODES:
            if await self._permissions.find_by_code(code):
                continue
            parsed = engine.parse_permission_code(code)
            if not parsed:
                continue
            module, resource, action = parsed
            permission = Permission.register(
                code=code,
                module=module,
                resource=resource,
                action=action,
                description=f"System permission {code}",
                is_system=True,
            )
            await self._permissions.save(permission)

    async def handle_tenant_provisioned(self, event: dict) -> None:
        tenant_id = event.get("tenant_id") or event.get("payload", {}).get("tenant_id")
        if tenant_id:
            await self.seed(tenant_id)

    async def list_catalog(self) -> Result[dict]:
        await self._bootstrap_system_permissions()
        return Result.ok({
            "capabilities": engine.list_capability_catalog(),
            "policy_keys": engine.list_policy_keys(),
            "permission_pattern": "^[a-z][a-z0-9_]*\\.[a-z][a-z0-9_]*\\.[a-z][a-z0-9_.]*$",
            "delegation": {"role_sync": "identity", "pdp_consumer": "authorization"},
        })

    async def get_dependency_map(self) -> Result[dict]:
        return Result.ok(engine.dependency_map())

    async def seed(self, tenant_id: str) -> Result[dict]:
        await self._ensure_profile(tenant_id)
        await self._bootstrap_system_permissions()
        seed_data = engine.generate_seed_data()

        registered = 0
        for pdata in seed_data["permissions"]:
            if await self._permissions.find_by_code(pdata["code"]):
                continue
            parsed = engine.parse_permission_code(pdata["code"])
            if not parsed:
                continue
            module, resource, action = parsed
            permission = Permission.register(
                code=pdata["code"],
                module=module,
                resource=resource,
                action=action,
                description=pdata.get("description", ""),
                is_system=False,
            )
            await self._permissions.save(permission)
            registered += 1

        roles_created = 0
        for rdata in seed_data["roles"]:
            if await self._roles.find_by_code(tenant_id, rdata["code"]):
                continue
            result = await self.create_role(
                tenant_id,
                code=rdata["code"],
                name=rdata["name"],
                description=rdata.get("description", ""),
                permission_codes=rdata["permission_codes"],
            )
            if result.succeeded:
                roles_created += 1

        sets_created = 0
        for sdata in seed_data["permission_sets"]:
            result = await self.create_permission_set(
                tenant_id,
                module=sdata["module"],
                name=sdata["name"],
                description=sdata.get("description", ""),
                permission_codes=sdata["permission_codes"],
            )
            if result.succeeded:
                sets_created += 1

        return Result.ok({
            "seeded": True,
            "permissions_registered": registered,
            "roles": roles_created,
            "permission_sets": sets_created,
        })

    async def get_dashboard(self, tenant_id: str) -> Result[dict]:
        await self._bootstrap_system_permissions()
        profile = await self._profiles.find_by_tenant(tenant_id)
        permissions = [p.to_dict() for p in await self._permissions.list_all()]
        roles = [r.to_dict() for r in await self._roles.list_by_tenant(tenant_id)]
        bindings = [b.to_dict() for b in await self._bindings.list_by_tenant(tenant_id)]
        sets = [s.to_dict() for s in await self._permission_sets.list_by_tenant(tenant_id)]
        dashboard = engine.build_dashboard(
            profile=profile.to_dict() if profile else None,
            permissions=permissions,
            roles=roles,
            bindings=bindings,
            sets=sets,
        )
        await publish_integration_event(
            RegistryDashboardGeneratedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=str(uuid.uuid4()),
                permissions_total=dashboard["summary"]["permissions"],
                roles_total=dashboard["summary"]["roles"],
            )
        )
        return Result.ok(dashboard)

    async def list_permissions(self, *, module: str | None = None) -> Result[list[dict]]:
        await self._bootstrap_system_permissions()
        permissions = await self._permissions.list_all(module=module)
        return Result.ok([p.to_dict() for p in permissions])

    async def register_permissions(
        self,
        tenant_id: str,
        *,
        module: str,
        permissions: list[dict],
    ) -> Result[dict]:
        policy = await self._policy_params(tenant_id)
        if not policy["module_registration_enabled"]:
            return Result.fail("module_registration_disabled")
        codes = [p.get("code", "") for p in permissions]
        valid, invalid = engine.validate_permission_codes(codes)
        if invalid:
            return Result.fail(f"invalid_permission_codes:{','.join(invalid)}")

        created: list[str] = []
        for pdata in permissions:
            code = pdata["code"].lower()
            if await self._permissions.find_by_code(code):
                continue
            parsed = engine.parse_permission_code(code)
            if not parsed:
                continue
            mod, resource, action = parsed
            if mod != module.lower():
                return Result.fail(f"module_mismatch:{code}")
            permission = Permission.register(
                code=code,
                module=mod,
                resource=resource,
                action=action,
                description=pdata.get("description", ""),
                is_system=False,
            )
            await self._permissions.save(permission)
            created.append(code)

        if created:
            await publish_integration_event(
                PermissionRegisteredIntegration(
                    tenant_id=TenantId(tenant_id),
                    correlation_id=str(uuid.uuid4()),
                    module=module.lower(),
                    codes=created,
                )
            )
        return Result.ok({"registered": created, "count": len(created)})

    async def list_roles(self, tenant_id: str) -> Result[list[dict]]:
        roles = await self._roles.list_by_tenant(tenant_id)
        return Result.ok([r.to_dict() for r in roles])

    async def create_role(
        self,
        tenant_id: str,
        *,
        code: str,
        name: str,
        description: str = "",
        permission_codes: list[str],
    ) -> Result[dict]:
        policy = await self._policy_params(tenant_id)
        if not policy["custom_roles_enabled"] and code.lower() != "admin":
            return Result.fail("custom_roles_disabled")

        await self._bootstrap_system_permissions()
        catalog = {p.code for p in await self._permissions.list_all()}
        ok, missing = engine.validate_role_permissions(permission_codes, catalog)
        if not ok:
            return Result.fail(f"unknown_permissions:{','.join(missing)}")

        if await self._roles.find_by_code(tenant_id, code):
            return Result.fail("role_code_exists")

        role = RegistryRole.create(
            tenant_id=tenant_id,
            role_ref=self._roles.next_role_ref(tenant_id),
            code=code,
            name=name,
            description=description,
            permission_codes=[c.lower() for c in permission_codes],
        )
        await self._roles.save(role)
        await self._identity.sync_role(
            tenant_id,
            role_id=str(role.id),
            code=role.code,
            name=role.name,
            permission_codes=role.permission_codes,
            is_system=role.is_system,
        )
        await publish_integration_event(
            RoleCreatedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=str(uuid.uuid4()),
                role_ref=role.role_ref,
                code=role.code,
            )
        )
        return Result.ok(role.to_dict())

    async def get_role(self, tenant_id: str, role_ref: str) -> Result[dict]:
        role = await self._roles.find_by_ref(tenant_id, role_ref)
        if not role:
            return Result.fail("role_not_found")
        return Result.ok(role.to_dict())

    async def assign_role(
        self,
        tenant_id: str,
        *,
        role_ref: str,
        principal_id: str,
        scope_type: str = "tenant",
        scope_id: str | None = None,
        granted_by: str | None = None,
        expires_at=None,
    ) -> Result[dict]:
        role = await self._roles.find_by_ref(tenant_id, role_ref)
        if not role:
            return Result.fail("role_not_found")
        if not await self._identity.principal_exists(tenant_id, principal_id):
            return Result.fail("principal_not_found")

        binding = RoleBinding.assign(
            tenant_id=tenant_id,
            binding_ref=self._bindings.next_binding_ref(tenant_id),
            principal_id=principal_id,
            role_id=str(role.id),
            role_ref=role.role_ref,
            scope_type=scope_type,
            scope_id=scope_id,
            granted_by=granted_by,
            expires_at=expires_at,
        )
        await self._bindings.save(binding)
        await self._identity.assign_role_to_principal(tenant_id, principal_id, str(role.id))
        await publish_integration_event(
            RoleAssignedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=str(uuid.uuid4()),
                binding_ref=binding.binding_ref,
                principal_id=principal_id,
                role_ref=role.role_ref,
            )
        )
        return Result.ok(binding.to_dict())

    async def revoke_binding(self, tenant_id: str, binding_ref: str) -> Result[dict]:
        binding = await self._bindings.find_by_ref(tenant_id, binding_ref)
        if not binding:
            return Result.fail("binding_not_found")
        await self._identity.revoke_role_from_principal(tenant_id, binding.principal_id, binding.role_id)
        await self._bindings.delete(tenant_id, binding_ref)
        return Result.ok({"revoked": True, "binding_ref": binding_ref})

    async def list_bindings(self, tenant_id: str, *, principal_id: str | None = None) -> Result[list[dict]]:
        if principal_id:
            bindings = await self._bindings.list_by_principal(tenant_id, principal_id)
        else:
            bindings = await self._bindings.list_by_tenant(tenant_id)
        return Result.ok([b.to_dict() for b in bindings])

    async def create_permission_set(
        self,
        tenant_id: str,
        *,
        module: str,
        name: str,
        description: str = "",
        permission_codes: list[str],
    ) -> Result[dict]:
        await self._bootstrap_system_permissions()
        catalog = {p.code for p in await self._permissions.list_all()}
        ok, missing = engine.validate_role_permissions(permission_codes, catalog)
        if not ok:
            return Result.fail(f"unknown_permissions:{','.join(missing)}")

        permission_set = PermissionSet.create(
            tenant_id=tenant_id,
            set_ref=self._permission_sets.next_set_ref(tenant_id),
            module=module,
            name=name,
            description=description,
            permission_codes=[c.lower() for c in permission_codes],
        )
        await self._permission_sets.save(permission_set)
        return Result.ok(permission_set.to_dict())

    async def list_permission_sets(self, tenant_id: str) -> Result[list[dict]]:
        sets = await self._permission_sets.list_by_tenant(tenant_id)
        return Result.ok([s.to_dict() for s in sets])

    async def resolve_principal_permissions(self, tenant_id: str, principal_id: str) -> Result[dict]:
        bindings = await self._bindings.list_by_principal(tenant_id, principal_id)
        perms: set[str] = set()
        role_codes: list[str] = []
        for binding in bindings:
            role = await self._roles.find_by_ref(tenant_id, binding.role_ref)
            if not role:
                continue
            role_codes.append(role.code)
            if "*" in role.permission_codes:
                return Result.ok({"principal_id": principal_id, "permissions": ["*"], "roles": role_codes})
            perms.update(role.permission_codes)
        return Result.ok({
            "principal_id": principal_id,
            "permissions": sorted(perms),
            "roles": role_codes,
        })
