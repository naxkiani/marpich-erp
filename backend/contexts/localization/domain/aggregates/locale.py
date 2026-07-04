"""Locale aggregate."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class TextDirection(StrEnum):
    LTR = "ltr"
    RTL = "rtl"


@dataclass(eq=False, kw_only=True)
class Locale(AggregateRoot):
    tenant_id: str
    code: str
    name: str
    direction: TextDirection
    is_default: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        code: str,
        name: str,
        direction: TextDirection,
        is_default: bool = False,
    ) -> Locale:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            code=code.strip().lower(),
            name=name.strip(),
            direction=direction,
            is_default=is_default,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "code": self.code,
            "name": self.name,
            "direction": self.direction.value,
            "is_default": self.is_default,
            "created_at": self.created_at.isoformat(),
        }
