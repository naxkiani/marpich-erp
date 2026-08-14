"""Laboratory DI container — memory default; Postgres when configured."""
from __future__ import annotations

from contexts.laboratory.application.service import LaboratoryApplicationService
from contexts.laboratory.infrastructure.acl.clinic_events import (
    handle_clinic_encounter_completed,
)
from contexts.laboratory.infrastructure.acl.hospital_events import (
    handle_hospital_encounter_completed,
    handle_hospital_encounter_started,
)
from contexts.laboratory.infrastructure.persistence.memory_store import (
    InMemorySampleRepository,
    InMemoryTestOrderRepository,
)
from contexts.laboratory.infrastructure.persistence.postgres_store import (
    PostgresSampleRepository,
    PostgresTestOrderRepository,
)
from shared.infrastructure.messaging.event_bus import InProcessEventBus
from shared.infrastructure.settings import use_postgres

_service: LaboratoryApplicationService | None = None
_registered = False


def get_laboratory_service() -> LaboratoryApplicationService:
    global _service, _registered
    if _service is None:
        if use_postgres():
            _service = LaboratoryApplicationService(
                orders=PostgresTestOrderRepository(),
                samples=PostgresSampleRepository(),
            )
        else:
            _service = LaboratoryApplicationService(
                orders=InMemoryTestOrderRepository(),
                samples=InMemorySampleRepository(),
            )
    if not _registered:
        InProcessEventBus.subscribe(
            "hospital.encounter.started",
            handle_hospital_encounter_started,
        )
        InProcessEventBus.subscribe(
            "hospital.encounter.completed",
            handle_hospital_encounter_completed,
        )
        InProcessEventBus.subscribe(
            "clinic.encounter.completed",
            handle_clinic_encounter_completed,
        )
        _registered = True
    return _service


def reset_laboratory_service() -> None:
    global _service, _registered
    _service = None
    _registered = False
