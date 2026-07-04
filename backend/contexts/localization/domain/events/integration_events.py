"""Localization integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(frozen=True, kw_only=True)
class LocaleChangedIntegration(IntegrationEvent):
    locale_code: str
    is_default: bool

    @property
    def event_name(self) -> str:
        return "localization.locale.changed"

    @property
    def source_context(self) -> str:
        return "localization"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"locale_code": self.locale_code, "is_default": self.is_default}


@dataclass(frozen=True, kw_only=True)
class TranslationUpdatedIntegration(IntegrationEvent):
    namespace: str
    key: str
    locale_code: str

    @property
    def event_name(self) -> str:
        return "localization.translation.updated"

    @property
    def source_context(self) -> str:
        return "localization"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"namespace": self.namespace, "key": self.key, "locale_code": self.locale_code}


@dataclass(frozen=True, kw_only=True)
class KeyMissingIntegration(IntegrationEvent):
    namespace: str
    key: str
    locale_code: str

    @property
    def event_name(self) -> str:
        return "localization.key.missing"

    @property
    def source_context(self) -> str:
        return "localization"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"namespace": self.namespace, "key": self.key, "locale_code": self.locale_code}
