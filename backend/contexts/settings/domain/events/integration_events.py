"""Settings integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent


@dataclass(frozen=True, kw_only=True)
class ConfigUpdatedIntegration(IntegrationEvent):
    config_key: str

    @property
    def event_name(self) -> str:
        return "settings.config.updated"

    @property
    def source_context(self) -> str:
        return "settings"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"config_key": self.config_key}


@dataclass(frozen=True, kw_only=True)
class FeatureToggledIntegration(IntegrationEvent):
    feature_key: str
    enabled: bool

    @property
    def event_name(self) -> str:
        return "settings.feature.toggled"

    @property
    def source_context(self) -> str:
        return "settings"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"feature_key": self.feature_key, "enabled": self.enabled}
