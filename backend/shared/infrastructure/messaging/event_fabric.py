"""Enterprise event fabric — enqueue, dispatch, idempotent delivery."""
from __future__ import annotations

from shared.infrastructure.messaging.dispatcher import get_outbox_dispatcher, reset_outbox_dispatcher
from shared.infrastructure.messaging.event_bus import InProcessEventBus
from shared.infrastructure.messaging.idempotency import ProcessedEventMemoryStore
from shared.infrastructure.messaging.kafka_transport import reset_kafka_transport
from shared.infrastructure.messaging.outbox_repository import (
    OutboxMemoryStore,
    get_outbox_repository,
    reset_outbox_repository,
)
from shared.infrastructure.settings import settings


class EventFabric:
    @staticmethod
    async def publish(event: object) -> None:
        envelope = event.envelope() if hasattr(event, "envelope") else event
        if settings.event_bus_mode == "outbox":
            await get_outbox_repository().enqueue(envelope)
            if settings.outbox_dispatch_immediate:
                await get_outbox_dispatcher().dispatch_once()
        else:
            await InProcessEventBus.deliver(envelope)

    @staticmethod
    def reset_dev_state() -> None:
        OutboxMemoryStore.reset()
        ProcessedEventMemoryStore.reset()
        InProcessEventBus.reset()
        reset_outbox_repository()
        reset_outbox_dispatcher()
        reset_kafka_transport()


async def publish_integration_event(event: object) -> None:
    await EventFabric.publish(event)
