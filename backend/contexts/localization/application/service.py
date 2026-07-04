"""Localization application service."""
from __future__ import annotations

import json
from datetime import UTC, datetime

from contexts.localization.application.commands.seed_tenant_locales import SeedTenantLocalesCommand
from contexts.localization.application.constants.default_locales import DEFAULT_LOCALES
from contexts.localization.application.ports.platform_events import IPlatformLocalizationAdapter
from contexts.localization.domain.aggregates.locale import Locale, TextDirection
from contexts.localization.domain.aggregates.translation_bundle import TranslationBundle
from contexts.localization.domain.aggregates.translation_key import TranslationKey
from contexts.localization.domain.events.integration_events import (
    KeyMissingIntegration,
    LocaleChangedIntegration,
    TranslationUpdatedIntegration,
)
from contexts.localization.domain.ports.repositories import (
    ILocaleRepository,
    ITranslationBundleRepository,
    ITranslationKeyRepository,
)
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class ConsoleLocalizationAudit:
    async def log(self, **kwargs: object) -> None:
        entry = {"type": "audit", "context": "localization", **kwargs, "occurred_at": datetime.now(UTC).isoformat()}
        print(json.dumps(entry, default=str))


class LocalizationApplicationService:
    def __init__(
        self,
        locales: ILocaleRepository,
        keys: ITranslationKeyRepository,
        bundles: ITranslationBundleRepository,
        platform_events: IPlatformLocalizationAdapter,
        audit: ConsoleLocalizationAudit | None = None,
    ) -> None:
        self._locales = locales
        self._keys = keys
        self._bundles = bundles
        self._platform_events = platform_events
        self._audit = audit or ConsoleLocalizationAudit()

    async def handle_tenant_provisioned(self, envelope: dict) -> None:
        command = await self._platform_events.parse_tenant_provisioned(envelope)
        await self.seed_tenant_locales(command)

    async def seed_tenant_locales(self, command: SeedTenantLocalesCommand) -> Result[dict]:
        if await self._locales.exists(command.tenant_id):
            locales = await self._locales.list_locales(command.tenant_id)
            return Result.ok({"locales": [l.to_dict() for l in locales]})

        created: list[Locale] = []
        for code, name, direction, is_default in DEFAULT_LOCALES:
            locale = Locale.create(
                tenant_id=command.tenant_id,
                code=code,
                name=name,
                direction=TextDirection(direction),
                is_default=(code == command.default_locale),
            )
            await self._locales.save(locale)
            created.append(locale)

        default = next((l for l in created if l.is_default), created[0])
        event = LocaleChangedIntegration(
            tenant_id=TenantId.create(command.tenant_id),
            correlation_id=command.correlation_id,
            locale_code=default.code,
            is_default=True,
        )
        await publish_integration_event(event)
        return Result.ok({"locales": [l.to_dict() for l in created]})

    async def list_locales(self, tenant_id: str) -> Result[list[dict]]:
        locales = await self._locales.list_locales(tenant_id)
        if not locales:
            return Result.fail("localization.errors.tenant_not_seeded")
        return Result.ok([l.to_dict() for l in locales])

    async def define_key(
        self,
        *,
        tenant_id: str,
        namespace: str,
        key: str,
        default_value: str,
        description: str,
        correlation_id: str,
    ) -> Result[dict]:
        existing = await self._keys.find(tenant_id, namespace, key)
        if existing:
            existing.default_value = default_value
            existing.description = description
            existing.updated_at = datetime.now(UTC)
            translation_key = existing
        else:
            translation_key = TranslationKey.define(
                tenant_id=tenant_id,
                namespace=namespace,
                key=key,
                default_value=default_value,
                description=description,
            )
        await self._keys.save(translation_key)
        await self._audit.log(
            tenant_id=tenant_id,
            correlation_id=correlation_id,
            action="localization.key.defined",
            resource_type="translation_key",
            resource_id=translation_key.qualified_key,
        )
        return Result.ok(translation_key.to_dict())

    async def upsert_translation(
        self,
        *,
        tenant_id: str,
        locale_code: str,
        namespace: str,
        key: str,
        value: str,
        correlation_id: str,
    ) -> Result[dict]:
        locale = await self._locales.find_by_code(tenant_id, locale_code)
        if not locale:
            return Result.fail("localization.errors.locale_not_found")

        bundle = await self._bundles.find(tenant_id, locale_code, namespace)
        if not bundle:
            bundle = TranslationBundle.create(
                tenant_id=tenant_id, locale_code=locale_code, namespace=namespace
            )
        bundle.set_entry(key, value)
        await self._bundles.save(bundle)

        event = TranslationUpdatedIntegration(
            tenant_id=TenantId.create(tenant_id),
            correlation_id=correlation_id,
            namespace=namespace,
            key=key,
            locale_code=locale_code,
        )
        await publish_integration_event(event)
        return Result.ok(bundle.to_dict())

    async def get_bundle(self, tenant_id: str, locale_code: str, namespace: str) -> Result[dict]:
        bundle = await self._bundles.find(tenant_id, locale_code, namespace)
        if bundle:
            return Result.ok(bundle.to_dict())

        keys = await self._keys.list_keys(tenant_id, namespace)
        if not keys:
            return Result.fail("localization.errors.bundle_not_found")

        entries = {k.key: k.default_value for k in keys}
        return Result.ok(
            {
                "tenant_id": tenant_id,
                "locale_code": locale_code,
                "namespace": namespace,
                "entries": entries,
                "source": "defaults",
            }
        )

    async def report_missing_key(
        self,
        *,
        tenant_id: str,
        locale_code: str,
        namespace: str,
        key: str,
        correlation_id: str,
    ) -> Result[dict]:
        event = KeyMissingIntegration(
            tenant_id=TenantId.create(tenant_id),
            correlation_id=correlation_id,
            namespace=namespace,
            key=key,
            locale_code=locale_code,
        )
        await publish_integration_event(event)
        return Result.ok(event.to_payload())
