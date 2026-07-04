"""In-memory plugin persistence."""
from __future__ import annotations

from contexts.plugins.domain.aggregates.plugin import Plugin, PluginInstallation
from contexts.plugins.domain.ports.repositories import (
    IPluginInstallationRepository,
    IPluginRepository,
)


class InMemoryPluginRepository(IPluginRepository):
    _plugins: dict[str, Plugin] = {}

    @classmethod
    def reset(cls) -> None:
        cls._plugins = {}

    async def save(self, plugin: Plugin) -> None:
        self._plugins[plugin.plugin_id] = plugin

    async def find_by_id(self, plugin_id: str) -> Plugin | None:
        return self._plugins.get(plugin_id.strip().lower())

    async def list_all(self) -> list[Plugin]:
        return list(self._plugins.values())

    async def list_by_type(self, plugin_type: str) -> list[Plugin]:
        return [p for p in self._plugins.values() if p.plugin_type == plugin_type]

    async def search(self, query: str) -> list[Plugin]:
        q = query.lower()
        return [
            p
            for p in self._plugins.values()
            if q in p.display_name.lower() or q in p.description.lower()
        ]


class InMemoryPluginInstallationRepository(IPluginInstallationRepository):
    _installations: dict[str, PluginInstallation] = {}

    @classmethod
    def reset(cls) -> None:
        cls._installations = {}

    def _key(self, tenant_id: str, plugin_id: str) -> str:
        return f"{tenant_id}:{plugin_id}"

    async def save(self, installation: PluginInstallation) -> None:
        self._installations[self._key(installation.tenant_id, installation.plugin_id)] = installation

    async def find(self, tenant_id: str, plugin_id: str) -> PluginInstallation | None:
        return self._installations.get(self._key(tenant_id, plugin_id))

    async def list_by_tenant(self, tenant_id: str) -> list[PluginInstallation]:
        return [i for k, i in self._installations.items() if k.startswith(f"{tenant_id}:")]

    async def delete(self, tenant_id: str, plugin_id: str) -> bool:
        key = self._key(tenant_id, plugin_id)
        if key in self._installations:
            del self._installations[key]
            return True
        return False
