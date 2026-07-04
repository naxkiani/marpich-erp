"""In-memory Enterprise Cost Center persistence."""
from __future__ import annotations

from contexts.financial_kernel.domain.aggregates.cost_center import (
    CenterAllocation,
    EnterpriseCostCenter,
    EnterpriseProfitCenter,
)
from contexts.financial_kernel.domain.ports.cost_center_repositories import (
    ICenterAllocationRepository,
    IEnterpriseCostCenterRepository,
    IEnterpriseProfitCenterRepository,
)


class InMemoryEnterpriseCostCenterRepository(IEnterpriseCostCenterRepository):
    _centers: dict[str, EnterpriseCostCenter] = {}

    @classmethod
    def reset(cls) -> None:
        cls._centers = {}

    async def save(self, center: EnterpriseCostCenter) -> None:
        self._centers[str(center.id)] = center
        self._centers[f"code:{center.tenant_id}:{center.code}"] = center

    async def find_by_id(self, center_id: str) -> EnterpriseCostCenter | None:
        c = self._centers.get(center_id)
        return c if isinstance(c, EnterpriseCostCenter) else None

    async def find_by_code(self, tenant_id: str, code: str) -> EnterpriseCostCenter | None:
        c = self._centers.get(f"code:{tenant_id}:{code.upper()}")
        return c if isinstance(c, EnterpriseCostCenter) else None

    async def list_by_tenant(self, tenant_id: str) -> list[EnterpriseCostCenter]:
        seen: set[str] = set()
        result = []
        for c in self._centers.values():
            if isinstance(c, EnterpriseCostCenter) and c.tenant_id == tenant_id and str(c.id) not in seen:
                seen.add(str(c.id))
                result.append(c)
        return result

    async def list_by_type(self, tenant_id: str, center_type: str) -> list[EnterpriseCostCenter]:
        return [c for c in await self.list_by_tenant(tenant_id) if c.center_type == center_type]


class InMemoryEnterpriseProfitCenterRepository(IEnterpriseProfitCenterRepository):
    _centers: dict[str, EnterpriseProfitCenter] = {}

    @classmethod
    def reset(cls) -> None:
        cls._centers = {}

    async def save(self, center: EnterpriseProfitCenter) -> None:
        self._centers[str(center.id)] = center
        self._centers[f"code:{center.tenant_id}:{center.code}"] = center

    async def find_by_id(self, center_id: str) -> EnterpriseProfitCenter | None:
        c = self._centers.get(center_id)
        return c if isinstance(c, EnterpriseProfitCenter) else None

    async def find_by_code(self, tenant_id: str, code: str) -> EnterpriseProfitCenter | None:
        c = self._centers.get(f"code:{tenant_id}:{code.upper()}")
        return c if isinstance(c, EnterpriseProfitCenter) else None

    async def list_by_tenant(self, tenant_id: str) -> list[EnterpriseProfitCenter]:
        seen: set[str] = set()
        result = []
        for c in self._centers.values():
            if isinstance(c, EnterpriseProfitCenter) and c.tenant_id == tenant_id and str(c.id) not in seen:
                seen.add(str(c.id))
                result.append(c)
        return result


class InMemoryCenterAllocationRepository(ICenterAllocationRepository):
    _allocations: dict[str, CenterAllocation] = {}

    @classmethod
    def reset(cls) -> None:
        cls._allocations = {}

    async def save(self, allocation: CenterAllocation) -> None:
        self._allocations[str(allocation.id)] = allocation
        self._allocations[f"idemp:{allocation.tenant_id}:{allocation.idempotency_key}"] = allocation

    async def find_by_idempotency(self, tenant_id: str, key: str) -> CenterAllocation | None:
        a = self._allocations.get(f"idemp:{tenant_id}:{key}")
        return a if isinstance(a, CenterAllocation) else None

    async def list_by_tenant(self, tenant_id: str) -> list[CenterAllocation]:
        seen: set[str] = set()
        result = []
        for a in self._allocations.values():
            if isinstance(a, CenterAllocation) and a.tenant_id == tenant_id and str(a.id) not in seen:
                seen.add(str(a.id))
                result.append(a)
        return result

    async def list_by_cost_center(self, tenant_id: str, cost_center_code: str) -> list[CenterAllocation]:
        code = cost_center_code.upper()
        return [a for a in await self.list_by_tenant(tenant_id) if a.cost_center_code == code]

    async def list_by_type(self, tenant_id: str, allocation_type: str) -> list[CenterAllocation]:
        return [a for a in await self.list_by_tenant(tenant_id) if a.allocation_type == allocation_type]
