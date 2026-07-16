"""Messenger conversation aggregate — text rooms (LiveKit via Integration)."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class Conversation(AggregateRoot):
    tenant_id: str
    title: str
    member_ids: list[str]
    e2ee_enabled: bool = False
    livekit_room_name: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def open(
        cls,
        *,
        tenant_id: str,
        title: str,
        member_ids: list[str],
        e2ee_enabled: bool = False,
    ) -> Conversation:
        members = sorted({m.strip() for m in member_ids if m and m.strip()})
        if len(members) < 1:
            raise ValueError("messenger.errors.members_required")
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            title=title.strip() or "Conversation",
            member_ids=members,
            e2ee_enabled=e2ee_enabled,
            livekit_room_name=None,
        )

    def attach_livekit_room(self, room_name: str) -> None:
        self.livekit_room_name = room_name

    def ensure_member(self, user_id: str) -> None:
        if user_id not in self.member_ids:
            raise ValueError("messenger.errors.not_a_member")

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "title": self.title,
            "member_ids": list(self.member_ids),
            "e2ee_enabled": self.e2ee_enabled,
            "livekit_room_name": self.livekit_room_name,
            "created_at": self.created_at.isoformat(),
        }
