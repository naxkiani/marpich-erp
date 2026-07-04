"""Accounting DI + event subscription."""
from __future__ import annotations

from contexts.accounting.application.service import AccountingApplicationService
from contexts.accounting.infrastructure.acl.hospital_events import HospitalEventAdapter
from contexts.accounting.infrastructure.persistence.memory_store import InMemoryBillingRepository
from contexts.accounting.infrastructure.persistence.postgres_store import PostgresBillingRepository
from shared.infrastructure.messaging.event_bus import InProcessEventBus
from shared.infrastructure.settings import use_postgres

_service: AccountingApplicationService | None = None
_registered = False


def get_accounting_service() -> AccountingApplicationService:
    global _service, _registered
    if _service is None:
        billings = PostgresBillingRepository() if use_postgres() else InMemoryBillingRepository()
        _service = AccountingApplicationService(
            billings=billings,
            hospital_events=HospitalEventAdapter(),
        )
    if not _registered:
        InProcessEventBus.subscribe(
            "hospital.encounter.completed",
            _service.handle_hospital_encounter_completed,
        )
        _registered = True
    return _service


def reset_accounting_service() -> None:
    global _service, _registered
    _service = None
    _registered = False
