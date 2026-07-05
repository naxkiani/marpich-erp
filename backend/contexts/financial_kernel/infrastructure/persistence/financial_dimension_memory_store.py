"""In-memory financial dimension repositories."""
from __future__ import annotations

from contexts.financial_kernel.domain.aggregates.financial_dimension import (
    DimensionAuditLog,
    DimensionValue,
)
from contexts.financial_kernel.domain.ports.financial_dimension_repositories import (
    IDimensionAuditRepository,
    IDimensionValueRepository,
)


class InMemoryDimensionValueRepository(IDimensionValueRepository):
    _values: dict[str, DimensionValue] = {}

    @classmethod
    def reset(cls) -> None:
        cls._values = {}

    async def save(self, value: DimensionValue) -> None:
        self._values[str(value.id)] = value

    async def find_by_id(self, value_id: str) -> DimensionValue | None:
        return self._values.get(value_id)

    async def find_by_code(
        self, tenant_id: str, dimension_type: str, code: str
    ) -> DimensionValue | None:
        for value in self._values.values():
            if (
                value.tenant_id == tenant_id
                and value.dimension_type == dimension_type
                and value.code == code.upper()
            ):
                return value
        return None

    async def list_by_tenant(self, tenant_id: str) -> list[DimensionValue]:
        items = [v for v in self._values.values() if v.tenant_id == tenant_id]
        return sorted(items, key=lambda v: (v.dimension_type, v.code))

    async def list_by_type(self, tenant_id: str, dimension_type: str) -> list[DimensionValue]:
        items = [
            v
            for v in self._values.values()
            if v.tenant_id == tenant_id and v.dimension_type == dimension_type
        ]
        return sorted(items, key=lambda v: v.code)


class InMemoryDimensionAuditRepository(IDimensionAuditRepository):
    _entries: list[DimensionAuditLog] = []

    @classmethod
    def reset(cls) -> None:
        cls._entries = []

    async def save(self, entry: DimensionAuditLog) -> None:
        self._entries.append(entry)

    async def list_by_dimension_value(self, dimension_value_id: str) -> list[DimensionAuditLog]:
        return [e for e in self._entries if e.dimension_value_id == dimension_value_id]

    async def list_by_tenant(self, tenant_id: str, *, limit: int = 100) -> list[DimensionAuditLog]:
        items = [e for e in self._entries if e.tenant_id == tenant_id]
        return items[-limit:]
