"""Messenger integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(frozen=True, kw_only=True)
class MessageSentIntegration(IntegrationEvent):
    conversation_id: UniqueId
    message_id: UniqueId
    sender_id: str

    @property
    def event_name(self) -> str:
        return "messenger.message.sent"

    @property
    def source_context(self) -> str:
        return "messenger"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "conversation_id": str(self.conversation_id),
            "message_id": str(self.message_id),
            "sender_id": self.sender_id,
        }


@dataclass(frozen=True, kw_only=True)
class ConversationOpenedIntegration(IntegrationEvent):
    conversation_id: UniqueId
    title: str
    e2ee_enabled: bool

    @property
    def event_name(self) -> str:
        return "messenger.conversation.opened"

    @property
    def source_context(self) -> str:
        return "messenger"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "conversation_id": str(self.conversation_id),
            "title": self.title,
            "e2ee_enabled": self.e2ee_enabled,
        }
