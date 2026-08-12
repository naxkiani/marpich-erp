"""Procurement application service — CAP-ENT-040 Procurement Lifecycle."""
from __future__ import annotations

from decimal import Decimal, InvalidOperation

from contexts.procurement.domain.aggregates.purchase_requisition import PurchaseRequisition
from contexts.procurement.domain.ports.repositories import IRequisitionRepository
from contexts.procurement.infrastructure.acl.inventory_events import (
    DraftRequisitionFromReorderCommand,
    InventoryReorderEventAdapter,
)
from shared.application.result import Result
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class ProcurementApplicationService:
    def __init__(
        self,
        requisitions: IRequisitionRepository,
        reorder_adapter: InventoryReorderEventAdapter | None = None,
    ) -> None:
        self._requisitions = requisitions
        self._reorder_adapter = reorder_adapter or InventoryReorderEventAdapter()

    async def handle_integration_event(self, envelope: dict) -> None:
        command = await self._reorder_adapter.parse_integration_event(envelope)
        if command:
            await self.draft_requisition_from_reorder(command)

    async def draft_requisition_from_reorder(
        self, command: DraftRequisitionFromReorderCommand
    ) -> Result[dict]:
        sku = command.sku.strip().upper()
        existing = await self._requisitions.find_open_draft_by_sku(command.tenant_id, sku)
        if existing:
            return Result.ok(existing.to_dict())
        try:
            quantity = Decimal(command.quantity)
            quantity_available = Decimal(command.quantity_available)
            reorder_threshold = Decimal(command.reorder_threshold)
        except (InvalidOperation, ValueError):
            return Result.fail("procurement.errors.invalid_quantity")
        stock_id = UniqueId.from_string(command.stock_id) if command.stock_id else None
        try:
            requisition = PurchaseRequisition.draft_from_reorder(
                tenant_id=command.tenant_id,
                sku=sku,
                quantity=quantity,
                quantity_available=quantity_available,
                reorder_threshold=reorder_threshold,
                stock_id=stock_id,
                correlation_id=command.correlation_id,
            )
        except ValueError as exc:
            return Result.fail(str(exc))
        await self._requisitions.save(requisition)
        await publish_integration_event(requisition.created_event())
        return Result.ok(requisition.to_dict())

    async def list_requisitions(
        self, tenant_id: str, *, limit: int = 50, offset: int = 0
    ) -> Result[dict]:
        limit = max(1, min(limit, 100))
        offset = max(0, offset)
        items = await self._requisitions.list_requisitions(tenant_id)
        page = items[offset : offset + limit]
        return Result.ok(
            {
                "items": [r.to_dict() for r in page],
                "total": len(items),
                "limit": limit,
                "offset": offset,
            }
        )

    async def submit_requisition(
        self, *, tenant_id: str, requisition_id: str, correlation_id: str
    ) -> Result[dict]:
        requisition = await self._requisitions.find_by_id(
            tenant_id, UniqueId.from_string(requisition_id)
        )
        if not requisition:
            return Result.fail("procurement.errors.requisition_not_found")
        try:
            event = requisition.submit(correlation_id=correlation_id)
        except ValueError as exc:
            return Result.fail(str(exc))
        await self._requisitions.save(requisition)
        await publish_integration_event(event)
        return Result.ok(requisition.to_dict())

    async def approve_requisition(
        self, *, tenant_id: str, requisition_id: str, correlation_id: str
    ) -> Result[dict]:
        requisition = await self._requisitions.find_by_id(
            tenant_id, UniqueId.from_string(requisition_id)
        )
        if not requisition:
            return Result.fail("procurement.errors.requisition_not_found")
        try:
            event = requisition.approve(correlation_id=correlation_id)
        except ValueError as exc:
            return Result.fail(str(exc))
        await self._requisitions.save(requisition)
        await publish_integration_event(event)
        return Result.ok(requisition.to_dict())
