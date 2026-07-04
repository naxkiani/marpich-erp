"""Outbox dispatcher — polls unpublished events and delivers to consumers."""
from __future__ import annotations

import asyncio
import logging

from shared.infrastructure.messaging.event_bus import InProcessEventBus
from shared.infrastructure.messaging.kafka_transport import get_kafka_transport
from shared.infrastructure.messaging.outbox_repository import get_outbox_repository
from shared.infrastructure.settings import settings

logger = logging.getLogger(__name__)


class OutboxDispatcher:
    def __init__(self) -> None:
        self._task: asyncio.Task | None = None
        self._running = False

    async def dispatch_once(self) -> int:
        outbox = get_outbox_repository()
        kafka = get_kafka_transport()
        pending = await outbox.fetch_pending(limit=settings.outbox_batch_size)
        dispatched = 0
        for message in pending:
            try:
                await kafka.publish(message.envelope)
                await InProcessEventBus.deliver(message.envelope)
                await outbox.mark_published(message.id)
                dispatched += 1
            except Exception as exc:  # noqa: BLE001 — dispatch boundary
                logger.exception("Outbox dispatch failed for %s: %s", message.id, exc)
                await outbox.mark_failed(message.id, str(exc))
        return dispatched

    async def _poll_loop(self) -> None:
        interval = settings.outbox_poll_interval_ms / 1000
        while self._running:
            try:
                count = await self.dispatch_once()
                if count:
                    logger.debug("Outbox dispatched %s message(s)", count)
            except Exception:  # noqa: BLE001 — poll loop must survive
                logger.exception("Outbox poll loop error")
            await asyncio.sleep(interval)

    async def start(self) -> None:
        if settings.event_bus_mode != "outbox":
            return
        await get_kafka_transport().start()
        self._running = True
        self._task = asyncio.create_task(self._poll_loop())

    async def stop(self) -> None:
        self._running = False
        if self._task is not None:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None
        await get_kafka_transport().stop()


_dispatcher: OutboxDispatcher | None = None


def get_outbox_dispatcher() -> OutboxDispatcher:
    global _dispatcher
    if _dispatcher is None:
        _dispatcher = OutboxDispatcher()
    return _dispatcher


def reset_outbox_dispatcher() -> None:
    global _dispatcher
    _dispatcher = None
