"""Payroll application service — CAP-ENT-015.

HR hire → local employee projection. Complete run → payroll.run.completed.
"""
from __future__ import annotations

from decimal import Decimal, InvalidOperation

from contexts.payroll.domain.aggregates.payroll_employee import PayrollEmployee
from contexts.payroll.domain.aggregates.payroll_run import PayrollRun, PayslipLine
from contexts.payroll.domain.events.integration_events import PayslipGeneratedIntegration
from contexts.payroll.domain.ports.repositories import (
    IPayrollEmployeeRepository,
    IPayrollRunRepository,
)
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class PayrollApplicationService:
    def __init__(
        self,
        employees: IPayrollEmployeeRepository,
        runs: IPayrollRunRepository,
    ) -> None:
        self._employees = employees
        self._runs = runs

    async def project_hired_employee(
        self,
        *,
        tenant_id: str,
        hr_employee_id: str,
        email: str,
        full_name: str,
        correlation_id: str,
        job_title: str = "",
        department: str = "",
        employee_number: str = "",
    ) -> Result[dict]:
        hr_id = UniqueId.from_string(hr_employee_id)
        existing = await self._employees.find_by_hr_employee_id(tenant_id, hr_id)
        if existing:
            return Result.ok(existing.to_dict())
        try:
            employee = PayrollEmployee.project_from_hire(
                tenant_id=tenant_id,
                hr_employee_id=hr_id,
                email=email,
                full_name=full_name,
                job_title=job_title,
                department=department,
                employee_number=employee_number,
            )
        except ValueError as exc:
            return Result.fail(str(exc))
        await self._employees.save(employee)
        return Result.ok(employee.to_dict())

    async def list_employees(
        self, tenant_id: str, *, limit: int = 50, offset: int = 0
    ) -> Result[dict]:
        limit = max(1, min(limit, 100))
        offset = max(0, offset)
        items = await self._employees.list_active(tenant_id)
        page = items[offset : offset + limit]
        return Result.ok(
            {
                "items": [e.to_dict() for e in page],
                "total": len(items),
                "limit": limit,
                "offset": offset,
            }
        )

    async def list_runs(
        self, tenant_id: str, *, limit: int = 50, offset: int = 0
    ) -> Result[dict]:
        limit = max(1, min(limit, 100))
        offset = max(0, offset)
        items = await self._runs.list_runs(tenant_id)
        page = items[offset : offset + limit]
        return Result.ok(
            {
                "items": [r.to_dict() for r in page],
                "total": len(items),
                "limit": limit,
                "offset": offset,
            }
        )

    async def create_and_complete_run(
        self, *, tenant_id: str, period_label: str, correlation_id: str
    ) -> Result[dict]:
        employees = await self._employees.list_active(tenant_id)
        if not employees:
            return Result.fail("payroll.errors.no_employees")
        try:
            run = PayrollRun.open(tenant_id=tenant_id, period_label=period_label)
        except ValueError as exc:
            return Result.fail(str(exc))

        payslips: list[PayslipLine] = []
        for emp in employees:
            try:
                gross = Decimal(emp.base_salary)
            except (InvalidOperation, ValueError):
                gross = Decimal("5000.00")
            # Thin Wave 02 stub: flat 10% deduction — tax engine later
            net = (gross * Decimal("0.9")).quantize(Decimal("0.01"))
            payslips.append(
                PayslipLine(
                    payroll_employee_id=emp.id,
                    hr_employee_id=emp.hr_employee_id,
                    email=emp.email,
                    full_name=emp.full_name,
                    gross=gross,
                    net=net,
                    currency=emp.currency or run.currency,
                )
            )
        try:
            completed = run.complete(correlation_id=correlation_id, payslips=payslips)
        except ValueError as exc:
            return Result.fail(str(exc))
        await self._runs.save(run)
        await publish_integration_event(completed)
        for slip in payslips:
            await publish_integration_event(
                PayslipGeneratedIntegration(
                    tenant_id=TenantId.create(tenant_id),
                    correlation_id=correlation_id,
                    run_id=run.id,
                    payroll_employee_id=slip.payroll_employee_id,
                    hr_employee_id=slip.hr_employee_id,
                    gross=str(slip.gross),
                    net=str(slip.net),
                    currency=slip.currency,
                )
            )
        return Result.ok(run.to_dict())
