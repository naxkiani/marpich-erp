"""Postgres outbox repository — skip unless PERSISTENCE_BACKEND=postgres."""
from __future__ import annotations

import os
import uuid

import pytest

from shared.infrastructure.messaging.outbox_repository import (
    PostgresOutboxRepository,
    reset_outbox_repository,
)
from shared.infrastructure.settings import use_postgres

pytestmark = pytest.mark.asyncio


def _postgres_configured() -> bool:
    return os.getenv("PERSISTENCE_BACKEND", "").lower() == "postgres" and use_postgres()


@pytest.fixture
async def require_postgres():
    if not _postgres_configured():
        pytest.skip("Postgres outbox E2E requires PERSISTENCE_BACKEND=postgres")
    reset_outbox_repository()
    yield
    reset_outbox_repository()
    from shared.infrastructure.database.engine import dispose_engine

    await dispose_engine()


async def test_postgres_outbox_enqueue_fetch_mark_published(require_postgres):
    repo = PostgresOutboxRepository()
    event_id = str(uuid.uuid4())
    envelope = {
        "event_id": event_id,
        "event_name": "test.outbox.created",
        "event_version": 1,
        "source_context": "test",
        "tenant_id": "tenant-outbox-e2e",
        "correlation_id": "corr-outbox-e2e",
        "payload": {"ok": True},
    }
    msg_id = await repo.enqueue(envelope)
    pending = await repo.fetch_pending(limit=50)
    assert any(m.id == msg_id for m in pending)
    await repo.mark_published(msg_id)
    leftover = await repo.fetch_pending(limit=50)
    assert all(m.id != msg_id for m in leftover)


async def test_postgres_outbox_mark_failed_increments_retry(require_postgres):
    repo = PostgresOutboxRepository()
    event_id = str(uuid.uuid4())
    envelope = {
        "event_id": event_id,
        "event_name": "test.outbox.failed",
        "event_version": 1,
        "source_context": "test",
        "tenant_id": "tenant-outbox-e2e",
        "correlation_id": "corr-outbox-fail",
        "payload": {},
    }
    msg_id = await repo.enqueue(envelope)
    await repo.mark_failed(msg_id, "boom")
    pending = await repo.fetch_pending(limit=50)
    hit = next(m for m in pending if m.id == msg_id)
    assert hit.retry_count >= 1
    await repo.mark_published(msg_id)
