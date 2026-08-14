"""HR Employee aggregate — CAP-ENT-010 Employee Management."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from contexts.human_resources.domain.events.integration_events import (
    EmployeeHiredIntegration,
    EmployeeTerminatedIntegration,
)
from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId


class EmployeeStatus(StrEnum):
    ACTIVE = "active"
    TERMINATED = "terminated"


@dataclass(eq=False, kw_only=True)
class Employee(AggregateRoot):
    tenant_id: str
    email: str
    full_name: str
    job_title: str = ""
    department: str = ""
    employee_number: str = ""
    status: EmployeeStatus = EmployeeStatus.ACTIVE
    hired_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    terminated_at: datetime | None = None
    termination_reason: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def hire(
        cls,
        *,
        tenant_id: str,
        email: str,
        full_name: str,
        job_title: str = "",
        department: str = "",
        employee_number: str = "",
    ) -> tuple[Employee, EmployeeHiredIntegration]:
        email_norm = email.strip().lower()
        if not email_norm or "@" not in email_norm:
            raise ValueError("human_resources.errors.invalid_email")
        name = full_name.strip()
        if not name:
            raise ValueError("human_resources.errors.invalid_name")
        employee = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            email=email_norm,
            full_name=name,
            job_title=(job_title or "").strip(),
            department=(department or "").strip(),
            employee_number=(employee_number or "").strip(),
        )
        event = EmployeeHiredIntegration(
            tenant_id=TenantId.create(tenant_id),
            correlation_id="",
            employee_id=employee.id,
            email=employee.email,
            full_name=employee.full_name,
            job_title=employee.job_title,
            department=employee.department,
            employee_number=employee.employee_number,
        )
        return employee, event

    def terminate(self, *, correlation_id: str, reason: str = "") -> EmployeeTerminatedIntegration:
        if self.status != EmployeeStatus.ACTIVE:
            raise ValueError("human_resources.errors.employee_not_active")
        self.status = EmployeeStatus.TERMINATED
        self.terminated_at = datetime.now(UTC)
        self.updated_at = self.terminated_at
        self.termination_reason = (reason or "").strip()
        return EmployeeTerminatedIntegration(
            tenant_id=TenantId.create(self.tenant_id),
            correlation_id=correlation_id,
            employee_id=self.id,
            email=self.email,
            full_name=self.full_name,
            reason=self.termination_reason,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "email": self.email,
            "full_name": self.full_name,
            "job_title": self.job_title,
            "department": self.department,
            "employee_number": self.employee_number,
            "status": self.status.value,
            "hired_at": self.hired_at.isoformat(),
            "terminated_at": self.terminated_at.isoformat() if self.terminated_at else None,
            "termination_reason": self.termination_reason,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
