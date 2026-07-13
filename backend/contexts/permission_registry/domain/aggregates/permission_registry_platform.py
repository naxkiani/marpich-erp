"""Permission Registry aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class RegistryCapability(StrEnum):
    PERMISSION_CATALOG = "permission_catalog"
    MODULE_REGISTRATION = "module_registration"
    ROLE_MANAGEMENT = "role_management"
    ROLE_BINDING = "role_binding"
    PERMISSION_SETS = "permission_sets"
    PRINCIPAL_RESOLUTION = "principal_resolution"
    NAMESPACE_GOVERNANCE = "namespace_governance"
    POLICY_DRIVEN_REGISTRY = "policy_driven_registry"
    REGISTRY_DASHBOARD = "registry_dashboard"
    REGISTRY_API = "registry_api"


class BindingScope(StrEnum):
    TENANT = "tenant"
    ORG = "org"
    BRANCH = "branch"


@dataclass(eq=False, kw_only=True)
class RegistryProfile(AggregateRoot):
    tenant_id: str
    profile_ref: str
    module_registration_enabled: bool = True
    custom_roles_enabled: bool = True
    binding_expiry_enabled: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(cls, *, tenant_id: str, profile_ref: str) -> RegistryProfile:
        return cls(id=UniqueId.generate(), tenant_id=tenant_id, profile_ref=profile_ref)

    def to_dict(self) -> dict:
        return {
            "profile_ref": self.profile_ref,
            "tenant_id": self.tenant_id,
            "module_registration_enabled": self.module_registration_enabled,
            "custom_roles_enabled": self.custom_roles_enabled,
            "binding_expiry_enabled": self.binding_expiry_enabled,
        }


@dataclass(eq=False, kw_only=True)
class Permission(AggregateRoot):
    code: str
    module: str
    resource: str
    action: str
    description: str
    is_system: bool = True
    registered_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(
        cls,
        *,
        code: str,
        module: str,
        resource: str,
        action: str,
        description: str,
        is_system: bool = True,
    ) -> Permission:
        return cls(
            id=UniqueId.generate(),
            code=code.lower(),
            module=module.lower(),
            resource=resource.lower(),
            action=action.lower(),
            description=description,
            is_system=is_system,
        )

    def to_dict(self) -> dict:
        return {
            "code": self.code,
            "module": self.module,
            "resource": self.resource,
            "action": self.action,
            "description": self.description,
            "is_system": self.is_system,
            "registered_at": self.registered_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class RegistryRole(AggregateRoot):
    tenant_id: str
    role_ref: str
    code: str
    name: str
    description: str
    permission_codes: list[str]
    is_system: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        role_ref: str,
        code: str,
        name: str,
        description: str,
        permission_codes: list[str],
        is_system: bool = False,
    ) -> RegistryRole:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            role_ref=role_ref,
            code=code.lower(),
            name=name,
            description=description,
            permission_codes=permission_codes,
            is_system=is_system,
        )

    def to_dict(self) -> dict:
        return {
            "role_ref": self.role_ref,
            "role_id": str(self.id),
            "tenant_id": self.tenant_id,
            "code": self.code,
            "name": self.name,
            "description": self.description,
            "permission_codes": self.permission_codes,
            "is_system": self.is_system,
        }


@dataclass(eq=False, kw_only=True)
class RoleBinding(AggregateRoot):
    tenant_id: str
    binding_ref: str
    principal_id: str
    role_id: str
    role_ref: str
    scope_type: str
    scope_id: str | None
    granted_by: str | None
    expires_at: datetime | None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def assign(
        cls,
        *,
        tenant_id: str,
        binding_ref: str,
        principal_id: str,
        role_id: str,
        role_ref: str,
        scope_type: str = "tenant",
        scope_id: str | None = None,
        granted_by: str | None = None,
        expires_at: datetime | None = None,
    ) -> RoleBinding:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            binding_ref=binding_ref,
            principal_id=principal_id,
            role_id=role_id,
            role_ref=role_ref,
            scope_type=scope_type,
            scope_id=scope_id,
            granted_by=granted_by,
            expires_at=expires_at,
        )

    def to_dict(self) -> dict:
        return {
            "binding_ref": self.binding_ref,
            "tenant_id": self.tenant_id,
            "principal_id": self.principal_id,
            "role_id": self.role_id,
            "role_ref": self.role_ref,
            "scope_type": self.scope_type,
            "scope_id": self.scope_id,
            "granted_by": self.granted_by,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class PermissionSet(AggregateRoot):
    tenant_id: str
    set_ref: str
    module: str
    name: str
    description: str
    permission_codes: list[str]
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        set_ref: str,
        module: str,
        name: str,
        description: str,
        permission_codes: list[str],
    ) -> PermissionSet:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            set_ref=set_ref,
            module=module.lower(),
            name=name,
            description=description,
            permission_codes=permission_codes,
        )

    def to_dict(self) -> dict:
        return {
            "set_ref": self.set_ref,
            "tenant_id": self.tenant_id,
            "module": self.module,
            "name": self.name,
            "description": self.description,
            "permission_codes": self.permission_codes,
        }
