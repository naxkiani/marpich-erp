"""Inventory application service — stock seed + POS decrement."""
from __future__ import annotations

from decimal import Decimal

from contexts.inventory.domain.aggregates.stock_level import StockLevel
from contexts.inventory.domain.events.integration_events import StockAdjustedIntegration
from contexts.inventory.domain.ports.repositories import IStockLevelRepository
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class InventoryApplicationService:
    def __init__(self, stock: IStockLevelRepository) -> None:
        self._stock = stock
        self._processed_sales: set[str] = set()

    async def upsert_stock(
        self,
        *,
        tenant_id: str,
        sku: str,
        quantity: Decimal,
        correlation_id: str,
    ) -> Result[dict]:
        existing = await self._stock.find_by_sku(tenant_id, sku)
        if existing:
            try:
                existing.set_quantity(quantity)
            except ValueError as exc:
                return Result.fail(str(exc))
            await self._stock.save(existing)
            return Result.ok(existing.to_dict())
        try:
            row = StockLevel.seed(tenant_id=tenant_id, sku=sku, quantity=quantity)
        except ValueError as exc:
            return Result.fail(str(exc))
        await self._stock.save(row)
        return Result.ok(row.to_dict())

    async def list_stock(
        self, tenant_id: str, *, limit: int = 50, offset: int = 0
    ) -> Result[list[dict]]:
        rows = await self._stock.list_by_tenant(tenant_id, limit=limit, offset=offset)
        return Result.ok([r.to_dict() for r in rows])

    async def get_stock(self, tenant_id: str, sku: str) -> Result[dict]:
        row = await self._stock.find_by_sku(tenant_id, sku)
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
            sku = str(item.get("sku") or "")
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
