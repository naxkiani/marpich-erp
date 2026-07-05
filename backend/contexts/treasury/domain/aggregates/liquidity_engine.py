"""Enterprise Liquidity Engine aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class LiquidityPeriod(StrEnum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class CashPoolStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class FundingNeedStatus(StrEnum):
    OPEN = "open"
    FUNDED = "funded"
    CANCELLED = "cancelled"


@dataclass(eq=False, kw_only=True)
class CashPool(AggregateRoot):
    tenant_id: str
    code: str
    name: str
    currency: str
    target_balance: float
    minimum_balance: float
    member_account_ids: list[str]
    status: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        code: str,
        name: str,
        currency: str = "USD",
        target_balance: float = 0.0,
        minimum_balance: float = 0.0,
        member_account_ids: list[str] | None = None,
    ) -> CashPool:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            code=code.strip().upper(),
            name=name.strip(),
            currency=currency.strip().upper(),
            target_balance=round(target_balance, 2),
            minimum_balance=round(minimum_balance, 2),
            member_account_ids=member_account_ids or [],
            status=CashPoolStatus.ACTIVE.value,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "code": self.code,
            "name": self.name,
            "currency": self.currency,
            "target_balance": self.target_balance,
            "minimum_balance": self.minimum_balance,
            "member_account_ids": self.member_account_ids,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class LiquiditySnapshot(AggregateRoot):
    tenant_id: str
    period_type: str
    as_of_date: str
    currency: str
    opening_balance: float
    closing_balance: float
    total_inflow: float
    total_outflow: float
    liquidity_gap: float
    working_capital: float
    lines: list[dict]
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        period_type: str,
        as_of_date: str,
        currency: str,
        opening_balance: float,
        closing_balance: float,
        total_inflow: float,
        total_outflow: float,
        liquidity_gap: float,
        working_capital: float,
        lines: list[dict],
    ) -> LiquiditySnapshot:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            period_type=period_type,
            as_of_date=as_of_date,
            currency=currency.strip().upper(),
            opening_balance=round(opening_balance, 2),
            closing_balance=round(closing_balance, 2),
            total_inflow=round(total_inflow, 2),
            total_outflow=round(total_outflow, 2),
            liquidity_gap=round(liquidity_gap, 2),
            working_capital=round(working_capital, 2),
            lines=lines,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "period_type": self.period_type,
            "as_of_date": self.as_of_date,
            "currency": self.currency,
            "opening_balance": self.opening_balance,
            "closing_balance": self.closing_balance,
            "total_inflow": self.total_inflow,
            "total_outflow": self.total_outflow,
            "liquidity_gap": self.liquidity_gap,
            "working_capital": self.working_capital,
            "lines": self.lines,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class FundingNeed(AggregateRoot):
    tenant_id: str
    label: str
    currency: str
    required_amount: float
    available_amount: float
    gap_amount: float
    due_date: str
    status: str
    source: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        label: str,
        currency: str,
        required_amount: float,
        available_amount: float,
        due_date: str,
        source: str = "liquidity_engine",
    ) -> FundingNeed:
        gap = round(required_amount - available_amount, 2)
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            label=label,
            currency=currency.strip().upper(),
            required_amount=round(required_amount, 2),
            available_amount=round(available_amount, 2),
            gap_amount=max(gap, 0),
            due_date=due_date,
            status=FundingNeedStatus.OPEN.value if gap > 0 else FundingNeedStatus.FUNDED.value,
            source=source,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "label": self.label,
            "currency": self.currency,
            "required_amount": self.required_amount,
            "available_amount": self.available_amount,
            "gap_amount": self.gap_amount,
            "due_date": self.due_date,
            "status": self.status,
            "source": self.source,
            "created_at": self.created_at.isoformat(),
        }
