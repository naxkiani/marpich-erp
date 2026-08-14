"""Sales DI container + CRM opportunity subscription."""
from __future__ import annotations

from contexts.sales.application.service import SalesApplicationService
from contexts.sales.infrastructure.acl.event_routes import SalesCrmEventAdapter
from contexts.sales.infrastructure.persistence.memory_store import (
    InMemoryQuotationRepository,
    InMemorySalesOrderRepository,
)
from contexts.sales.infrastructure.persistence.postgres_store import (
    PostgresQuotationRepository,
    PostgresSalesOrderRepository,
)
from shared.infrastructure.messaging.event_bus import InProcessEventBus
from shared.infrastructure.settings import use_postgres

_service: SalesApplicationService | None = None
_registered = False


def get_sales_service() -> SalesApplicationService:
    global _service, _registered
    if _service is None:
        adapter = SalesCrmEventAdapter()
        if use_postgres():
            _service = SalesApplicationService(
                quotations=PostgresQuotationRepository(),
                orders=PostgresSalesOrderRepository(),
                event_adapter=adapter,
            )
        else:
            _service = SalesApplicationService(
                quotations=InMemoryQuotationRepository(),
                orders=InMemorySalesOrderRepository(),
                event_adapter=adapter,
            )
    if not _registered:
        InProcessEventBus.subscribe("crm.opportunity.won", _service.handle_integration_event)
        _registered = True
    return _service


def reset_sales_service() -> None:
    global _service, _registered
    _service = None
    _registered = False
