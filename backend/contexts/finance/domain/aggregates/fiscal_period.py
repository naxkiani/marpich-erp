"""Fiscal period aggregate."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId

from contexts.finance.domain.events.integration_events import PeriodClosedIntegration


class PeriodStatus(StrEnum):
    OPEN = "open"
    CLOSED = "closed"


@dataclass(eq=False, kw_only=True)
class FiscalPeriod(AggregateRoot):
    tenant_id: str
    name: str
    start_date: str
    end_date: str
    status: PeriodStatus = PeriodStatus.OPEN
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    closed_at: datetime | None = None

    @classmethod
    def open_period(
        cls,
        *,
        tenant_id: str,
        name: str,
        start_date: str,
        end_date: str,
    ) -> FiscalPeriod:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            name=name.strip(),
            start_date=start_date,
            end_date=end_date,
        )

    def close(self, correlation_id: str) -> PeriodClosedIntegration:
        if self.status == PeriodStatus.CLOSED:
            raise ValueError("Period already closed")
        self.status = PeriodStatus.CLOSED
        self.closed_at = datetime.now(UTC)
        return PeriodClosedIntegration(
            tenant_id=TenantId.create(self.tenant_id),
            correlation_id=correlation_id,
            period_id=self.id,
            period_name=self.name,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "name": self.name,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "closed_at": self.closed_at.isoformat() if self.closed_at else None,
        }
