"""Localization in-memory repositories."""
from __future__ import annotations

from contexts.localization.domain.aggregates.locale import Locale
from contexts.localization.domain.aggregates.translation_bundle import TranslationBundle
from contexts.localization.domain.aggregates.translation_key import TranslationKey
from contexts.localization.domain.ports.repositories import (
    ILocaleRepository,
    ITranslationBundleRepository,
    ITranslationKeyRepository,
)


class LocalizationMemoryStore:
    locales: dict[str, Locale] = {}
    keys: dict[str, TranslationKey] = {}
    bundles: dict[str, TranslationBundle] = {}

    @classmethod
    def reset(cls) -> None:
        cls.locales.clear()
        cls.keys.clear()
        cls.bundles.clear()


def _key_id(tenant_id: str, namespace: str, key: str) -> str:
    return f"{tenant_id}:{namespace}:{key}"


def _bundle_id(tenant_id: str, locale_code: str, namespace: str) -> str:
    return f"{tenant_id}:{locale_code}:{namespace}"


class InMemoryLocaleRepository(ILocaleRepository):
    async def save(self, locale: Locale) -> None:
        LocalizationMemoryStore.locales[f"{locale.tenant_id}:{locale.code}"] = locale

    async def find_by_code(self, tenant_id: str, code: str) -> Locale | None:
        return LocalizationMemoryStore.locales.get(f"{tenant_id}:{code.lower()}")

    async def list_locales(self, tenant_id: str) -> list[Locale]:
        return [l for l in LocalizationMemoryStore.locales.values() if l.tenant_id == tenant_id]

    async def exists(self, tenant_id: str) -> bool:
        return any(l.tenant_id == tenant_id for l in LocalizationMemoryStore.locales.values())


class InMemoryTranslationKeyRepository(ITranslationKeyRepository):
    async def save(self, translation_key: TranslationKey) -> None:
        LocalizationMemoryStore.keys[
            _key_id(translation_key.tenant_id, translation_key.namespace, translation_key.key)
        ] = translation_key

    async def find(self, tenant_id: str, namespace: str, key: str) -> TranslationKey | None:
        return LocalizationMemoryStore.keys.get(_key_id(tenant_id, namespace, key))

    async def list_keys(self, tenant_id: str, namespace: str | None = None) -> list[TranslationKey]:
        keys = [k for k in LocalizationMemoryStore.keys.values() if k.tenant_id == tenant_id]
        if namespace:
            keys = [k for k in keys if k.namespace == namespace]
        return keys


class InMemoryTranslationBundleRepository(ITranslationBundleRepository):
    async def save(self, bundle: TranslationBundle) -> None:
        LocalizationMemoryStore.bundles[
            _bundle_id(bundle.tenant_id, bundle.locale_code, bundle.namespace)
        ] = bundle

    async def find(self, tenant_id: str, locale_code: str, namespace: str) -> TranslationBundle | None:
        return LocalizationMemoryStore.bundles.get(_bundle_id(tenant_id, locale_code.lower(), namespace))

    async def list_for_locale(self, tenant_id: str, locale_code: str) -> list[TranslationBundle]:
        code = locale_code.lower()
        return [
            b
            for b in LocalizationMemoryStore.bundles.values()
            if b.tenant_id == tenant_id and b.locale_code == code
        ]
