"""Messenger repository ports."""
from __future__ import annotations

from typing import Protocol

from contexts.messenger.domain.aggregates.conversation import Conversation
from contexts.messenger.domain.aggregates.message import Message
from shared.domain.value_objects.unique_id import UniqueId


class IConversationRepository(Protocol):
    async def save(self, conversation: Conversation) -> None: ...
    async def find_by_id(self, tenant_id: str, conversation_id: UniqueId) -> Conversation | None: ...


class IMessageRepository(Protocol):
    async def save(self, message: Message) -> None: ...
    async def list_by_conversation(
        self, tenant_id: str, conversation_id: UniqueId, *, limit: int = 50
    ) -> list[Message]: ...
