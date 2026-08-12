"""Inventory application service — CAP-ENT-042 Inventory Lifecycle.

POS decrement + Sales order reservation. Audit via integration events.
"""
from __future__ import annotations

from decimal import Decimal

from contexts.inventory.domain.aggregates.stock_level import StockLevel
from contexts.inventory.domain.events.integration_events import (
    ReorderTriggeredIntegration,
    StockAdjustedIntegration,
    StockReservedIntegration,
)
from contexts.inventory.domain.ports.repositories import IStockLevelRepository
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event

REORDER_THRESHOLD = Decimal("20")


class InventoryApplicationService:
    def __init__(self, stock: IStockLevelRepository) -> None:
        self._stock = stock
        self._processed_sales: set[str] = set()
        self._processed_orders: set[str] = set()

    async def upsert_stock(
        self,
        *,
        tenant_id: str,
        sku: str,
        quantity: Decimal,
        correlation_id: str,
    ) -> Result[dict]:
        sku_key = sku.strip().upper()
        existing = await self._stock.find_by_sku(tenant_id, sku_key)
        if existing:
            try:
                existing.set_quantity(quantity)
            except ValueError as exc:
                return Result.fail(str(exc))
            await self._stock.save(existing)
            return Result.ok(existing.to_dict())
        try:
            row = StockLevel.seed(tenant_id=tenant_id, sku=sku_key, quantity=quantity)
        except ValueError as exc:
            return Result.fail(str(exc))
        await self._stock.save(row)
        return Result.ok(row.to_dict())

    async def list_stock(
        self, tenant_id: str, *, limit: int = 50, offset: int = 0
    ) -> Result[dict]:
        limit = max(1, min(limit, 100))
        offset = max(0, offset)
        # Fetch one extra page window via repo limit; total needs full count for desk.
        all_rows = await self._stock.list_by_tenant(tenant_id, limit=10_000, offset=0)
        page = all_rows[offset : offset + limit]
        return Result.ok(
            {
                "items": [r.to_dict() for r in page],
                "total": len(all_rows),
                "limit": limit,
                "offset": offset,
            }
        )

    async def get_stock(self, tenant_id: str, sku: str) -> Result[dict]:
        row = await self._stock.find_by_sku(tenant_id, sku.strip().upper())
        if not row:
            return Result.fail("inventory.errors.sku_not_found")
        return Result.ok(row.to_dict())

    async def apply_pos_sale_decrement(
        self,
        *,
        tenant_id: str,
        sale_id: str,
        items: list[dict],
        correlation_id: str,
    ) -> Result[list[dict]]:
        """Idempotent stock decrement for a completed POS sale."""
        dedupe = f"{tenant_id}:{sale_id}"
        if dedupe in self._processed_sales:
            return Result.ok([])

        adjusted: list[dict] = []
        for item in items:
            sku = str(item.get("sku") or "").strip().upper()
            qty = Decimal(str(item.get("quantity") or 0))
            if not sku or qty <= 0:
                continue
            row = await self._stock.find_by_sku(tenant_id, sku)
            if not row:
                return Result.fail(f"inventory.errors.sku_not_found:{sku}")
            try:
                row.decrement(qty)
            except ValueError as exc:
                return Result.fail(str(exc))
            await self._stock.save(row)
            event = StockAdjustedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                stock_id=row.id,
                sku=sku,
                quantity_delta=str(-qty),
                quantity_on_hand=str(row.quantity_on_hand),
                reason="pos.sale.completed",
                source_document_id=sale_id,
            )
            await publish_integration_event(event)
            adjusted.append(row.to_dict())

        self._processed_sales.add(dedupe)
        return Result.ok(adjusted)

    async def apply_sales_order_reservation(
        self,
        *,
        tenant_id: str,
        order_id: str,
        lines: list[dict],
        correlation_id: str,
    ) -> Result[list[dict]]:
        """Idempotent stock reservation for a placed sales order."""
        dedupe = f"{tenant_id}:{order_id}"
        if dedupe in self._processed_orders:
            return Result.ok([])

        reserved: list[dict] = []
        for line in lines:
            sku = str(line.get("sku") or line.get("item_id") or "").strip().upper()
            qty = Decimal(str(line.get("quantity") or 0))
            if not sku or qty <= 0:
                continue
            row = await self._stock.find_by_sku(tenant_id, sku)
            if not row:
                return Result.fail(f"inventory.errors.sku_not_found:{sku}")
            try:
                row.reserve(qty)
            except ValueError as exc:
                return Result.fail(str(exc))
            await self._stock.save(row)
            event = StockReservedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                stock_id=row.id,
                sku=sku,
                quantity_reserved_delta=str(qty),
                quantity_reserved=str(row.quantity_reserved),
                quantity_available=str(row.quantity_available),
                order_id=order_id,
            )
            await publish_integration_event(event)
            reserved.append(row.to_dict())
            if row.quantity_available < REORDER_THRESHOLD:
                replenish = REORDER_THRESHOLD * 2 - row.quantity_available
                if replenish < REORDER_THRESHOLD:
                    replenish = REORDER_THRESHOLD
                await publish_integration_event(
                    ReorderTriggeredIntegration(
                        tenant_id=TenantId.create(tenant_id),
                        correlation_id=correlation_id,
                        stock_id=row.id,
                        sku=sku,
                        quantity_available=str(row.quantity_available),
                        quantity_on_hand=str(row.quantity_on_hand),
                        quantity_reserved=str(row.quantity_reserved),
                        reorder_threshold=str(REORDER_THRESHOLD),
                        suggested_reorder_quantity=str(replenish),
                    )
                )

        self._processed_orders.add(dedupe)
        return Result.ok(reserved)
