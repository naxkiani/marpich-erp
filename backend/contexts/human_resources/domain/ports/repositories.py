"""Human Resources repository ports."""
from __future__ import annotations

from abc import ABC, abstractmethod

from contexts.human_resources.domain.aggregates.employee import Employee
from shared.domain.value_objects.unique_id import UniqueId


class IEmployeeRepository(ABC):
    @abstractmethod
    async def save(self, employee: Employee) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, employee_id: UniqueId) -> Employee | None: ...

    @abstractmethod
    async def find_by_email(self, tenant_id: str, email: str) -> Employee | None: ...

    @abstractmethod
    async def list_employees(self, tenant_id: str) -> list[Employee]: ...
