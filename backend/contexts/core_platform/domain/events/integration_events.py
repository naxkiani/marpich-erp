"""Core Platform integration events."""
from __future__ import annotations

from dataclasses import dataclass, field

from shared.domain.events.integration_event import IntegrationEvent
from shared.domain.value_objects.tenant_id import TenantId


@dataclass(frozen=True, kw_only=True)
class TenantProvisionedIntegration(IntegrationEvent):
    tenant_slug: str
    name: str
    industry_pack: str
    enabled_modules: tuple[str, ...] = field(default_factory=tuple)

    @property
    def event_name(self) -> str:
        return "platform.tenant.provisioned"

    @property
    def source_context(self) -> str:
        return "core_platform"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "tenant_slug": self.tenant_slug,
            "name": self.name,
            "industry_pack": self.industry_pack,
            "enabled_modules": list(self.enabled_modules),
        }


@dataclass(frozen=True, kw_only=True)
class ModuleActivatedIntegration(IntegrationEvent):
    tenant_slug: str
    module_id: str

    @property
    def event_name(self) -> str:
        return "platform.module.activated"

    @property
    def source_context(self) -> str:
        return "core_platform"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "tenant_slug": self.tenant_slug,
            "module_id": self.module_id,
        }


@dataclass(frozen=True, kw_only=True)
class TenantSuspendedIntegration(IntegrationEvent):
    tenant_slug: str

    @property
    def event_name(self) -> str:
        return "platform.tenant.suspended"

    @property
    def source_context(self) -> str:
        return "core_platform"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"tenant_slug": self.tenant_slug}


def platform_tenant_id(slug: str) -> TenantId:
    return TenantId.create(slug)
