"""PayrollRun aggregate — CAP-ENT-015 pay period completion."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from decimal import Decimal
from enum import StrEnum

from contexts.payroll.domain.events.integration_events import PayrollRunCompletedIntegration
from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId


class PayrollRunStatus(StrEnum):
    DRAFT = "draft"
    COMPLETED = "completed"


@dataclass(eq=False, kw_only=True)
class PayslipLine:
    payroll_employee_id: UniqueId
    hr_employee_id: UniqueId
    email: str
    full_name: str
    gross: Decimal
    net: Decimal
    currency: str

    def to_dict(self) -> dict:
        return {
            "payroll_employee_id": str(self.payroll_employee_id),
            "hr_employee_id": str(self.hr_employee_id),
            "email": self.email,
            "full_name": self.full_name,
            "gross": str(self.gross),
            "net": str(self.net),
            "currency": self.currency,
        }


@dataclass(eq=False, kw_only=True)
class PayrollRun(AggregateRoot):
    tenant_id: str
    period_label: str
    status: PayrollRunStatus = PayrollRunStatus.DRAFT
    payslips: list[PayslipLine] = field(default_factory=list)
    currency: str = "USD"
    total_gross: Decimal = Decimal("0")
    total_net: Decimal = Decimal("0")
    correlation_id: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    completed_at: datetime | None = None

    @classmethod
    def open(cls, *, tenant_id: str, period_label: str, currency: str = "USD") -> PayrollRun:
        label = period_label.strip()
        if not label:
            raise ValueError("payroll.errors.invalid_period")
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            period_label=label,
            currency=(currency or "USD").strip().upper(),
        )

    def complete(
        self, *, correlation_id: str, payslips: list[PayslipLine]
    ) -> PayrollRunCompletedIntegration:
        if self.status != PayrollRunStatus.DRAFT:
            raise ValueError("payroll.errors.run_not_draft")
        if not payslips:
            raise ValueError("payroll.errors.no_employees")
        self.payslips = list(payslips)
        self.total_gross = sum((p.gross for p in payslips), Decimal("0"))
        self.total_net = sum((p.net for p in payslips), Decimal("0"))
        self.status = PayrollRunStatus.COMPLETED
        self.completed_at = datetime.now(UTC)
        self.updated_at = self.completed_at
        self.correlation_id = correlation_id or self.correlation_id
        return PayrollRunCompletedIntegration(
            tenant_id=TenantId.create(self.tenant_id),
            correlation_id=self.correlation_id,
            run_id=self.id,
            period_label=self.period_label,
            employee_count=len(payslips),
            total_gross=str(self.total_gross),
            total_net=str(self.total_net),
            currency=self.currency,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "period_label": self.period_label,
            "status": self.status.value,
            "currency": self.currency,
            "total_gross": str(self.total_gross),
            "total_net": str(self.total_net),
            "employee_count": len(self.payslips),
            "payslips": [p.to_dict() for p in self.payslips],
            "correlation_id": self.correlation_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }
