"""Payroll integration events — CAP-ENT-015."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(frozen=True, kw_only=True)
class PayrollRunCompletedIntegration(IntegrationEvent):
    run_id: UniqueId
    period_label: str
    employee_count: int
    total_gross: str
    total_net: str
    currency: str

    @property
    def event_name(self) -> str:
        return "payroll.run.completed"

    @property
    def source_context(self) -> str:
        return "payroll"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "run_id": str(self.run_id),
            "period_label": self.period_label,
            "employee_count": self.employee_count,
            "total_gross": self.total_gross,
            "total_net": self.total_net,
            "currency": self.currency,
        }


@dataclass(frozen=True, kw_only=True)
class PayslipGeneratedIntegration(IntegrationEvent):
    run_id: UniqueId
    payroll_employee_id: UniqueId
    hr_employee_id: UniqueId
    gross: str
    net: str
    currency: str

    @property
    def event_name(self) -> str:
        return "payroll.payslip.generated"

    @property
    def source_context(self) -> str:
        return "payroll"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "run_id": str(self.run_id),
            "payroll_employee_id": str(self.payroll_employee_id),
            "hr_employee_id": str(self.hr_employee_id),
            "gross": self.gross,
            "net": self.net,
            "currency": self.currency,
        }
