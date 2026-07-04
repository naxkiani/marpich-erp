"""Plugin runtime port adapter."""
from __future__ import annotations

from contexts.plugins.application.service import PluginApplicationService
from shared.application.ports.plugins import ExtensionInfo, InvokeResult, IPluginRuntime


class PluginRuntimeClient(IPluginRuntime):
    def __init__(self, service: PluginApplicationService) -> None:
        self._service = service

    async def list_extensions(
        self,
        *,
        tenant_id: str,
        extension_point: str,
    ) -> list[ExtensionInfo]:
        result = await self._service.list_extensions(tenant_id, extension_point)
        return [
            ExtensionInfo(
                plugin_id=item["plugin_id"],
                display_name=item["display_name"],
                plugin_type=item["plugin_type"],
                version=item["version"],
                extension_point=item["extension_point"],
            )
            for item in result.unwrap()
        ]

    async def invoke(
        self,
        *,
        tenant_id: str,
        plugin_id: str,
        extension_point: str,
        payload: dict | None = None,
    ) -> InvokeResult:
        result = await self._service.invoke_plugin(
            tenant_id=tenant_id,
            plugin_id=plugin_id,
            extension_point=extension_point,
            payload=payload or {},
        )
        if not result.succeeded:
            return InvokeResult(ok=False, error=result.error or "invoke_failed")
        data = result.unwrap()
        return InvokeResult(
            ok=True,
            plugin_id=data["plugin_id"],
            extension_point=data["extension_point"],
            sandbox_profile=data["sandbox_profile"],
            result=data["result"],
        )

    async def is_installed(self, *, tenant_id: str, plugin_id: str) -> bool:
        installs = await self._service.list_installed(tenant_id)
        return any(i["plugin_id"] == plugin_id for i in installs.unwrap())
