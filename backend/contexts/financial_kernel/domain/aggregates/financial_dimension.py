"""Enterprise financial dimension aggregates — unlimited dimensions per journal line."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class DimensionType(StrEnum):
    COMPANY = "company"
    BRANCH = "branch"
    DEPARTMENT = "department"
    PROJECT = "project"
    COST_CENTER = "cost_center"
    PROFIT_CENTER = "profit_center"
    FUND = "fund"
    GRANT = "grant"
    FACULTY = "faculty"
    HOSPITAL = "hospital"
    WARD = "ward"
    CONSTRUCTION_SITE = "construction_site"
    WAREHOUSE = "warehouse"
    COUNTRY = "country"
    CURRENCY = "currency"
    BUSINESS_UNIT = "business_unit"


@dataclass(eq=False, kw_only=True)
class DimensionValue(AggregateRoot):
    tenant_id: str
    dimension_type: str
    code: str
    name: str
    parent_id: str | None
    is_active: bool
    metadata: dict
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        dimension_type: str,
        code: str,
        name: str,
        parent_id: str | None = None,
        metadata: dict | None = None,
    ) -> DimensionValue:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            dimension_type=dimension_type,
            code=code.strip().upper(),
            name=name.strip(),
            parent_id=parent_id,
            is_active=True,
            metadata=metadata or {},
        )

    def deactivate(self) -> None:
        self.is_active = False
        self.updated_at = datetime.now(UTC)

    def activate(self) -> None:
        self.is_active = True
        self.updated_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "dimension_type": self.dimension_type,
            "code": self.code,
            "name": self.name,
            "parent_id": self.parent_id,
            "is_active": self.is_active,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class DimensionAuditLog(AggregateRoot):
    tenant_id: str
    dimension_value_id: str
    action: str
    actor_id: str
    before_state: dict | None
    after_state: dict | None
    notes: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def record(
        cls,
        *,
        tenant_id: str,
        dimension_value_id: str,
        action: str,
        actor_id: str,
        before_state: dict | None = None,
        after_state: dict | None = None,
        notes: str = "",
    ) -> DimensionAuditLog:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            dimension_value_id=dimension_value_id,
            action=action,
            actor_id=actor_id,
            before_state=before_state,
            after_state=after_state,
            notes=notes,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "dimension_value_id": self.dimension_value_id,
            "action": self.action,
            "actor_id": self.actor_id,
            "before_state": self.before_state,
            "after_state": self.after_state,
            "notes": self.notes,
            "created_at": self.created_at.isoformat(),
        }
