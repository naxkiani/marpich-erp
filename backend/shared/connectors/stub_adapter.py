"""Base connector adapter with simulated execution for dev/tests."""
from __future__ import annotations

from shared.application.result import Result
from shared.connectors.base import IConnectorAdapter


class BaseConnectorAdapter(IConnectorAdapter):
    """Stub adapter — subclasses override operations for real integrations."""

    def __init__(self, connector_type: str, operations: list[str] | None = None) -> None:
        self.connector_type = connector_type
        self._operations = operations or ["test_connection"]

    def supported_operations(self) -> list[str]:
        return list(self._operations)

    async def test_connection(self, *, config: dict, secret: str = "") -> Result[dict]:
        if not config:
            return Result.fail("config_required")
        return Result.ok({
            "connector_type": self.connector_type,
            "connected": True,
            "latency_ms": 42,
            "environment": config.get("environment", "sandbox"),
        })

    async def execute(
        self,
        *,
        operation: str,
        payload: dict,
        config: dict,
        secret: str = "",
        idempotency_key: str = "",
    ) -> Result[dict]:
        if operation not in self._operations:
            return Result.fail(f"unsupported_operation:{operation}")
        return Result.ok({
            "connector_type": self.connector_type,
            "operation": operation,
            "status": "completed",
            "idempotency_key": idempotency_key or None,
            "result": {"simulated": True, "payload_keys": list(payload.keys())},
        })
