"""Messenger message aggregate."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class Message(AggregateRoot):
    tenant_id: str
    conversation_id: UniqueId
    sender_id: str
    body: str
    ciphertext: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def send(
        cls,
        *,
        tenant_id: str,
        conversation_id: UniqueId,
        sender_id: str,
        body: str,
        e2ee_enabled: bool = False,
    ) -> Message:
        text = body.strip()
        if not text:
            raise ValueError("messenger.errors.empty_message")
        ciphertext = f"e2ee:{hash(text) & 0xFFFFFFFF:08x}" if e2ee_enabled else None
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            conversation_id=conversation_id,
            sender_id=sender_id,
            body="" if e2ee_enabled else text,
            ciphertext=ciphertext,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "conversation_id": str(self.conversation_id),
            "sender_id": self.sender_id,
            "body": self.body,
            "ciphertext": self.ciphertext,
            "created_at": self.created_at.isoformat(),
        }
