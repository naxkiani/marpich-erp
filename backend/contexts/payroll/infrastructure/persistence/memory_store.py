"""Payroll in-memory repositories."""
from __future__ import annotations

from contexts.payroll.domain.aggregates.payroll_employee import (
    PayrollEmployee,
    PayrollEmployeeStatus,
)
from contexts.payroll.domain.aggregates.payroll_run import PayrollRun
from contexts.payroll.domain.ports.repositories import (
    IPayrollEmployeeRepository,
    IPayrollRunRepository,
)
from shared.domain.value_objects.unique_id import UniqueId


class PayrollMemoryStore:
    employees: dict[str, PayrollEmployee] = {}
    runs: dict[str, PayrollRun] = {}

    @classmethod
    def reset(cls) -> None:
        cls.employees.clear()
        cls.runs.clear()


class InMemoryPayrollEmployeeRepository(IPayrollEmployeeRepository):
    async def save(self, employee: PayrollEmployee) -> None:
        PayrollMemoryStore.employees[str(employee.id)] = employee

    async def find_by_id(self, tenant_id: str, employee_id: UniqueId) -> PayrollEmployee | None:
        emp = PayrollMemoryStore.employees.get(str(employee_id))
        return emp if emp and emp.tenant_id == tenant_id else None

    async def find_by_hr_employee_id(
        self, tenant_id: str, hr_employee_id: UniqueId
    ) -> PayrollEmployee | None:
        for emp in PayrollMemoryStore.employees.values():
            if emp.tenant_id == tenant_id and str(emp.hr_employee_id) == str(hr_employee_id):
                return emp
        return None

    async def list_active(self, tenant_id: str) -> list[PayrollEmployee]:
        items = [
            e
            for e in PayrollMemoryStore.employees.values()
            if e.tenant_id == tenant_id and e.status == PayrollEmployeeStatus.ACTIVE
        ]
        return sorted(items, key=lambda e: e.created_at, reverse=True)


class InMemoryPayrollRunRepository(IPayrollRunRepository):
    async def save(self, run: PayrollRun) -> None:
        PayrollMemoryStore.runs[str(run.id)] = run

    async def find_by_id(self, tenant_id: str, run_id: UniqueId) -> PayrollRun | None:
        run = PayrollMemoryStore.runs.get(str(run_id))
        return run if run and run.tenant_id == tenant_id else None

    async def list_runs(self, tenant_id: str) -> list[PayrollRun]:
        items = [r for r in PayrollMemoryStore.runs.values() if r.tenant_id == tenant_id]
        return sorted(items, key=lambda r: r.created_at, reverse=True)
