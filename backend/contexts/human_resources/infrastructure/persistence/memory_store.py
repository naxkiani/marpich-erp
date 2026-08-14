"""Human Resources in-memory repositories."""
from __future__ import annotations

from contexts.human_resources.domain.aggregates.employee import Employee
from contexts.human_resources.domain.ports.repositories import IEmployeeRepository
from shared.domain.value_objects.unique_id import UniqueId


class HumanResourcesMemoryStore:
    employees: dict[str, Employee] = {}

    @classmethod
    def reset(cls) -> None:
        cls.employees.clear()


class InMemoryEmployeeRepository(IEmployeeRepository):
    async def save(self, employee: Employee) -> None:
        HumanResourcesMemoryStore.employees[str(employee.id)] = employee

    async def find_by_id(self, tenant_id: str, employee_id: UniqueId) -> Employee | None:
        emp = HumanResourcesMemoryStore.employees.get(str(employee_id))
        return emp if emp and emp.tenant_id == tenant_id else None

    async def find_by_email(self, tenant_id: str, email: str) -> Employee | None:
        target = email.strip().lower()
        for emp in HumanResourcesMemoryStore.employees.values():
            if emp.tenant_id == tenant_id and emp.email == target:
                return emp
        return None

    async def list_employees(self, tenant_id: str) -> list[Employee]:
        items = [
            e for e in HumanResourcesMemoryStore.employees.values() if e.tenant_id == tenant_id
        ]
        return sorted(items, key=lambda e: e.created_at, reverse=True)
