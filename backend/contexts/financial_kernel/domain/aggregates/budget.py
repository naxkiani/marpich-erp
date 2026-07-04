"""Budget and recurring journal aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class Budget(AggregateRoot):
    tenant_id: str
    organization_id: str | None
    period_id: str
    account_code: str
    cost_center: str | None
    amount: float
    consumed: float = 0.0
    currency: str = "USD"
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        organization_id: str | None,
        period_id: str,
        account_code: str,
        amount: float,
        cost_center: str | None = None,
        currency: str = "USD",
    ) -> Budget:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            organization_id=organization_id,
            period_id=period_id,
            account_code=account_code,
            cost_center=cost_center,
            amount=amount,
            currency=currency,
        )

    @property
    def remaining(self) -> float:
        return round(self.amount - self.consumed, 2)

    def consume(self, amount: float) -> bool:
        if self.consumed + amount > self.amount:
            return False
        self.consumed = round(self.consumed + amount, 2)
        return True

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "organization_id": self.organization_id,
            "period_id": self.period_id,
            "account_code": self.account_code,
            "cost_center": self.cost_center,
            "amount": self.amount,
            "consumed": self.consumed,
            "remaining": self.remaining,
            "currency": self.currency,
        }


@dataclass(eq=False, kw_only=True)
class RecurringJournal(AggregateRoot):
    tenant_id: str
    organization_id: str | None
    name: str
    schedule: str
    currency: str
    base_currency: str
    lines: list[dict]
    requires_approval: bool = False
    is_active: bool = True
    last_run_at: datetime | None = None
    run_count: int = 0
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        organization_id: str | None,
        name: str,
        schedule: str,
        currency: str,
        base_currency: str,
        lines: list[dict],
        requires_approval: bool = False,
    ) -> RecurringJournal:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            organization_id=organization_id,
            name=name,
            schedule=schedule,
            currency=currency,
            base_currency=base_currency,
            lines=lines,
            requires_approval=requires_approval,
        )

    def record_run(self) -> None:
        self.last_run_at = datetime.now(UTC)
        self.run_count += 1

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "organization_id": self.organization_id,
            "name": self.name,
            "schedule": self.schedule,
            "currency": self.currency,
            "base_currency": self.base_currency,
            "lines": self.lines,
            "requires_approval": self.requires_approval,
            "is_active": self.is_active,
            "run_count": self.run_count,
            "last_run_at": self.last_run_at.isoformat() if self.last_run_at else None,
        }
