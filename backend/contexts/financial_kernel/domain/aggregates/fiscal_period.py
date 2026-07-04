"""Fiscal year and period aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class FiscalYear(AggregateRoot):
    tenant_id: str
    organization_id: str | None
    name: str
    start_date: str
    end_date: str
    status: str = "open"
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        organization_id: str | None,
        name: str,
        start_date: str,
        end_date: str,
    ) -> FiscalYear:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            organization_id=organization_id,
            name=name,
            start_date=start_date,
            end_date=end_date,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "organization_id": self.organization_id,
            "name": self.name,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "status": self.status,
        }


@dataclass(eq=False, kw_only=True)
class FiscalPeriod(AggregateRoot):
    tenant_id: str
    organization_id: str | None
    branch_id: str | None
    fiscal_year_id: str
    name: str
    start_date: str
    end_date: str
    status: str = "open"
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def open_period(
        cls,
        *,
        tenant_id: str,
        organization_id: str | None,
        branch_id: str | None,
        fiscal_year_id: str,
        name: str,
        start_date: str,
        end_date: str,
    ) -> FiscalPeriod:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            organization_id=organization_id,
            branch_id=branch_id,
            fiscal_year_id=fiscal_year_id,
            name=name,
            start_date=start_date,
            end_date=end_date,
            status="open",
        )

    def close(self) -> None:
        self.status = "closed"

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "organization_id": self.organization_id,
            "branch_id": self.branch_id,
            "fiscal_year_id": self.fiscal_year_id,
            "name": self.name,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "status": self.status,
        }
