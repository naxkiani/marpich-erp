"""Human Resources integration events — CAP-ENT-010."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(frozen=True, kw_only=True)
class EmployeeHiredIntegration(IntegrationEvent):
    employee_id: UniqueId
    email: str
    full_name: str
    job_title: str = ""
    department: str = ""
    employee_number: str = ""

    @property
    def event_name(self) -> str:
        return "human_resources.employee.hired"

    @property
    def source_context(self) -> str:
        return "human_resources"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "employee_id": str(self.employee_id),
            "email": self.email,
            "full_name": self.full_name,
            "job_title": self.job_title,
            "department": self.department,
            "employee_number": self.employee_number,
        }


@dataclass(frozen=True, kw_only=True)
class EmployeeTerminatedIntegration(IntegrationEvent):
    employee_id: UniqueId
    email: str
    full_name: str
    reason: str = ""

    @property
    def event_name(self) -> str:
        return "human_resources.employee.terminated"

    @property
    def source_context(self) -> str:
        return "human_resources"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "employee_id": str(self.employee_id),
            "email": self.email,
            "full_name": self.full_name,
            "reason": self.reason,
        }
