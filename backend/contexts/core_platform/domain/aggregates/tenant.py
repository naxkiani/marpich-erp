"""Tenant aggregate — Core Platform bounded context."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId

from contexts.core_platform.domain.events.integration_events import (
    ModuleActivatedIntegration,
    TenantProvisionedIntegration,
    TenantSuspendedIntegration,
)


class TenantStatus(StrEnum):
    PROVISIONING = "provisioning"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    ARCHIVED = "archived"


class TenantTier(StrEnum):
    STARTER = "starter"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"


@dataclass(eq=False, kw_only=True)
class Tenant(AggregateRoot):
    slug: str
    name: str
    industry_pack: str
    tier: TenantTier = TenantTier.PROFESSIONAL
    status: TenantStatus = TenantStatus.PROVISIONING
    enabled_modules: list[str] = field(default_factory=list)
    locale: str = "en-US"
    timezone: str = "UTC"
    data_region: str = "us-east"
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def provision(
        cls,
        *,
        name: str,
        slug: str,
        industry_pack: str,
        enabled_modules: list[str],
        tier: TenantTier = TenantTier.PROFESSIONAL,
        locale: str = "en-US",
        timezone: str = "UTC",
        data_region: str = "us-east",
        correlation_id: str,
    ) -> tuple[Tenant, TenantProvisionedIntegration]:
        tenant = cls(
            id=UniqueId.generate(),
            slug=slug.strip().lower(),
            name=name.strip(),
            industry_pack=industry_pack,
            tier=tier,
            enabled_modules=sorted(set(enabled_modules)),
            locale=locale,
            timezone=timezone,
            data_region=data_region,
        )
        event = TenantProvisionedIntegration(
            tenant_id=TenantId.create(tenant.slug),
            correlation_id=correlation_id,
            tenant_slug=tenant.slug,
            name=tenant.name,
            industry_pack=tenant.industry_pack,
            enabled_modules=tuple(tenant.enabled_modules),
        )
        return tenant, event

    def activate(self) -> None:
        if self.status == TenantStatus.ARCHIVED:
            raise ValueError("Cannot activate archived tenant")
        self.status = TenantStatus.ACTIVE
        self.updated_at = datetime.now(UTC)

    def suspend(self, correlation_id: str) -> TenantSuspendedIntegration:
        self.status = TenantStatus.SUSPENDED
        self.updated_at = datetime.now(UTC)
        return TenantSuspendedIntegration(
            tenant_id=TenantId.create(self.slug),
            correlation_id=correlation_id,
            tenant_slug=self.slug,
        )

    def enable_module(self, module_id: str, correlation_id: str) -> ModuleActivatedIntegration | None:
        if module_id in self.enabled_modules:
            return None
        self.enabled_modules.append(module_id)
        self.enabled_modules.sort()
        self.updated_at = datetime.now(UTC)
        return ModuleActivatedIntegration(
            tenant_id=TenantId.create(self.slug),
            correlation_id=correlation_id,
            tenant_slug=self.slug,
            module_id=module_id,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "slug": self.slug,
            "name": self.name,
            "industry_pack": self.industry_pack,
            "tier": self.tier.value,
            "status": self.status.value,
            "enabled_modules": self.enabled_modules,
            "locale": self.locale,
            "timezone": self.timezone,
            "data_region": self.data_region,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
