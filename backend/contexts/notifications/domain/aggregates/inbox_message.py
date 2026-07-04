"""In-app inbox message aggregate."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class InboxStatus(StrEnum):
    UNREAD = "unread"
    READ = "read"
    ARCHIVED = "archived"


@dataclass(eq=False, kw_only=True)
class InboxMessage(AggregateRoot):
    tenant_id: str
    user_id: str | None
    channel: str
    title: str
    body: str
    category: str
    source_event: str
    status: InboxStatus = InboxStatus.UNREAD
    metadata: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    read_at: datetime | None = None

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        user_id: str | None,
        channel: str,
        title: str,
        body: str,
        category: str,
        source_event: str,
        metadata: dict | None = None,
    ) -> InboxMessage:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            user_id=user_id,
            channel=channel,
            title=title,
            body=body,
            category=category,
            source_event=source_event,
            metadata=metadata or {},
        )

    def mark_read(self) -> None:
        if self.status == InboxStatus.UNREAD:
            self.status = InboxStatus.READ
            self.read_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "user_id": self.user_id,
            "channel": self.channel,
            "title": self.title,
            "body": self.body,
            "category": self.category,
            "source_event": self.source_event,
            "status": self.status.value,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "read_at": self.read_at.isoformat() if self.read_at else None,
        }
