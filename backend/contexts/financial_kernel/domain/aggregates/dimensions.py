"""Cost and profit center aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class CostCenter(AggregateRoot):
    tenant_id: str
    code: str
    name: str
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(cls, *, tenant_id: str, code: str, name: str) -> CostCenter:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            code=code.strip(),
            name=name.strip(),
        )

    def to_dict(self) -> dict:
        return {"id": str(self.id), "tenant_id": self.tenant_id, "code": self.code, "name": self.name}


@dataclass(eq=False, kw_only=True)
class ProfitCenter(AggregateRoot):
    tenant_id: str
    code: str
    name: str
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(cls, *, tenant_id: str, code: str, name: str) -> ProfitCenter:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            code=code.strip(),
            name=name.strip(),
        )

    def to_dict(self) -> dict:
        return {"id": str(self.id), "tenant_id": self.tenant_id, "code": self.code, "name": self.name}
