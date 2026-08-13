"""Tax integration events — CAP-ENT-026."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(frozen=True, kw_only=True)
class TaxLiabilityCalculatedIntegration(IntegrationEvent):
    liability_id: UniqueId
    payroll_run_id: UniqueId
    period_label: str
    taxable_base: str
    tax_amount: str
    currency: str

    @property
    def event_name(self) -> str:
        return "tax.liability.calculated"

    @property
    def source_context(self) -> str:
        return "tax"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "liability_id": str(self.liability_id),
            "payroll_run_id": str(self.payroll_run_id),
            "period_label": self.period_label,
            "taxable_base": self.taxable_base,
            "tax_amount": self.tax_amount,
            "currency": self.currency,
        }


@dataclass(frozen=True, kw_only=True)
class TaxReturnFiledIntegration(IntegrationEvent):
    return_id: UniqueId
    period_label: str
    liability_count: int
    total_tax: str
    currency: str

    @property
    def event_name(self) -> str:
        return "tax.return.filed"

    @property
    def source_context(self) -> str:
        return "tax"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "return_id": str(self.return_id),
            "period_label": self.period_label,
            "liability_count": self.liability_count,
            "total_tax": self.total_tax,
            "currency": self.currency,
        }
