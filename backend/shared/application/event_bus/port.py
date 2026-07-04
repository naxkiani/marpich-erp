"""Integration event bus port — infrastructure implements Kafka/RabbitMQ."""

from __future__ import annotations

from typing import Awaitable, Callable, Protocol

from shared.domain.events.integration_event import IntegrationEventEnvelope

EventHandler = Callable[[IntegrationEventEnvelope], Awaitable[None]]


class IIntegrationEventBus(Protocol):
    async def publish(self, event: IntegrationEventEnvelope) -> None: ...

    def subscribe(self, event_name: str, handler: EventHandler) -> None: ...

    def subscribe_context(self, source_context: str, handler: EventHandler) -> None: ...
