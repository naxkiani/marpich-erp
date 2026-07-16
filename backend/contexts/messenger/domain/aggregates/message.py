"""Messenger message aggregate — E2EE stores client ciphertext only."""
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
    ciphertext_type: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def send(
        cls,
        *,
        tenant_id: str,
        conversation_id: UniqueId,
        sender_id: str,
        body: str = "",
        ciphertext: str | None = None,
        ciphertext_type: str | None = None,
        e2ee_enabled: bool = False,
    ) -> Message:
        plain = (body or "").strip()
        cipher = (ciphertext or "").strip() or None
        ctype = (ciphertext_type or "").strip() or None

        if e2ee_enabled:
            if not cipher:
                raise ValueError("messenger.errors.ciphertext_required")
            if plain:
                raise ValueError("messenger.errors.plaintext_forbidden_when_e2ee")
            return cls(
                id=UniqueId.generate(),
                tenant_id=tenant_id,
                conversation_id=conversation_id,
                sender_id=sender_id,
                body="",
                ciphertext=cipher,
                ciphertext_type=ctype or "application/octet-stream",
            )

        if not plain:
            raise ValueError("messenger.errors.empty_message")
        if cipher:
            raise ValueError("messenger.errors.ciphertext_without_e2ee")
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            conversation_id=conversation_id,
            sender_id=sender_id,
            body=plain,
            ciphertext=None,
            ciphertext_type=None,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "conversation_id": str(self.conversation_id),
            "sender_id": self.sender_id,
            "body": self.body,
            "ciphertext": self.ciphertext,
            "ciphertext_type": self.ciphertext_type,
            "created_at": self.created_at.isoformat(),
        }
