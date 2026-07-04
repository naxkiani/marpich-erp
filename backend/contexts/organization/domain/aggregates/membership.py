"""User membership in org unit."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class Membership(AggregateRoot):
    tenant_id: str
    org_unit_id: UniqueId
    user_id: str
    title: str
    is_primary: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def assign(
        cls,
        *,
        tenant_id: str,
        org_unit_id: UniqueId,
        user_id: str,
        title: str,
        is_primary: bool = False,
    ) -> Membership:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            org_unit_id=org_unit_id,
            user_id=user_id,
            title=title.strip(),
            is_primary=is_primary,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "org_unit_id": str(self.org_unit_id),
            "user_id": self.user_id,
            "title": self.title,
            "is_primary": self.is_primary,
            "created_at": self.created_at.isoformat(),
        }
