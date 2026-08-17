"""Force AuthZ memory path unless a test opts into Postgres wiring."""
from __future__ import annotations

import pytest

from contexts.authorization.container import reset_authorization_service
from shared.infrastructure.messaging.event_fabric import EventFabric
from shared.infrastructure.messaging.idempotency import InMemoryProcessedEventStore


@pytest.fixture(autouse=True)
def _authorization_memory_backend(monkeypatch):
    monkeypatch.setattr("contexts.authorization.container.use_postgres", lambda: False)
    monkeypatch.setattr("contexts.identity.container.use_postgres", lambda: False)
    monkeypatch.setattr(
        "shared.infrastructure.messaging.idempotency.use_postgres",
        lambda: False,
    )
    monkeypatch.setattr(
        "shared.infrastructure.messaging.event_bus.get_processed_event_store",
        lambda: InMemoryProcessedEventStore(),
    )
    EventFabric.reset_dev_state()
    reset_authorization_service()
    yield
    reset_authorization_service()
    EventFabric.reset_dev_state()
