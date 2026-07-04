"""Role aggregate."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class Role(AggregateRoot):
    tenant_id: str
    code: str
    name: str
    description: str | None = None
    is_system: bool = False
    permission_ids: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create_system_admin(cls, tenant_id: str) -> Role:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            code="admin",
            name="Administrator",
            description="Full platform access",
            is_system=True,
            permission_ids=["*"],
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "code": self.code,
            "name": self.name,
            "description": self.description,
            "is_system": self.is_system,
            "permission_ids": self.permission_ids,
        }
