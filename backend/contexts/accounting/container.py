"""Accounting DI + hospital + sales event subscriptions."""
from __future__ import annotations

from contexts.accounting.application.service import AccountingApplicationService
from contexts.accounting.infrastructure.acl.hospital_events import HospitalEventAdapter
from contexts.accounting.infrastructure.acl.sales_events import SalesOrderEventAdapter
from contexts.accounting.infrastructure.persistence.memory_store import (
    InMemoryBillingRepository,
    InMemoryInvoiceRepository,
)
from contexts.accounting.infrastructure.persistence.postgres_store import (
    PostgresBillingRepository,
    PostgresInvoiceRepository,
)
from shared.infrastructure.messaging.event_bus import InProcessEventBus
from shared.infrastructure.settings import use_postgres

_service: AccountingApplicationService | None = None
_registered = False


def get_accounting_service() -> AccountingApplicationService:
    global _service, _registered
    if _service is None:
        if use_postgres():
            billings = PostgresBillingRepository()
            invoices = PostgresInvoiceRepository()
        else:
            billings = InMemoryBillingRepository()
            invoices = InMemoryInvoiceRepository()
        _service = AccountingApplicationService(
            billings=billings,
            hospital_events=HospitalEventAdapter(),
            invoices=invoices,
            sales_events=SalesOrderEventAdapter(),
        )
    if not _registered:
        InProcessEventBus.subscribe(
            "hospital.encounter.completed",
            _service.handle_hospital_encounter_completed,
        )
        InProcessEventBus.subscribe(
            "sales.order.placed",
            _service.handle_sales_order_placed,
        )
        _registered = True
    return _service


def reset_accounting_service() -> None:
    global _service, _registered
    _service = None
    _registered = False
