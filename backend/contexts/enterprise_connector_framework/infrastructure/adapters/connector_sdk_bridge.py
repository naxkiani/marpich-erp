"""Bridge to shared Connector SDK."""
from __future__ import annotations

from shared.application.result import Result
from shared.connectors import get_connector_adapter, list_registered_connectors, register_builtin_connectors


class ConnectorSdkBridge:
    _initialized = False

    @classmethod
    def ensure_initialized(cls) -> None:
        if not cls._initialized:
            register_builtin_connectors()
            cls._initialized = True

    @classmethod
    def reset(cls) -> None:
        cls._initialized = False

    def list_sdk_types(self) -> list[str]:
        self.ensure_initialized()
        return list_registered_connectors()

    async def test_connection(self, *, connector_type: str, config: dict, secret: str = "") -> Result[dict]:
        self.ensure_initialized()
        adapter = get_connector_adapter(connector_type)
        if adapter is None:
            return Result.fail(f"connector_adapter_not_found:{connector_type}")
        return await adapter.test_connection(config=config, secret=secret)

    async def execute(
        self,
        *,
        connector_type: str,
        operation: str,
        payload: dict,
        config: dict,
        secret: str = "",
        idempotency_key: str = "",
    ) -> Result[dict]:
        self.ensure_initialized()
        adapter = get_connector_adapter(connector_type)
        if adapter is None:
            return Result.fail(f"connector_adapter_not_found:{connector_type}")
        return await adapter.execute(
            operation=operation,
            payload=payload,
            config=config,
            secret=secret,
            idempotency_key=idempotency_key,
        )

    def adapter_metadata(self, connector_type: str) -> dict:
        self.ensure_initialized()
        adapter = get_connector_adapter(connector_type)
        if adapter is None:
            return {"connector_type": connector_type, "registered": False}
        return {**adapter.metadata(), "registered": True}


_bridge: ConnectorSdkBridge | None = None


def get_connector_sdk_bridge() -> ConnectorSdkBridge:
    global _bridge
    if _bridge is None:
        _bridge = ConnectorSdkBridge()
    return _bridge
