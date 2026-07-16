"""Inventory in-memory repositories."""
from __future__ import annotations

from contexts.inventory.domain.aggregates.stock_level import StockLevel
from contexts.inventory.domain.ports.repositories import IStockLevelRepository


class InventoryMemoryStore:
    stock: dict[str, StockLevel] = {}

    @classmethod
    def reset(cls) -> None:
        cls.stock.clear()


class InMemoryStockLevelRepository(IStockLevelRepository):
    async def save(self, stock: StockLevel) -> None:
        InventoryMemoryStore.stock[str(stock.id)] = stock

    async def find_by_sku(self, tenant_id: str, sku: str) -> StockLevel | None:
        for row in InventoryMemoryStore.stock.values():
            if row.tenant_id == tenant_id and row.sku == sku:
                return row
        return None

    async def list_by_tenant(
        self, tenant_id: str, *, limit: int = 50, offset: int = 0
    ) -> list[StockLevel]:
        rows = [s for s in InventoryMemoryStore.stock.values() if s.tenant_id == tenant_id]
        rows.sort(key=lambda s: s.sku)
        return rows[offset : offset + limit]
