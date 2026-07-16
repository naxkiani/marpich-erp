"""Inventory repository ports."""
from __future__ import annotations

from typing import Protocol

from contexts.inventory.domain.aggregates.stock_level import StockLevel


class IStockLevelRepository(Protocol):
    async def save(self, stock: StockLevel) -> None: ...

    async def find_by_sku(self, tenant_id: str, sku: str) -> StockLevel | None: ...

    async def list_by_tenant(
        self, tenant_id: str, *, limit: int = 50, offset: int = 0
    ) -> list[StockLevel]: ...
