"""Messenger DI container."""
from __future__ import annotations

from contexts.messenger.application.service import MessengerApplicationService
from contexts.messenger.infrastructure.external_apis.livekit_media import LiveKitRealtimeMediaAdapter
from contexts.messenger.infrastructure.persistence.memory_store import (
    InMemoryConversationRepository,
    InMemoryMessageRepository,
)
from contexts.messenger.infrastructure.persistence.postgres_store import (
    PostgresConversationRepository,
    PostgresMessageRepository,
)
from shared.infrastructure.settings import use_postgres

_service: MessengerApplicationService | None = None


def get_messenger_service() -> MessengerApplicationService:
    global _service
    if _service is None:
        media = LiveKitRealtimeMediaAdapter()
        if use_postgres():
            _service = MessengerApplicationService(
                conversations=PostgresConversationRepository(),
                messages=PostgresMessageRepository(),
                realtime_media=media,
            )
        else:
            _service = MessengerApplicationService(
                conversations=InMemoryConversationRepository(),
                messages=InMemoryMessageRepository(),
                realtime_media=media,
            )
    return _service


def reset_messenger_service() -> None:
    global _service
    _service = None
