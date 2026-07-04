"""Localization repository ports."""
from __future__ import annotations

from abc import ABC, abstractmethod

from contexts.localization.domain.aggregates.locale import Locale
from contexts.localization.domain.aggregates.translation_bundle import TranslationBundle
from contexts.localization.domain.aggregates.translation_key import TranslationKey
from shared.domain.value_objects.unique_id import UniqueId


class ILocaleRepository(ABC):
    @abstractmethod
    async def save(self, locale: Locale) -> None: ...

    @abstractmethod
    async def find_by_code(self, tenant_id: str, code: str) -> Locale | None: ...

    @abstractmethod
    async def list_locales(self, tenant_id: str) -> list[Locale]: ...

    @abstractmethod
    async def exists(self, tenant_id: str) -> bool: ...


class ITranslationKeyRepository(ABC):
    @abstractmethod
    async def save(self, translation_key: TranslationKey) -> None: ...

    @abstractmethod
    async def find(self, tenant_id: str, namespace: str, key: str) -> TranslationKey | None: ...

    @abstractmethod
    async def list_keys(self, tenant_id: str, namespace: str | None = None) -> list[TranslationKey]: ...


class ITranslationBundleRepository(ABC):
    @abstractmethod
    async def save(self, bundle: TranslationBundle) -> None: ...

    @abstractmethod
    async def find(
        self, tenant_id: str, locale_code: str, namespace: str
    ) -> TranslationBundle | None: ...

    @abstractmethod
    async def list_for_locale(self, tenant_id: str, locale_code: str) -> list[TranslationBundle]: ...
