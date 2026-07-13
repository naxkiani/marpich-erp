"""Identity sync adapter for Permission Registry."""
from __future__ import annotations

from contexts.identity.domain.aggregates.role import Role
from contexts.identity.infrastructure.persistence.memory_store import InMemoryRoleRepository, InMemoryUserRepository
from contexts.permission_registry.domain.ports.permission_registry_repositories import IIdentityRegistryPort
from shared.domain.value_objects.unique_id import UniqueId


class IdentityRegistryAdapter(IIdentityRegistryPort):
    def __init__(self) -> None:
        self._roles = InMemoryRoleRepository()
        self._users = InMemoryUserRepository()

    async def sync_role(
        self,
        tenant_id: str,
        *,
        role_id: str,
        code: str,
        name: str,
        permission_codes: list[str],
        is_system: bool,
    ) -> None:
        existing = await self._roles.find_by_code(tenant_id, code)
        if existing:
            existing.name = name
            existing.permission_ids = permission_codes
            existing.is_system = is_system
            await self._roles.save(existing)
            return
        role = Role(
            id=UniqueId.from_string(role_id),
            tenant_id=tenant_id,
            code=code,
            name=name,
            description=name,
            is_system=is_system,
            permission_ids=permission_codes,
        )
        await self._roles.save(role)

    async def assign_role_to_principal(self, tenant_id: str, principal_id: str, role_id: str) -> None:
        user = await self._users.find_by_id(tenant_id, UniqueId.from_string(principal_id))
        if not user:
            return
        if role_id not in user.role_ids:
            user.role_ids.append(role_id)
            await self._users.save(user)

    async def revoke_role_from_principal(self, tenant_id: str, principal_id: str, role_id: str) -> None:
        user = await self._users.find_by_id(tenant_id, UniqueId.from_string(principal_id))
        if not user:
            return
        if role_id in user.role_ids:
            user.role_ids.remove(role_id)
            await self._users.save(user)

    async def principal_exists(self, tenant_id: str, principal_id: str) -> bool:
        user = await self._users.find_by_id(tenant_id, UniqueId.from_string(principal_id))
        return user is not None
