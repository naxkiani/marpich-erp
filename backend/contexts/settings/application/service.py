"""Settings application service."""
from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any

from contexts.settings.application.commands.merge_module_config import MergeModuleConfigCommand
from contexts.settings.application.commands.seed_tenant_settings import SeedTenantSettingsCommand
from contexts.settings.application.constants.module_defaults import MODULE_DEFAULTS
from contexts.settings.application.ports.platform_events import IPlatformSettingsAdapter
from contexts.settings.domain.aggregates.tenant_settings import TenantSettings
from contexts.settings.domain.events.integration_events import (
    ConfigUpdatedIntegration,
    FeatureToggledIntegration,
)
from contexts.settings.domain.ports.repositories import ITenantSettingsRepository
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class ConsoleSettingsAudit:
    async def log(self, **kwargs: object) -> None:
        entry = {"type": "audit", "context": "settings", **kwargs, "occurred_at": datetime.now(UTC).isoformat()}
        print(json.dumps(entry, default=str))


class SettingsApplicationService:
    def __init__(
        self,
        settings: ITenantSettingsRepository,
        platform_events: IPlatformSettingsAdapter,
        audit: ConsoleSettingsAudit | None = None,
    ) -> None:
        self._settings = settings
        self._platform_events = platform_events
        self._audit = audit or ConsoleSettingsAudit()

    async def handle_tenant_provisioned(self, envelope: dict) -> None:
        command = await self._platform_events.parse_tenant_provisioned(envelope)
        await self.seed_tenant_settings(command)

    async def handle_module_activated(self, envelope: dict) -> None:
        command = await self._platform_events.parse_module_activated(envelope)
        await self.merge_module_config(command)

    async def seed_tenant_settings(self, command: SeedTenantSettingsCommand) -> Result[dict]:
        if await self._settings.exists(command.tenant_id):
            existing = await self._settings.find_by_tenant(command.tenant_id)
            return Result.ok(existing.to_dict() if existing else {})

        tenant_settings = TenantSettings.seed(
            tenant_id=command.tenant_id,
            industry_pack=command.industry_pack,
            locale=command.locale,
            enabled_modules=command.enabled_modules,
        )
        await self._settings.save(tenant_settings)

        await self._audit.log(
            tenant_id=command.tenant_id,
            correlation_id=command.correlation_id,
            action="settings.tenant.seeded",
            resource_type="tenant_settings",
            resource_id=str(tenant_settings.id),
        )
        return Result.ok(tenant_settings.to_dict())

    async def merge_module_config(self, command: MergeModuleConfigCommand) -> Result[dict]:
        tenant_settings = await self._settings.find_by_tenant(command.tenant_id)
        if not tenant_settings:
            return Result.fail("settings.errors.tenant_not_seeded")

        defaults = MODULE_DEFAULTS.get(command.module_id, {"enabled": True})
        tenant_settings.merge_module_config(command.module_id, defaults)
        await self._settings.save(tenant_settings)

        event = ConfigUpdatedIntegration(
            tenant_id=TenantId.create(command.tenant_id),
            correlation_id=command.correlation_id,
            config_key=f"module.{command.module_id}",
        )
        await publish_integration_event(event)
        return Result.ok(tenant_settings.to_dict())

    async def get_settings(self, tenant_id: str) -> Result[dict]:
        tenant_settings = await self._settings.find_by_tenant(tenant_id)
        if not tenant_settings:
            return Result.fail("settings.errors.tenant_not_seeded")
        return Result.ok(tenant_settings.to_dict())

    async def get_config_key(self, tenant_id: str, key: str) -> Result[dict]:
        tenant_settings = await self._settings.find_by_tenant(tenant_id)
        if not tenant_settings:
            return Result.fail("settings.errors.tenant_not_seeded")
        if key not in tenant_settings.config:
            return Result.fail("settings.errors.config_key_not_found")
        return Result.ok({"key": key, "value": tenant_settings.config[key]})

    async def update_config(
        self, tenant_id: str, key: str, value: Any, correlation_id: str
    ) -> Result[dict]:
        tenant_settings = await self._settings.find_by_tenant(tenant_id)
        if not tenant_settings:
            return Result.fail("settings.errors.tenant_not_seeded")

        tenant_settings.set_config(key, value)
        await self._settings.save(tenant_settings)

        event = ConfigUpdatedIntegration(
            tenant_id=TenantId.create(tenant_id),
            correlation_id=correlation_id,
            config_key=key,
        )
        await publish_integration_event(event)

        await self._audit.log(
            tenant_id=tenant_id,
            correlation_id=correlation_id,
            action="settings.config.updated",
            resource_type="config",
            resource_id=key,
        )
        return Result.ok(tenant_settings.to_dict())

    async def list_features(self, tenant_id: str) -> Result[dict]:
        tenant_settings = await self._settings.find_by_tenant(tenant_id)
        if not tenant_settings:
            return Result.fail("settings.errors.tenant_not_seeded")
        return Result.ok(tenant_settings.features)

    async def toggle_feature(
        self, tenant_id: str, key: str, enabled: bool, correlation_id: str
    ) -> Result[dict]:
        tenant_settings = await self._settings.find_by_tenant(tenant_id)
        if not tenant_settings:
            return Result.fail("settings.errors.tenant_not_seeded")

        tenant_settings.toggle_feature(key, enabled)
        await self._settings.save(tenant_settings)

        event = FeatureToggledIntegration(
            tenant_id=TenantId.create(tenant_id),
            correlation_id=correlation_id,
            feature_key=key,
            enabled=enabled,
        )
        await publish_integration_event(event)

        await self._audit.log(
            tenant_id=tenant_id,
            correlation_id=correlation_id,
            action="settings.feature.toggled",
            resource_type="feature",
            resource_id=key,
            payload={"enabled": enabled},
        )
        return Result.ok(tenant_settings.features)

    async def update_branding(
        self, tenant_id: str, branding: dict, correlation_id: str
    ) -> Result[dict]:
        tenant_settings = await self._settings.find_by_tenant(tenant_id)
        if not tenant_settings:
            return Result.fail("settings.errors.tenant_not_seeded")

        tenant_settings.branding.update(branding)
        tenant_settings.updated_at = datetime.now(UTC)
        await self._settings.save(tenant_settings)

        event = ConfigUpdatedIntegration(
            tenant_id=TenantId.create(tenant_id),
            correlation_id=correlation_id,
            config_key="branding",
        )
        await publish_integration_event(event)
        return Result.ok(tenant_settings.branding)
