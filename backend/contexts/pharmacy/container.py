"""Pharmacy DI container — memory default; Postgres when configured."""
from __future__ import annotations

from contexts.pharmacy.application.service import PharmacyApplicationService
from contexts.pharmacy.infrastructure.acl.clinic_events import (
    handle_clinic_encounter_completed,
)
from contexts.pharmacy.infrastructure.acl.hospital_inventory_events import (
    handle_hospital_encounter_completed,
    handle_inventory_stock_adjusted,
)
from contexts.pharmacy.infrastructure.persistence.memory_store import (
    InMemoryDispenseRepository,
    InMemoryPrescriptionRepository,
)
from contexts.pharmacy.infrastructure.persistence.postgres_store import (
    PostgresDispenseRepository,
    PostgresPrescriptionRepository,
)
from shared.infrastructure.messaging.event_bus import InProcessEventBus
from shared.infrastructure.settings import use_postgres

_service: PharmacyApplicationService | None = None
_registered = False


def get_pharmacy_service() -> PharmacyApplicationService:
    global _service, _registered
    if _service is None:
        if use_postgres():
            _service = PharmacyApplicationService(
                prescriptions=PostgresPrescriptionRepository(),
                dispenses=PostgresDispenseRepository(),
            )
        else:
            _service = PharmacyApplicationService(
                prescriptions=InMemoryPrescriptionRepository(),
                dispenses=InMemoryDispenseRepository(),
            )
    if not _registered:
        InProcessEventBus.subscribe(
            "hospital.encounter.completed",
            handle_hospital_encounter_completed,
        )
        InProcessEventBus.subscribe(
            "clinic.encounter.completed",
            handle_clinic_encounter_completed,
        )
        InProcessEventBus.subscribe(
            "inventory.stock.adjusted",
            handle_inventory_stock_adjusted,
        )
        _registered = True
    return _service


def reset_pharmacy_service() -> None:
    global _service, _registered
    _service = None
    _registered = False
