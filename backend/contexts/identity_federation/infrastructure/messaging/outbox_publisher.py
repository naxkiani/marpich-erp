"""Outbox-oriented messaging adapter surface for federation events (P200-B2)."""
from __future__ import annotations

from typing import Any, Protocol

from shared.infrastructure.messaging.event_bus import publish_integration_event


class IFederationEventPublisher(Protocol):
    async def publish(self, event: Any) -> None: ...


class OutboxFederationEventPublisher:
    """Delegates to platform Event Fabric / in-process bus — no direct Kafka client in domain."""

    async def publish(self, event: Any) -> None:
        await publish_integration_event(event)
