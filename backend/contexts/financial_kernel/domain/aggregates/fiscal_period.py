"""Fiscal year and period aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from contexts.financial_kernel.domain.aggregates.fiscal_calendar import (
    CloseLevel,
    PeriodStatus,
    PeriodType,
)
from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class FiscalYear(AggregateRoot):
    tenant_id: str
    organization_id: str | None
    calendar_id: str | None = None
    name: str
    start_date: str
    end_date: str
    status: str = "open"
    close_level: str = CloseLevel.NONE.value
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
        calendar_id: str | None = None,
    ) -> FiscalYear:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            organization_id=organization_id,
            calendar_id=calendar_id,
            name=name,
            start_date=start_date,
            end_date=end_date,
        )

    def close_year(self) -> None:
        self.status = "closed"
        self.close_level = CloseLevel.YEAR.value

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "organization_id": self.organization_id,
            "calendar_id": self.calendar_id,
            "name": self.name,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "status": self.status,
            "close_level": self.close_level,
        }


@dataclass(eq=False, kw_only=True)
class FiscalPeriod(AggregateRoot):
    tenant_id: str
    organization_id: str | None
    branch_id: str | None
    fiscal_year_id: str
    calendar_id: str | None = None
    name: str
    start_date: str
    end_date: str
    status: str = PeriodStatus.OPEN.value
    period_type: str = PeriodType.MONTHLY.value
    close_level: str = CloseLevel.NONE.value
    period_number: int = 1
    is_adjustment: bool = False
    is_financially_locked: bool = False
    locked_at: datetime | None = None
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
        calendar_id: str | None = None,
        period_type: str = PeriodType.MONTHLY.value,
        period_number: int = 1,
        is_adjustment: bool = False,
    ) -> FiscalPeriod:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            organization_id=organization_id,
            branch_id=branch_id,
            fiscal_year_id=fiscal_year_id,
            calendar_id=calendar_id,
            name=name,
            start_date=start_date,
            end_date=end_date,
            status=PeriodStatus.OPEN.value,
            period_type=period_type,
            period_number=period_number,
            is_adjustment=is_adjustment,
        )

    def soft_close(self, *, close_level: str = CloseLevel.MONTHLY.value) -> None:
        if self.status in (PeriodStatus.HARD_CLOSED.value, PeriodStatus.CLOSED.value):
            raise ValueError("period_hard_closed")
        self.status = PeriodStatus.SOFT_CLOSED.value
        self.close_level = close_level
        self._apply_financial_lock()

    def hard_close(self, *, close_level: str = CloseLevel.YEAR.value) -> None:
        self.status = PeriodStatus.HARD_CLOSED.value
        self.close_level = close_level
        self._apply_financial_lock()

    def close(self) -> None:
        self.status = PeriodStatus.CLOSED.value
        self.close_level = CloseLevel.MONTHLY.value
        self._apply_financial_lock()

    def reopen(self) -> None:
        if not self.is_financially_locked:
            pass
        self.status = PeriodStatus.OPEN.value
        self.close_level = CloseLevel.NONE.value
        self.is_financially_locked = False
        self.locked_at = None

    def apply_financial_lock(self) -> None:
        self._apply_financial_lock()

    def release_financial_lock(self) -> None:
        self.is_financially_locked = False
        self.locked_at = None

    def _apply_financial_lock(self) -> None:
        self.is_financially_locked = True
        self.locked_at = datetime.now(UTC)

    @property
    def accepts_posting(self) -> bool:
        return self.status == PeriodStatus.OPEN.value

    @property
    def accepts_adjustments(self) -> bool:
        return self.status in (
            PeriodStatus.OPEN.value,
            PeriodStatus.SOFT_CLOSED.value,
        ) or self.is_adjustment

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "organization_id": self.organization_id,
            "branch_id": self.branch_id,
            "fiscal_year_id": self.fiscal_year_id,
            "calendar_id": self.calendar_id,
            "name": self.name,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "status": self.status,
            "period_type": self.period_type,
            "close_level": self.close_level,
            "period_number": self.period_number,
            "is_adjustment": self.is_adjustment,
            "is_financially_locked": self.is_financially_locked,
            "locked_at": self.locked_at.isoformat() if self.locked_at else None,
            "accepts_posting": self.accepts_posting,
            "accepts_adjustments": self.accepts_adjustments,
        }
