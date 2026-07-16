"""Connector adapter port — implemented by SDK adapters and plugins."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from shared.application.result import Result


class IConnectorAdapter(ABC):
    connector_type: str

    @abstractmethod
    async def test_connection(self, *, config: dict, secret: str = "") -> Result[dict]: ...

    @abstractmethod
    async def execute(
        self,
        *,
        operation: str,
        payload: dict,
        config: dict,
        secret: str = "",
        idempotency_key: str = "",
    ) -> Result[dict]: ...

    def supported_operations(self) -> list[str]:
        return []

    def metadata(self) -> dict[str, Any]:
        return {"connector_type": self.connector_type, "operations": self.supported_operations()}
