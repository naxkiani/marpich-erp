"""Messenger in-memory stores."""
from __future__ import annotations

from contexts.messenger.domain.aggregates.conversation import Conversation
from contexts.messenger.domain.aggregates.message import Message
from contexts.messenger.domain.ports.repositories import IConversationRepository, IMessageRepository
from shared.domain.value_objects.unique_id import UniqueId


class MessengerMemoryStore:
    conversations: dict[str, Conversation] = {}
    messages: dict[str, Message] = {}

    @classmethod
    def reset(cls) -> None:
        cls.conversations.clear()
        cls.messages.clear()


class InMemoryConversationRepository(IConversationRepository):
    async def save(self, conversation: Conversation) -> None:
        MessengerMemoryStore.conversations[str(conversation.id)] = conversation

    async def find_by_id(self, tenant_id: str, conversation_id: UniqueId) -> Conversation | None:
        row = MessengerMemoryStore.conversations.get(str(conversation_id))
        if row and row.tenant_id == tenant_id:
            return row
        return None


class InMemoryMessageRepository(IMessageRepository):
    async def save(self, message: Message) -> None:
        MessengerMemoryStore.messages[str(message.id)] = message

    async def list_by_conversation(
        self, tenant_id: str, conversation_id: UniqueId, *, limit: int = 50
    ) -> list[Message]:
        rows = [
            m
            for m in MessengerMemoryStore.messages.values()
            if m.tenant_id == tenant_id and m.conversation_id == conversation_id
        ]
        rows.sort(key=lambda m: m.created_at)
        return rows[-limit:]
