"""Org unit — branch, department, ward, cost center."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class OrgUnitType(StrEnum):
    ROOT = "root"
    BRANCH = "branch"
    DEPARTMENT = "department"
    WARD = "ward"
    COST_CENTER = "cost_center"


@dataclass(eq=False, kw_only=True)
class OrgUnit(AggregateRoot):
    tenant_id: str
    organization_id: UniqueId
    parent_id: UniqueId | None
    unit_type: OrgUnitType
    code: str
    name: str
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        organization_id: UniqueId,
        parent_id: UniqueId | None,
        unit_type: OrgUnitType,
        code: str,
        name: str,
    ) -> OrgUnit:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            organization_id=organization_id,
            parent_id=parent_id,
            unit_type=unit_type,
            code=code.strip().upper(),
            name=name.strip(),
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "organization_id": str(self.organization_id),
            "parent_id": str(self.parent_id) if self.parent_id else None,
            "unit_type": self.unit_type.value,
            "code": self.code,
            "name": self.name,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
        }
