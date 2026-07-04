"""Core Platform application service."""
from __future__ import annotations

import json
import re
from datetime import UTC, datetime

from contexts.core_platform.domain.aggregates.tenant import Tenant, TenantTier
from contexts.core_platform.domain.ports.repositories import ITenantRepository
from shared.application.result import Result
from shared.contracts.industry_packs import (
    get_industry_pack,
    list_industry_packs,
    resolve_modules_for_pack,
)
from shared.infrastructure.messaging.event_bus import publish_integration_event

_SLUG_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{1,62}[a-z0-9]$")


class ConsolePlatformAudit:
    async def log(self, **kwargs: object) -> None:
        entry = {"type": "audit", "context": "core_platform", **kwargs, "occurred_at": datetime.now(UTC).isoformat()}
        print(json.dumps(entry, default=str))


class CorePlatformApplicationService:
    def __init__(
        self,
        tenants: ITenantRepository,
        audit: ConsolePlatformAudit | None = None,
    ) -> None:
        self._tenants = tenants
        self._audit = audit or ConsolePlatformAudit()

    async def list_industry_packs(self) -> Result[list[dict]]:
        return Result.ok([p.to_dict() for p in list_industry_packs()])

    async def get_industry_pack(self, pack_id: str) -> Result[dict]:
        pack = get_industry_pack(pack_id)
        if not pack:
            return Result.fail("platform.errors.unknown_industry_pack")
        data = pack.to_dict()
        data["all_modules"] = resolve_modules_for_pack(pack_id)
        return Result.ok(data)

    async def provision_tenant(
        self,
        *,
        name: str,
        slug: str,
        industry_pack: str,
        correlation_id: str,
        tier: str = "professional",
        optional_modules: list[str] | None = None,
        locale: str | None = None,
        timezone: str = "UTC",
        data_region: str = "us-east",
    ) -> Result[dict]:
        pack = get_industry_pack(industry_pack)
        if not pack:
            return Result.fail("platform.errors.unknown_industry_pack")

        normalized_slug = slug.strip().lower()
        if not _SLUG_PATTERN.match(normalized_slug):
            return Result.fail("platform.errors.invalid_slug")

        if await self._tenants.exists_by_slug(normalized_slug):
            return Result.fail("platform.errors.slug_exists")

        try:
            tenant_tier = TenantTier(tier)
        except ValueError:
            return Result.fail("platform.errors.invalid_tier")

        enabled_modules = resolve_modules_for_pack(industry_pack, optional_modules)
        tenant, event = Tenant.provision(
            name=name,
            slug=normalized_slug,
            industry_pack=industry_pack,
            enabled_modules=enabled_modules,
            tier=tenant_tier,
            locale=locale or pack.default_locale,
            timezone=timezone,
            data_region=data_region,
            correlation_id=correlation_id,
        )
        tenant.activate()
        await self._tenants.save(tenant)
        await publish_integration_event(event)

        await self._audit.log(
            tenant_id=tenant.slug,
            correlation_id=correlation_id,
            action="platform.tenant.provisioned",
            resource_type="tenant",
            resource_id=str(tenant.id),
            payload={"slug": tenant.slug, "industry_pack": industry_pack},
        )
        return Result.ok(tenant.to_dict())

    async def get_tenant(self, slug: str) -> Result[dict]:
        tenant = await self._tenants.find_by_slug(slug.strip().lower())
        if not tenant:
            return Result.fail("platform.errors.tenant_not_found")
        return Result.ok(tenant.to_dict())

    async def list_tenants(self) -> Result[list[dict]]:
        tenants = await self._tenants.list_tenants()
        return Result.ok([t.to_dict() for t in tenants])

    async def suspend_tenant(self, slug: str, correlation_id: str) -> Result[dict]:
        tenant = await self._tenants.find_by_slug(slug.strip().lower())
        if not tenant:
            return Result.fail("platform.errors.tenant_not_found")
        if tenant.status.value == "archived":
            return Result.fail("platform.errors.tenant_archived")

        event = tenant.suspend(correlation_id)
        await self._tenants.save(tenant)
        await publish_integration_event(event)

        await self._audit.log(
            tenant_id=tenant.slug,
            correlation_id=correlation_id,
            action="platform.tenant.suspended",
            resource_type="tenant",
            resource_id=str(tenant.id),
        )
        return Result.ok(tenant.to_dict())

    async def activate_module(
        self,
        slug: str,
        module_id: str,
        correlation_id: str,
    ) -> Result[dict]:
        tenant = await self._tenants.find_by_slug(slug.strip().lower())
        if not tenant:
            return Result.fail("platform.errors.tenant_not_found")

        pack = get_industry_pack(tenant.industry_pack)
        if not pack:
            return Result.fail("platform.errors.unknown_industry_pack")

        allowed = set(pack.required_modules) | set(pack.optional_modules)
        if module_id not in allowed:
            return Result.fail("platform.errors.module_not_in_pack")

        event = tenant.enable_module(module_id, correlation_id)
        if event is None:
            return Result.ok(tenant.to_dict())

        await self._tenants.save(tenant)
        await publish_integration_event(event)

        await self._audit.log(
            tenant_id=tenant.slug,
            correlation_id=correlation_id,
            action="platform.module.activated",
            resource_type="module",
            resource_id=module_id,
        )
        return Result.ok(tenant.to_dict())
