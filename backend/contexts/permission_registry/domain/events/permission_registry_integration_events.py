"""Permission Registry integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent


@dataclass(frozen=True, kw_only=True)
class PermissionRegisteredIntegration(IntegrationEvent):
    module: str
    codes: list[str]

    @property
    def event_name(self) -> str:
        return "permission_registry.permission.registered"

    @property
    def source_context(self) -> str:
        return "permission_registry"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"module": self.module, "codes": self.codes}


@dataclass(frozen=True, kw_only=True)
class RoleCreatedIntegration(IntegrationEvent):
    role_ref: str
    code: str

    @property
    def event_name(self) -> str:
        return "permission_registry.role.created"

    @property
    def source_context(self) -> str:
        return "permission_registry"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"role_ref": self.role_ref, "code": self.code}


@dataclass(frozen=True, kw_only=True)
class RoleAssignedIntegration(IntegrationEvent):
    binding_ref: str
    principal_id: str
    role_ref: str

    @property
    def event_name(self) -> str:
        return "permission_registry.role.assigned"

    @property
    def source_context(self) -> str:
        return "permission_registry"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "binding_ref": self.binding_ref,
            "principal_id": self.principal_id,
            "role_ref": self.role_ref,
        }


@dataclass(frozen=True, kw_only=True)
class RegistryDashboardGeneratedIntegration(IntegrationEvent):
    permissions_total: int
    roles_total: int

    @property
    def event_name(self) -> str:
        return "permission_registry.dashboard.generated"

    @property
    def source_context(self) -> str:
        return "permission_registry"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"permissions_total": self.permissions_total, "roles_total": self.roles_total}
