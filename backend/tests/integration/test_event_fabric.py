"""Event fabric — outbox dispatch and idempotent delivery."""
import pytest

from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.messaging.dispatcher import get_outbox_dispatcher
from shared.infrastructure.messaging.event_bus import InProcessEventBus
from shared.infrastructure.messaging.event_fabric import EventFabric, publish_integration_event
from shared.infrastructure.messaging.outbox_repository import OutboxMemoryStore
from shared.infrastructure import settings as settings_module


def _sample_envelope(event_id: str | None = None) -> dict:
    eid = event_id or str(UniqueId.generate())
    return {
        "event_id": eid,
        "event_name": "test.event.created",
        "event_version": 1,
        "source_context": "test",
        "tenant_id": "tenant-alpha",
        "correlation_id": "corr-1",
        "causation_id": None,
        "occurred_at": "2026-07-02T00:00:00+00:00",
        "payload": {"value": 42},
    }


@pytest.fixture(autouse=True)
def reset_fabric():
    EventFabric.reset_dev_state()
    yield
    EventFabric.reset_dev_state()


@pytest.mark.asyncio
async def test_idempotent_handler_runs_once():
    calls: list[str] = []

    async def handler(envelope: dict) -> None:
        calls.append(envelope["event_id"])

    InProcessEventBus.subscribe("test.event.created", handler)
    envelope = _sample_envelope()

    await InProcessEventBus.deliver(envelope)
    await InProcessEventBus.deliver(envelope)

    assert len(calls) == 1


@pytest.mark.asyncio
async def test_direct_mode_publish_delivers_immediately():
    received: list[dict] = []

    async def handler(envelope: dict) -> None:
        received.append(envelope)

    InProcessEventBus.subscribe("test.event.created", handler)
    envelope = _sample_envelope()

    await publish_integration_event(envelope)

    assert len(received) == 1
    assert received[0]["event_id"] == envelope["event_id"]


@pytest.mark.asyncio
async def test_outbox_mode_enqueues_then_dispatches(monkeypatch):
    monkeypatch.setattr(settings_module.settings, "event_bus_mode", "outbox")
    monkeypatch.setattr(settings_module.settings, "outbox_dispatch_immediate", True)

    delivered: list[dict] = []

    async def handler(envelope: dict) -> None:
        delivered.append(envelope)

    InProcessEventBus.subscribe("test.event.created", handler)
    envelope = _sample_envelope()

    await EventFabric.publish(envelope)

    assert len(delivered) == 1
    assert not OutboxMemoryStore._messages


@pytest.mark.asyncio
async def test_outbox_dispatcher_poll_drains_queue(monkeypatch):
    monkeypatch.setattr(settings_module.settings, "event_bus_mode", "outbox")
    monkeypatch.setattr(settings_module.settings, "outbox_dispatch_immediate", False)

    delivered: list[dict] = []

    async def handler(envelope: dict) -> None:
        delivered.append(envelope)

    InProcessEventBus.subscribe("test.event.created", handler)
    envelope = _sample_envelope()

    await EventFabric.publish(envelope)
    assert OutboxMemoryStore._messages

    count = await get_outbox_dispatcher().dispatch_once()
    assert count == 1
    assert len(delivered) == 1
    assert not OutboxMemoryStore._messages
