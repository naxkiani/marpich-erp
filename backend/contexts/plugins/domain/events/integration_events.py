"""Plugin integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent


@dataclass(frozen=True, kw_only=True)
class PluginRegisteredIntegration(IntegrationEvent):
    plugin_id: str
    plugin_type: str
    version: str

    @property
    def event_name(self) -> str:
        return "plugin.registered"

    @property
    def source_context(self) -> str:
        return "plugins"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "plugin_id": self.plugin_id,
            "plugin_type": self.plugin_type,
            "version": self.version,
        }


@dataclass(frozen=True, kw_only=True)
class PluginPublishedIntegration(IntegrationEvent):
    plugin_id: str
    version: str
    trust_level: str

    @property
    def event_name(self) -> str:
        return "plugin.published"

    @property
    def source_context(self) -> str:
        return "plugins"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "plugin_id": self.plugin_id,
            "version": self.version,
            "trust_level": self.trust_level,
        }


@dataclass(frozen=True, kw_only=True)
class PluginInstalledIntegration(IntegrationEvent):
    plugin_id: str
    version: str
    granted_permissions: tuple[str, ...]

    @property
    def event_name(self) -> str:
        return "plugin.installed"

    @property
    def source_context(self) -> str:
        return "plugins"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "plugin_id": self.plugin_id,
            "version": self.version,
            "granted_permissions": list(self.granted_permissions),
        }


@dataclass(frozen=True, kw_only=True)
class PluginUpgradedIntegration(IntegrationEvent):
    plugin_id: str
    from_version: str
    to_version: str

    @property
    def event_name(self) -> str:
        return "plugin.upgraded"

    @property
    def source_context(self) -> str:
        return "plugins"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "plugin_id": self.plugin_id,
            "from_version": self.from_version,
            "to_version": self.to_version,
        }


@dataclass(frozen=True, kw_only=True)
class PluginUninstalledIntegration(IntegrationEvent):
    plugin_id: str

    @property
    def event_name(self) -> str:
        return "plugin.uninstalled"

    @property
    def source_context(self) -> str:
        return "plugins"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"plugin_id": self.plugin_id}


@dataclass(frozen=True, kw_only=True)
class SandboxViolationIntegration(IntegrationEvent):
    plugin_id: str
    violation_type: str

    @property
    def event_name(self) -> str:
        return "plugin.sandbox.violation"

    @property
    def source_context(self) -> str:
        return "plugins"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"plugin_id": self.plugin_id, "violation_type": self.violation_type}
