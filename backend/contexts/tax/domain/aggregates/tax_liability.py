"""TaxLiability aggregate — CAP-ENT-026 (peer payroll_run_id only)."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from decimal import Decimal
from enum import StrEnum

from contexts.tax.domain.events.integration_events import TaxLiabilityCalculatedIntegration
from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId


class TaxLiabilityStatus(StrEnum):
    OPEN = "open"
    FILED = "filed"


@dataclass(eq=False, kw_only=True)
class TaxLiability(AggregateRoot):
    tenant_id: str
    payroll_run_id: UniqueId
    period_label: str
    taxable_base: Decimal
    tax_amount: Decimal
    currency: str = "USD"
    status: TaxLiabilityStatus = TaxLiabilityStatus.OPEN
    correlation_id: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def calculate_from_payroll(
        cls,
        *,
        tenant_id: str,
        payroll_run_id: UniqueId,
        period_label: str,
        taxable_base: Decimal,
        currency: str,
        correlation_id: str,
        rate: Decimal = Decimal("0.10"),
    ) -> tuple["TaxLiability", TaxLiabilityCalculatedIntegration]:
        if taxable_base < 0:
            raise ValueError("tax.errors.invalid_base")
        label = period_label.strip()
        if not label:
            raise ValueError("tax.errors.invalid_period")
        amount = (taxable_base * rate).quantize(Decimal("0.01"))
        liability = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            payroll_run_id=payroll_run_id,
            period_label=label,
            taxable_base=taxable_base,
            tax_amount=amount,
            currency=(currency or "USD").strip().upper(),
            correlation_id=correlation_id,
        )
        event = TaxLiabilityCalculatedIntegration(
            tenant_id=TenantId.create(tenant_id),
            correlation_id=correlation_id,
            liability_id=liability.id,
            payroll_run_id=payroll_run_id,
            period_label=label,
            taxable_base=str(taxable_base),
            tax_amount=str(amount),
            currency=liability.currency,
        )
        return liability, event

    def mark_filed(self) -> None:
        if self.status != TaxLiabilityStatus.OPEN:
            raise ValueError("tax.errors.liability_not_open")
        self.status = TaxLiabilityStatus.FILED
        self.updated_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "payroll_run_id": str(self.payroll_run_id),
            "period_label": self.period_label,
            "taxable_base": str(self.taxable_base),
            "tax_amount": str(self.tax_amount),
            "currency": self.currency,
            "status": self.status.value,
            "correlation_id": self.correlation_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
