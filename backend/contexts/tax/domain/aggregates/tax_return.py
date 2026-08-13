"""TaxReturn aggregate — CAP-ENT-026 file return."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from decimal import Decimal
from enum import StrEnum

from contexts.tax.domain.events.integration_events import TaxReturnFiledIntegration
from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId


class TaxReturnStatus(StrEnum):
    DRAFT = "draft"
    FILED = "filed"


@dataclass(eq=False, kw_only=True)
class TaxReturn(AggregateRoot):
    tenant_id: str
    period_label: str
    status: TaxReturnStatus = TaxReturnStatus.DRAFT
    liability_ids: list[UniqueId] = field(default_factory=list)
    total_tax: Decimal = Decimal("0")
    currency: str = "USD"
    correlation_id: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    filed_at: datetime | None = None

    @classmethod
    def draft(
        cls,
        *,
        tenant_id: str,
        period_label: str,
        liability_ids: list[UniqueId],
        total_tax: Decimal,
        currency: str = "USD",
    ) -> TaxReturn:
        label = period_label.strip()
        if not label:
            raise ValueError("tax.errors.invalid_period")
        if not liability_ids:
            raise ValueError("tax.errors.no_liabilities")
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            period_label=label,
            liability_ids=list(liability_ids),
            total_tax=total_tax,
            currency=(currency or "USD").strip().upper(),
        )

    def file(self, *, correlation_id: str) -> TaxReturnFiledIntegration:
        if self.status != TaxReturnStatus.DRAFT:
            raise ValueError("tax.errors.return_not_draft")
        self.status = TaxReturnStatus.FILED
        self.filed_at = datetime.now(UTC)
        self.updated_at = self.filed_at
        self.correlation_id = correlation_id or self.correlation_id
        return TaxReturnFiledIntegration(
            tenant_id=TenantId.create(self.tenant_id),
            correlation_id=self.correlation_id,
            return_id=self.id,
            period_label=self.period_label,
            liability_count=len(self.liability_ids),
            total_tax=str(self.total_tax),
            currency=self.currency,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "period_label": self.period_label,
            "status": self.status.value,
            "liability_ids": [str(i) for i in self.liability_ids],
            "liability_count": len(self.liability_ids),
            "total_tax": str(self.total_tax),
            "currency": self.currency,
            "correlation_id": self.correlation_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "filed_at": self.filed_at.isoformat() if self.filed_at else None,
        }
