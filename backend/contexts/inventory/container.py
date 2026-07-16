"""Inventory DI container + POS event subscription."""
from __future__ import annotations

from contexts.inventory.application.service import InventoryApplicationService
from contexts.inventory.infrastructure.acl.pharmacy_events import make_pharmacy_dispense_handler
from contexts.inventory.infrastructure.acl.pos_events import handle_pos_sale_completed
from contexts.inventory.infrastructure.persistence.memory_store import InMemoryStockLevelRepository
from contexts.inventory.infrastructure.persistence.postgres_store import PostgresStockLevelRepository
from shared.infrastructure.messaging.event_bus import InProcessEventBus
from shared.infrastructure.settings import use_postgres

_service: InventoryApplicationService | None = None
_registered = False


def get_inventory_service() -> InventoryApplicationService:
    global _service, _registered
    if _service is None:
        if use_postgres():
            _service = InventoryApplicationService(stock=PostgresStockLevelRepository())
        else:
            _service = InventoryApplicationService(stock=InMemoryStockLevelRepository())
    if not _registered:
        InProcessEventBus.subscribe("pos.sale.completed", handle_pos_sale_completed)
        InProcessEventBus.subscribe(
            "pharmacy.dispense.completed",
            make_pharmacy_dispense_handler(get_inventory_service),
        )
        _registered = True
    return _service


def reset_inventory_service() -> None:
    global _service, _registered
    _service = None
    _registered = False
