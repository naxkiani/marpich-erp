"""Kafka transport — optional fan-out to external consumers."""
from __future__ import annotations

import json
import logging

from shared.domain.events.event_envelope import EventEnvelope
from shared.infrastructure.settings import settings

logger = logging.getLogger(__name__)


class KafkaEventTransport:
    """Publishes to Kafka when bootstrap servers are configured."""

    def __init__(self) -> None:
        self._producer = None

    async def start(self) -> None:
        if not settings.kafka_enabled or not settings.kafka_bootstrap_servers:
            return
        try:
            from aiokafka import AIOKafkaProducer  # type: ignore[import-not-found]

            self._producer = AIOKafkaProducer(
                bootstrap_servers=settings.kafka_bootstrap_servers,
                value_serializer=lambda v: json.dumps(v, default=str).encode(),
            )
            await self._producer.start()
            logger.info("Kafka producer connected: %s", settings.kafka_bootstrap_servers)
        except ImportError:
            logger.warning("aiokafka not installed — Kafka transport disabled")
        except Exception as exc:  # noqa: BLE001 — startup boundary
            logger.warning("Kafka producer failed to start: %s", exc)

    async def stop(self) -> None:
        if self._producer is not None:
            await self._producer.stop()
            self._producer = None

    async def publish(self, envelope: dict) -> None:
        if self._producer is None:
            return
        mapped = EventEnvelope.from_integration_event(envelope)
        await self._producer.send_and_wait(
            mapped.topic,
            value=mapped.body,
            key=mapped.key.encode(),
            headers=[(k, v.encode()) for k, v in mapped.headers.items()],
        )


_kafka_transport: KafkaEventTransport | None = None


def get_kafka_transport() -> KafkaEventTransport:
    global _kafka_transport
    if _kafka_transport is None:
        _kafka_transport = KafkaEventTransport()
    return _kafka_transport


def reset_kafka_transport() -> None:
    global _kafka_transport
    _kafka_transport = None
