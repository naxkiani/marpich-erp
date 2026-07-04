"""Tenant retention rules for audit logs."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot


@dataclass(eq=False, kw_only=True)
class RetentionPolicy(AggregateRoot):
    tenant_id: str
    retention_days: int
    is_active: bool = True
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def default_for_tenant(cls, tenant_id: str) -> RetentionPolicy:
        from shared.domain.value_objects.unique_id import UniqueId

        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            retention_days=2555,  # ~7 years SOX default
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "retention_days": self.retention_days,
            "is_active": self.is_active,
            "updated_at": self.updated_at.isoformat(),
        }
