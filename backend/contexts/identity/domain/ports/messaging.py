"""Messaging ports — implemented in infrastructure/messaging/."""
from __future__ import annotations

from typing import Protocol


class IAuditLogger(Protocol):
    async def log(
        self,
        *,
        tenant_id: str,
        correlation_id: str,
        action: str,
        resource_type: str,
        resource_id: str | None = None,
        actor_id: str | None = None,
        payload: dict | None = None,
        ip_address: str | None = None,
    ) -> None: ...


class IOutboxPublisher(Protocol):
    async def publish(self, event: object) -> None: ...
