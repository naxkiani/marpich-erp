"""Plugin DTO and runtime port."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class ExtensionInfo:
    plugin_id: str
    display_name: str
    plugin_type: str
    version: str
    extension_point: str


@dataclass(frozen=True, slots=True)
class InvokeResult:
    ok: bool
    plugin_id: str = ""
    extension_point: str = ""
    sandbox_profile: str = ""
    result: dict | None = None
    error: str | None = None


class IPluginRuntime(Protocol):
    async def list_extensions(
        self,
        *,
        tenant_id: str,
        extension_point: str,
    ) -> list[ExtensionInfo]: ...

    async def invoke(
        self,
        *,
        tenant_id: str,
        plugin_id: str,
        extension_point: str,
        payload: dict | None = None,
    ) -> InvokeResult: ...

    async def is_installed(self, *, tenant_id: str, plugin_id: str) -> bool: ...
