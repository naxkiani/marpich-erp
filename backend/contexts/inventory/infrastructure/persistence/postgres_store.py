"""PostgreSQL repositories — Inventory bounded context."""
from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from sqlalchemy import select

from contexts.inventory.domain.aggregates.stock_level import StockLevel
from contexts.inventory.domain.ports.repositories import IStockLevelRepository
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.database.engine import session_scope
from shared.infrastructure.database.orm import InventoryStockLevelRow


class PostgresStockLevelRepository(IStockLevelRepository):
    async def save(self, stock: StockLevel) -> None:
        async with session_scope() as session:
            row = await session.get(InventoryStockLevelRow, UUID(str(stock.id)))
            if row is None:
                session.add(
                    InventoryStockLevelRow(
                        id=UUID(str(stock.id)),
                        tenant_id=stock.tenant_id,
                        sku=stock.sku,
                        quantity_on_hand=stock.quantity_on_hand,
                        updated_at=stock.updated_at,
                    )
                )
            else:
                row.sku = stock.sku
                row.quantity_on_hand = stock.quantity_on_hand
                row.updated_at = stock.updated_at

    async def find_by_sku(self, tenant_id: str, sku: str) -> StockLevel | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(InventoryStockLevelRow).where(
                    InventoryStockLevelRow.tenant_id == tenant_id,
                    InventoryStockLevelRow.sku == sku,
                )
            )
            return _stock_from_row(row) if row else None

    async def list_by_tenant(
        self, tenant_id: str, *, limit: int = 50, offset: int = 0
    ) -> list[StockLevel]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(InventoryStockLevelRow)
                    .where(InventoryStockLevelRow.tenant_id == tenant_id)
                    .order_by(InventoryStockLevelRow.sku)
                    .offset(offset)
                    .limit(limit)
                )
            ).all()
        return [_stock_from_row(r) for r in rows]


def _stock_from_row(row: InventoryStockLevelRow) -> StockLevel:
    return StockLevel(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        sku=row.sku,
        quantity_on_hand=Decimal(str(row.quantity_on_hand)),
        updated_at=row.updated_at,
    )
