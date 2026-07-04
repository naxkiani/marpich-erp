"""Plugins DI."""
from __future__ import annotations

from contexts.plugins.application.service import PluginApplicationService
from contexts.plugins.infrastructure.adapters.runtime_client import PluginRuntimeClient
from contexts.plugins.infrastructure.persistence.memory_store import (
    InMemoryPluginInstallationRepository,
    InMemoryPluginRepository,
)
from shared.application.ports.plugins import IPluginRuntime

_service: PluginApplicationService | None = None
_runtime: PluginRuntimeClient | None = None


def get_plugin_service() -> PluginApplicationService:
    global _service, _runtime
    if _service is None:
        _service = PluginApplicationService(
            plugins=InMemoryPluginRepository(),
            installations=InMemoryPluginInstallationRepository(),
        )
        _runtime = PluginRuntimeClient(_service)
    return _service


def get_plugin_runtime() -> IPluginRuntime:
    get_plugin_service()
    assert _runtime is not None
    return _runtime


def reset_plugin_service() -> None:
    global _service, _runtime
    _service = None
    _runtime = None
    InMemoryPluginRepository.reset()
    InMemoryPluginInstallationRepository.reset()
