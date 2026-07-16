"""Inventory DI container + POS event subscription."""
from __future__ import annotations

from contexts.inventory.application.service import InventoryApplicationService
from contexts.inventory.infrastructure.acl.pos_events import handle_pos_sale_completed
from contexts.inventory.infrastructure.persistence.memory_store import InMemoryStockLevelRepository
from shared.infrastructure.messaging.event_bus import InProcessEventBus

_service: InventoryApplicationService | None = None
_registered = False


def get_inventory_service() -> InventoryApplicationService:
    global _service, _registered
    if _service is None:
        _service = InventoryApplicationService(stock=InMemoryStockLevelRepository())
    if not _registered:
        InProcessEventBus.subscribe("pos.sale.completed", handle_pos_sale_completed)
        _registered = True
    return _service


def reset_inventory_service() -> None:
    global _service, _registered
    _service = None
    _registered = False
