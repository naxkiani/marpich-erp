"""Hospital DI container + laboratory result ACL subscription."""
from __future__ import annotations

from contexts.hospital.application.service import HospitalApplicationService
from contexts.hospital.infrastructure.acl.laboratory_events import (
    make_laboratory_result_handler,
)
from contexts.hospital.infrastructure.persistence.lab_result_postgres import (
    PostgresLabResultProjectionRepository,
)
from contexts.hospital.infrastructure.persistence.memory_store import (
    InMemoryAdmissionRepository,
    InMemoryEncounterRepository,
    InMemoryLabResultProjectionRepository,
    InMemoryPatientRepository,
)
from contexts.hospital.infrastructure.persistence.postgres_store import (
    PostgresAdmissionRepository,
    PostgresEncounterRepository,
    PostgresPatientRepository,
)
from shared.infrastructure.messaging.event_bus import InProcessEventBus
from shared.infrastructure.settings import use_postgres

_service: HospitalApplicationService | None = None
_registered = False


def get_hospital_service() -> HospitalApplicationService:
    global _service, _registered
    if _service is None:
        if use_postgres():
            _service = HospitalApplicationService(
                patients=PostgresPatientRepository(),
                admissions=PostgresAdmissionRepository(),
                encounters=PostgresEncounterRepository(),
                lab_projections=PostgresLabResultProjectionRepository(),
            )
        else:
            _service = HospitalApplicationService(
                patients=InMemoryPatientRepository(),
                admissions=InMemoryAdmissionRepository(),
                encounters=InMemoryEncounterRepository(),
                lab_projections=InMemoryLabResultProjectionRepository(),
            )
    if not _registered:
        InProcessEventBus.subscribe(
            "laboratory.result.available",
            make_laboratory_result_handler(get_hospital_service),
        )
        _registered = True
    return _service


def reset_hospital_service() -> None:
    global _service, _registered
    _service = None
    _registered = False
