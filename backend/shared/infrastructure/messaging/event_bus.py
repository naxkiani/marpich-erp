"""In-process integration event bus — production uses outbox + Kafka."""
from __future__ import annotations

import json
import logging
from collections import defaultdict
from typing import Awaitable, Callable

from shared.infrastructure.messaging.idempotency import (
    ProcessedEventKey,
    consumer_id_for_handler,
    get_processed_event_store,
)

logger = logging.getLogger(__name__)

Handler = Callable[[dict], Awaitable[None]]


class InProcessEventBus:
    _subscribers: dict[str, list[Handler]] = defaultdict(list)

    @classmethod
    def subscribe(cls, event_name: str, handler: Handler) -> None:
        cls._subscribers[event_name].append(handler)

    @classmethod
    async def deliver(cls, envelope: dict) -> None:
        """Deliver to subscribers with idempotent consumer guards."""
        event_name = envelope.get("event_name", "")
        logger.debug("Delivering event %s", event_name)
        print(json.dumps({"type": "integration_event", **envelope}))

        store = get_processed_event_store()
        tenant_id = str(envelope.get("tenant_id", ""))
        event_id = str(envelope.get("event_id", ""))

        for handler in cls._subscribers.get(event_name, []):
            await cls._invoke_handler(store, handler, envelope, tenant_id, event_id, event_name)

        for handler in cls._subscribers.get("*", []):
            await cls._invoke_handler(store, handler, envelope, tenant_id, event_id, event_name)

    @classmethod
    async def _invoke_handler(
        cls,
        store: object,
        handler: Handler,
        envelope: dict,
        tenant_id: str,
        event_id: str,
        event_name: str,
    ) -> None:
        if not event_id:
            await handler(envelope)
            return

        consumer_id = consumer_id_for_handler(handler)
        key = ProcessedEventKey(tenant_id=tenant_id, event_id=event_id, consumer_id=consumer_id)
        if await store.is_processed(key):  # type: ignore[attr-defined]
            return

        try:
            await handler(envelope)
            await store.mark_processed(key, event_name)  # type: ignore[attr-defined]
        except Exception:
            logger.exception("Handler failed: %s for event %s", consumer_id, event_name)
            raise

    @classmethod
    async def publish(cls, envelope: dict) -> None:
        """Backward-compatible alias for deliver."""
        await cls.deliver(envelope)

    @classmethod
    def reset(cls) -> None:
        cls._subscribers = defaultdict(list)


async def publish_integration_event(event: object) -> None:
    """Publish via enterprise event fabric (lazy import avoids circular deps)."""
    from shared.infrastructure.messaging.event_fabric import EventFabric

    await EventFabric.publish(event)
