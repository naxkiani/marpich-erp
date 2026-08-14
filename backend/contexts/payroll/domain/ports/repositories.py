"""Payroll repository ports."""
from __future__ import annotations

from abc import ABC, abstractmethod

from contexts.payroll.domain.aggregates.payroll_employee import PayrollEmployee
from contexts.payroll.domain.aggregates.payroll_run import PayrollRun
from shared.domain.value_objects.unique_id import UniqueId


class IPayrollEmployeeRepository(ABC):
    @abstractmethod
    async def save(self, employee: PayrollEmployee) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, employee_id: UniqueId) -> PayrollEmployee | None: ...

    @abstractmethod
    async def find_by_hr_employee_id(
        self, tenant_id: str, hr_employee_id: UniqueId
    ) -> PayrollEmployee | None: ...

    @abstractmethod
    async def list_active(self, tenant_id: str) -> list[PayrollEmployee]: ...


class IPayrollRunRepository(ABC):
    @abstractmethod
    async def save(self, run: PayrollRun) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, run_id: UniqueId) -> PayrollRun | None: ...

    @abstractmethod
    async def list_runs(self, tenant_id: str) -> list[PayrollRun]: ...
