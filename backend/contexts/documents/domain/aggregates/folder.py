"""Folder aggregate — document hierarchy."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class Folder(AggregateRoot):
    tenant_id: str
    parent_id: UniqueId | None
    name: str
    is_root: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        name: str,
        parent_id: UniqueId | None = None,
        is_root: bool = False,
    ) -> Folder:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            parent_id=parent_id,
            name=name.strip(),
            is_root=is_root,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "parent_id": str(self.parent_id) if self.parent_id else None,
            "name": self.name,
            "is_root": self.is_root,
            "created_at": self.created_at.isoformat(),
        }
