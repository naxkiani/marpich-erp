"""PostgreSQL repositories — Payroll (CAP-ENT-015)."""
from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from sqlalchemy import select

from contexts.payroll.domain.aggregates.payroll_employee import (
    PayrollEmployee,
    PayrollEmployeeStatus,
)
from contexts.payroll.domain.aggregates.payroll_run import (
    PayrollRun,
    PayrollRunStatus,
    PayslipLine,
)
from contexts.payroll.domain.ports.repositories import (
    IPayrollEmployeeRepository,
    IPayrollRunRepository,
)
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.database.engine import session_scope
from shared.infrastructure.database.orm import PayrollEmployeeRow, PayrollRunRow


class PostgresPayrollEmployeeRepository(IPayrollEmployeeRepository):
    async def save(self, employee: PayrollEmployee) -> None:
        async with session_scope(tenant_id=employee.tenant_id) as session:
            row = await session.get(PayrollEmployeeRow, UUID(str(employee.id)))
            if row is None:
                session.add(
                    PayrollEmployeeRow(
                        id=UUID(str(employee.id)),
                        tenant_id=employee.tenant_id,
                        hr_employee_id=UUID(str(employee.hr_employee_id)),
                        email=employee.email,
                        full_name=employee.full_name,
                        job_title=employee.job_title,
                        department=employee.department,
                        employee_number=employee.employee_number,
                        status=employee.status.value,
                        base_salary=Decimal(employee.base_salary),
                        currency=employee.currency,
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
                row.base_salary = Decimal(employee.base_salary)
                row.currency = employee.currency
                row.updated_at = employee.updated_at

    async def find_by_id(self, tenant_id: str, employee_id: UniqueId) -> PayrollEmployee | None:
        async with session_scope(tenant_id=tenant_id) as session:
            row = await session.get(PayrollEmployeeRow, UUID(str(employee_id)))
            return _employee_from_row(row) if row and row.tenant_id == tenant_id else None

    async def find_by_hr_employee_id(
        self, tenant_id: str, hr_employee_id: UniqueId
    ) -> PayrollEmployee | None:
        async with session_scope(tenant_id=tenant_id) as session:
            row = await session.scalar(
                select(PayrollEmployeeRow).where(
                    PayrollEmployeeRow.tenant_id == tenant_id,
                    PayrollEmployeeRow.hr_employee_id == UUID(str(hr_employee_id)),
                )
            )
            return _employee_from_row(row) if row else None

    async def list_active(self, tenant_id: str) -> list[PayrollEmployee]:
        async with session_scope(tenant_id=tenant_id) as session:
            rows = (
                await session.scalars(
                    select(PayrollEmployeeRow).where(
                        PayrollEmployeeRow.tenant_id == tenant_id,
                        PayrollEmployeeRow.status == PayrollEmployeeStatus.ACTIVE.value,
                    )
                )
            ).all()
        return [_employee_from_row(r) for r in rows]


class PostgresPayrollRunRepository(IPayrollRunRepository):
    async def save(self, run: PayrollRun) -> None:
        async with session_scope(tenant_id=run.tenant_id) as session:
            row = await session.get(PayrollRunRow, UUID(str(run.id)))
            payload = [p.to_dict() for p in run.payslips]
            if row is None:
                session.add(
                    PayrollRunRow(
                        id=UUID(str(run.id)),
                        tenant_id=run.tenant_id,
                        period_label=run.period_label,
                        status=run.status.value,
                        currency=run.currency,
                        total_gross=run.total_gross,
                        total_net=run.total_net,
                        payslips=payload,
                        correlation_id=run.correlation_id,
                        created_at=run.created_at,
                        updated_at=run.updated_at,
                        completed_at=run.completed_at,
                    )
                )
            else:
                row.period_label = run.period_label
                row.status = run.status.value
                row.currency = run.currency
                row.total_gross = run.total_gross
                row.total_net = run.total_net
                row.payslips = payload
                row.correlation_id = run.correlation_id
                row.updated_at = run.updated_at
                row.completed_at = run.completed_at

    async def find_by_id(self, tenant_id: str, run_id: UniqueId) -> PayrollRun | None:
        async with session_scope(tenant_id=tenant_id) as session:
            row = await session.get(PayrollRunRow, UUID(str(run_id)))
            return _run_from_row(row) if row and row.tenant_id == tenant_id else None

    async def list_runs(self, tenant_id: str) -> list[PayrollRun]:
        async with session_scope(tenant_id=tenant_id) as session:
            rows = (
                await session.scalars(
                    select(PayrollRunRow).where(PayrollRunRow.tenant_id == tenant_id)
                )
            ).all()
        return [_run_from_row(r) for r in rows]


def _employee_from_row(row: PayrollEmployeeRow) -> PayrollEmployee:
    return PayrollEmployee(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        hr_employee_id=UniqueId.from_string(str(row.hr_employee_id)),
        email=row.email,
        full_name=row.full_name,
        job_title=row.job_title or "",
        department=row.department or "",
        employee_number=row.employee_number or "",
        status=PayrollEmployeeStatus(row.status),
        base_salary=str(row.base_salary),
        currency=row.currency,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def _run_from_row(row: PayrollRunRow) -> PayrollRun:
    slips: list[PayslipLine] = []
    for item in row.payslips or []:
        slips.append(
            PayslipLine(
                payroll_employee_id=UniqueId.from_string(str(item["payroll_employee_id"])),
                hr_employee_id=UniqueId.from_string(str(item["hr_employee_id"])),
                email=str(item.get("email") or ""),
                full_name=str(item.get("full_name") or ""),
                gross=Decimal(str(item.get("gross") or "0")),
                net=Decimal(str(item.get("net") or "0")),
                currency=str(item.get("currency") or row.currency),
            )
        )
    return PayrollRun(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        period_label=row.period_label,
        status=PayrollRunStatus(row.status),
        payslips=slips,
        currency=row.currency,
        total_gross=Decimal(str(row.total_gross)),
        total_net=Decimal(str(row.total_net)),
        correlation_id=row.correlation_id or "",
        created_at=row.created_at,
        updated_at=row.updated_at,
        completed_at=row.completed_at,
    )
