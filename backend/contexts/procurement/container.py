"""Procurement DI container + inventory reorder subscription."""
from __future__ import annotations

from contexts.procurement.application.service import ProcurementApplicationService
from contexts.procurement.infrastructure.acl.inventory_events import InventoryReorderEventAdapter
from contexts.procurement.infrastructure.persistence.memory_store import InMemoryRequisitionRepository
from contexts.procurement.infrastructure.persistence.postgres_store import (
    PostgresRequisitionRepository,
)
from shared.infrastructure.messaging.event_bus import InProcessEventBus
from shared.infrastructure.settings import use_postgres

_service: ProcurementApplicationService | None = None
_registered = False


def get_procurement_service() -> ProcurementApplicationService:
    global _service, _registered
    if _service is None:
        adapter = InventoryReorderEventAdapter()
        if use_postgres():
            _service = ProcurementApplicationService(
                requisitions=PostgresRequisitionRepository(),
                reorder_adapter=adapter,
            )
        else:
            _service = ProcurementApplicationService(
                requisitions=InMemoryRequisitionRepository(),
                reorder_adapter=adapter,
            )
    if not _registered:
        InProcessEventBus.subscribe(
            "inventory.reorder.triggered",
            _service.handle_integration_event,
        )
        _registered = True
    return _service


def reset_procurement_service() -> None:
    global _service, _registered
    _service = None
    _registered = False
