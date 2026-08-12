"""Payroll employee projection — CAP-ENT-015 (peer hr_employee_id only)."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class PayrollEmployeeStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"


@dataclass(eq=False, kw_only=True)
class PayrollEmployee(AggregateRoot):
    tenant_id: str
    hr_employee_id: UniqueId
    email: str
    full_name: str
    job_title: str = ""
    department: str = ""
    employee_number: str = ""
    status: PayrollEmployeeStatus = PayrollEmployeeStatus.ACTIVE
    base_salary: str = "5000.00"
    currency: str = "USD"
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def project_from_hire(
        cls,
        *,
        tenant_id: str,
        hr_employee_id: UniqueId,
        email: str,
        full_name: str,
        job_title: str = "",
        department: str = "",
        employee_number: str = "",
        base_salary: str = "5000.00",
        currency: str = "USD",
    ) -> PayrollEmployee:
        email_norm = email.strip().lower()
        if not email_norm:
            raise ValueError("payroll.errors.invalid_email")
        name = full_name.strip()
        if not name:
            raise ValueError("payroll.errors.invalid_name")
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            hr_employee_id=hr_employee_id,
            email=email_norm,
            full_name=name,
            job_title=(job_title or "").strip(),
            department=(department or "").strip(),
            employee_number=(employee_number or "").strip(),
            base_salary=str(base_salary),
            currency=(currency or "USD").strip().upper(),
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "hr_employee_id": str(self.hr_employee_id),
            "email": self.email,
            "full_name": self.full_name,
            "job_title": self.job_title,
            "department": self.department,
            "employee_number": self.employee_number,
            "status": self.status.value,
            "base_salary": self.base_salary,
            "currency": self.currency,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
