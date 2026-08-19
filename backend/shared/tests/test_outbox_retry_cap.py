"""Outbox pending fetch excludes rows at max retry (bounded DLQ)."""
from __future__ import annotations

import pytest

from shared.infrastructure.messaging.outbox_repository import (
    InMemoryOutboxRepository,
    OutboxMemoryStore,
    reset_outbox_repository,
)


@pytest.fixture(autouse=True)
def _reset():
    OutboxMemoryStore.reset()
    reset_outbox_repository()
    yield
    OutboxMemoryStore.reset()
    reset_outbox_repository()


@pytest.mark.asyncio
async def test_outbox_stops_dispatch_after_max_retries(monkeypatch):
    monkeypatch.setattr(
        "shared.infrastructure.settings.settings.outbox_max_retries",
        2,
    )
    repo = InMemoryOutboxRepository()
    msg_id = await repo.enqueue(
        {
            "event_id": "e1",
            "event_name": "test.retry.cap",
            "tenant_id": "t1",
            "payload": {},
        }
    )
    await repo.mark_failed(msg_id, "boom-1")
    pending_after_one = await repo.fetch_pending(limit=10)
    assert any(m.id == msg_id for m in pending_after_one)
    await repo.mark_failed(msg_id, "boom-2")
    pending_after_cap = await repo.fetch_pending(limit=10)
    assert all(m.id != msg_id for m in pending_after_cap)
    parked = OutboxMemoryStore._messages.get(msg_id)
    assert parked is not None
    assert parked.retry_count >= 2
