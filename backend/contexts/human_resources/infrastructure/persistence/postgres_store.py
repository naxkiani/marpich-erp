"""PostgreSQL repositories — Human Resources (CAP-ENT-010)."""
from __future__ import annotations

from uuid import UUID

from sqlalchemy import select

from contexts.human_resources.domain.aggregates.employee import Employee, EmployeeStatus
from contexts.human_resources.domain.ports.repositories import IEmployeeRepository
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.database.engine import session_scope
from shared.infrastructure.database.orm import HrEmployeeRow


class PostgresEmployeeRepository(IEmployeeRepository):
    async def save(self, employee: Employee) -> None:
        async with session_scope(tenant_id=employee.tenant_id) as session:
            row = await session.get(HrEmployeeRow, UUID(str(employee.id)))
            if row is None:
                session.add(
                    HrEmployeeRow(
                        id=UUID(str(employee.id)),
                        tenant_id=employee.tenant_id,
                        email=employee.email,
                        full_name=employee.full_name,
                        job_title=employee.job_title,
                        department=employee.department,
                        employee_number=employee.employee_number,
                        status=employee.status.value,
                        hired_at=employee.hired_at,
                        terminated_at=employee.terminated_at,
                        termination_reason=employee.termination_reason,
                        created_at=employee.created_at,
                        updated_at=employee.updated_at,
                    )
                )
            else:
                row.email = employee.email
                row.full_name = employee.full_name
                row.job_title = employee.job_title
                row.department = employee.department
                row.employee_number = employee.employee_number
                row.status = employee.status.value
                row.hired_at = employee.hired_at
                row.terminated_at = employee.terminated_at
                row.termination_reason = employee.termination_reason
                row.updated_at = employee.updated_at

    async def find_by_id(self, tenant_id: str, employee_id: UniqueId) -> Employee | None:
        async with session_scope(tenant_id=tenant_id) as session:
            row = await session.get(HrEmployeeRow, UUID(str(employee_id)))
            return _employee_from_row(row) if row and row.tenant_id == tenant_id else None

    async def find_by_email(self, tenant_id: str, email: str) -> Employee | None:
        async with session_scope(tenant_id=tenant_id) as session:
            row = await session.scalar(
                select(HrEmployeeRow).where(
                    HrEmployeeRow.tenant_id == tenant_id,
                    HrEmployeeRow.email == email.strip().lower(),
                )
            )
            return _employee_from_row(row) if row else None

    async def list_employees(self, tenant_id: str) -> list[Employee]:
        async with session_scope(tenant_id=tenant_id) as session:
            rows = (
                await session.scalars(
                    select(HrEmployeeRow).where(HrEmployeeRow.tenant_id == tenant_id)
                )
            ).all()
        return [_employee_from_row(r) for r in rows]


def _employee_from_row(row: HrEmployeeRow) -> Employee:
    return Employee(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        email=row.email,
        full_name=row.full_name,
        job_title=row.job_title or "",
        department=row.department or "",
        employee_number=row.employee_number or "",
        status=EmployeeStatus(row.status),
        hired_at=row.hired_at,
        terminated_at=row.terminated_at,
        termination_reason=row.termination_reason or "",
        created_at=row.created_at,
        updated_at=row.updated_at,
    )
