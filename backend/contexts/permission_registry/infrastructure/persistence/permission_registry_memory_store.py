"""In-memory Permission Registry persistence."""
from __future__ import annotations

from contexts.permission_registry.domain.aggregates.permission_registry_platform import (
    Permission,
    PermissionSet,
    RegistryProfile,
    RegistryRole,
    RoleBinding,
)
from contexts.permission_registry.domain.ports.permission_registry_repositories import (
    IPermissionRepository,
    IPermissionSetRepository,
    IRegistryProfileRepository,
    IRegistryRoleRepository,
    IRoleBindingRepository,
)


class _RefCounter:
    _counters: dict[str, int] = {}

    @classmethod
    def reset(cls) -> None:
        cls._counters = {}

    @classmethod
    def next(cls, tenant_id: str, prefix: str) -> str:
        key = f"{tenant_id}:{prefix}"
        n = cls._counters.get(key, 0) + 1
        cls._counters[key] = n
        return f"{prefix}-{tenant_id[:4].upper()}-{n:05d}"


class InMemoryRegistryProfileRepository(IRegistryProfileRepository):
    _store: dict[str, RegistryProfile] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, profile: RegistryProfile) -> None:
        self._store[str(profile.id)] = profile

    async def find_by_tenant(self, tenant_id: str) -> RegistryProfile | None:
        for profile in self._store.values():
            if profile.tenant_id == tenant_id:
                return profile
        return None

    def next_profile_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-PRM-PRF")


class InMemoryPermissionRepository(IPermissionRepository):
    _store: dict[str, Permission] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, permission: Permission) -> None:
        self._store[permission.code] = permission

    async def find_by_code(self, code: str) -> Permission | None:
        return self._store.get(code.lower())

    async def list_all(self, *, module: str | None = None) -> list[Permission]:
        items = list(self._store.values())
        if module:
            items = [p for p in items if p.module == module.lower()]
        return sorted(items, key=lambda p: p.code)


class InMemoryRegistryRoleRepository(IRegistryRoleRepository):
    _store: dict[str, RegistryRole] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, role: RegistryRole) -> None:
        self._store[str(role.id)] = role

    async def find_by_ref(self, tenant_id: str, role_ref: str) -> RegistryRole | None:
        for role in self._store.values():
            if role.tenant_id == tenant_id and role.role_ref == role_ref:
                return role
        return None

    async def find_by_code(self, tenant_id: str, code: str) -> RegistryRole | None:
        for role in self._store.values():
            if role.tenant_id == tenant_id and role.code == code.lower():
                return role
        return None

    async def list_by_tenant(self, tenant_id: str) -> list[RegistryRole]:
        return [r for r in self._store.values() if r.tenant_id == tenant_id]

    def next_role_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-PRM-ROL")


class InMemoryRoleBindingRepository(IRoleBindingRepository):
    _store: dict[str, RoleBinding] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, binding: RoleBinding) -> None:
        self._store[str(binding.id)] = binding

    async def find_by_ref(self, tenant_id: str, binding_ref: str) -> RoleBinding | None:
        for binding in self._store.values():
            if binding.tenant_id == tenant_id and binding.binding_ref == binding_ref:
                return binding
        return None

    async def list_by_tenant(self, tenant_id: str) -> list[RoleBinding]:
        return [b for b in self._store.values() if b.tenant_id == tenant_id]

    async def list_by_principal(self, tenant_id: str, principal_id: str) -> list[RoleBinding]:
        return [
            b for b in self._store.values()
            if b.tenant_id == tenant_id and b.principal_id == principal_id
        ]

    async def delete(self, tenant_id: str, binding_ref: str) -> bool:
        for key, binding in list(self._store.items()):
            if binding.tenant_id == tenant_id and binding.binding_ref == binding_ref:
                del self._store[key]
                return True
        return False

    def next_binding_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-PRM-BND")


class InMemoryPermissionSetRepository(IPermissionSetRepository):
    _store: dict[str, PermissionSet] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, permission_set: PermissionSet) -> None:
        self._store[str(permission_set.id)] = permission_set

    async def list_by_tenant(self, tenant_id: str) -> list[PermissionSet]:
        return [s for s in self._store.values() if s.tenant_id == tenant_id]

    def next_set_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-PRM-SET")
