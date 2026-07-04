"""Enterprise cost and profit center aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class CenterType(StrEnum):
    DEPARTMENT = "department"
    PROJECT = "project"
    BRANCH = "branch"
    FACULTY = "faculty"
    HOSPITAL_WARD = "hospital_ward"
    CONSTRUCTION_SITE = "construction_site"
    WAREHOUSE = "warehouse"
    BUSINESS_UNIT = "business_unit"


class AllocationType(StrEnum):
    BUDGET = "budget"
    EXPENSE = "expense"
    REVENUE = "revenue"


@dataclass(eq=False, kw_only=True)
class EnterpriseCostCenter(AggregateRoot):
    tenant_id: str
    code: str
    name: str
    center_type: str
    parent_id: str | None
    profit_center_id: str | None
    manager_id: str | None
    is_active: bool
    metadata: dict
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        code: str,
        name: str,
        center_type: str,
        parent_id: str | None = None,
        profit_center_id: str | None = None,
        manager_id: str | None = None,
        metadata: dict | None = None,
    ) -> EnterpriseCostCenter:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            code=code.strip().upper(),
            name=name.strip(),
            center_type=center_type,
            parent_id=parent_id,
            profit_center_id=profit_center_id,
            manager_id=manager_id,
            is_active=True,
            metadata=dict(metadata or {}),
        )

    def deactivate(self) -> None:
        self.is_active = False

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "code": self.code,
            "name": self.name,
            "center_type": self.center_type,
            "parent_id": self.parent_id,
            "profit_center_id": self.profit_center_id,
            "manager_id": self.manager_id,
            "is_active": self.is_active,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class EnterpriseProfitCenter(AggregateRoot):
    tenant_id: str
    code: str
    name: str
    business_unit_id: str | None
    is_active: bool
    metadata: dict
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        code: str,
        name: str,
        business_unit_id: str | None = None,
        metadata: dict | None = None,
    ) -> EnterpriseProfitCenter:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            code=code.strip().upper(),
            name=name.strip(),
            business_unit_id=business_unit_id,
            is_active=True,
            metadata=dict(metadata or {}),
        )

    def deactivate(self) -> None:
        self.is_active = False

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "code": self.code,
            "name": self.name,
            "business_unit_id": self.business_unit_id,
            "is_active": self.is_active,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class CenterAllocation(AggregateRoot):
    tenant_id: str
    allocation_type: str
    source_context: str
    source_document_id: str
    idempotency_key: str
    cost_center_code: str
    profit_center_code: str | None
    account_code: str
    amount: float
    currency: str
    period_id: str | None
    description: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        allocation_type: str,
        source_context: str,
        source_document_id: str,
        idempotency_key: str,
        cost_center_code: str,
        account_code: str,
        amount: float,
        currency: str = "USD",
        profit_center_code: str | None = None,
        period_id: str | None = None,
        description: str = "",
    ) -> CenterAllocation:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            allocation_type=allocation_type,
            source_context=source_context,
            source_document_id=source_document_id,
            idempotency_key=idempotency_key,
            cost_center_code=cost_center_code.strip().upper(),
            profit_center_code=profit_center_code.strip().upper() if profit_center_code else None,
            account_code=account_code.strip(),
            amount=round(amount, 2),
            currency=currency.strip().upper(),
            period_id=period_id,
            description=description.strip(),
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "allocation_type": self.allocation_type,
            "source_context": self.source_context,
            "source_document_id": self.source_document_id,
            "idempotency_key": self.idempotency_key,
            "cost_center_code": self.cost_center_code,
            "profit_center_code": self.profit_center_code,
            "account_code": self.account_code,
            "amount": self.amount,
            "currency": self.currency,
            "period_id": self.period_id,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
        }
