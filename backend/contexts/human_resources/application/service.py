"""Human Resources application service — CAP-ENT-010 Employee Management.

Audit via integration events → Audit Platform (no local audit tables).
"""
from __future__ import annotations

from contexts.human_resources.domain.aggregates.employee import Employee
from contexts.human_resources.domain.events.integration_events import EmployeeHiredIntegration
from contexts.human_resources.domain.ports.repositories import IEmployeeRepository
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class HumanResourcesApplicationService:
    def __init__(self, employees: IEmployeeRepository) -> None:
        self._employees = employees

    async def hire_employee(
        self,
        *,
        tenant_id: str,
        email: str,
        full_name: str,
        correlation_id: str,
        job_title: str = "",
        department: str = "",
        employee_number: str = "",
    ) -> Result[dict]:
        if await self._employees.find_by_email(tenant_id, email):
            return Result.fail("human_resources.errors.employee_email_exists")
        try:
            employee, hired_event = Employee.hire(
                tenant_id=tenant_id,
                email=email,
                full_name=full_name,
                job_title=job_title,
                department=department,
                employee_number=employee_number,
            )
        except ValueError as exc:
            return Result.fail(str(exc))
        await self._employees.save(employee)
        event = EmployeeHiredIntegration(
            tenant_id=TenantId.create(tenant_id),
            correlation_id=correlation_id,
            employee_id=hired_event.employee_id,
            email=hired_event.email,
            full_name=hired_event.full_name,
            job_title=hired_event.job_title,
            department=hired_event.department,
            employee_number=hired_event.employee_number,
        )
        await publish_integration_event(event)
        return Result.ok(employee.to_dict())

    async def list_employees(
        self, tenant_id: str, *, limit: int = 50, offset: int = 0
    ) -> Result[dict]:
        limit = max(1, min(limit, 100))
        offset = max(0, offset)
        items = await self._employees.list_employees(tenant_id)
        page = items[offset : offset + limit]
        return Result.ok(
            {
                "items": [e.to_dict() for e in page],
                "total": len(items),
                "limit": limit,
                "offset": offset,
            }
        )

    async def get_employee(self, tenant_id: str, employee_id: str) -> Result[dict]:
        employee = await self._employees.find_by_id(
            tenant_id, UniqueId.from_string(employee_id)
        )
        if not employee:
            return Result.fail("human_resources.errors.employee_not_found")
        return Result.ok(employee.to_dict())

    async def terminate_employee(
        self,
        *,
        tenant_id: str,
        employee_id: str,
        correlation_id: str,
        reason: str = "",
    ) -> Result[dict]:
        employee = await self._employees.find_by_id(
            tenant_id, UniqueId.from_string(employee_id)
        )
        if not employee:
            return Result.fail("human_resources.errors.employee_not_found")
        try:
            event = employee.terminate(correlation_id=correlation_id, reason=reason)
        except ValueError as exc:
            return Result.fail(str(exc))
        await self._employees.save(employee)
        await publish_integration_event(event)
        return Result.ok(employee.to_dict())
