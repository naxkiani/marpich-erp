"""Messenger DI container."""
from __future__ import annotations

from contexts.messenger.application.service import MessengerApplicationService
from contexts.messenger.infrastructure.persistence.memory_store import (
    InMemoryConversationRepository,
    InMemoryMessageRepository,
)

_service: MessengerApplicationService | None = None


def get_messenger_service() -> MessengerApplicationService:
    global _service
    if _service is None:
        _service = MessengerApplicationService(
            conversations=InMemoryConversationRepository(),
            messages=InMemoryMessageRepository(),
        )
    return _service


def reset_messenger_service() -> None:
    global _service
    _service = None
