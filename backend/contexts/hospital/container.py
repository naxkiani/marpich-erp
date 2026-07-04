"""Hospital DI container."""
from __future__ import annotations

from contexts.hospital.application.service import HospitalApplicationService
from contexts.hospital.infrastructure.persistence.memory_store import (
    InMemoryAdmissionRepository,
    InMemoryEncounterRepository,
    InMemoryPatientRepository,
)
from contexts.hospital.infrastructure.persistence.postgres_store import (
    PostgresAdmissionRepository,
    PostgresEncounterRepository,
    PostgresPatientRepository,
)
from shared.infrastructure.settings import use_postgres

_service: HospitalApplicationService | None = None


def get_hospital_service() -> HospitalApplicationService:
    global _service
    if _service is None:
        if use_postgres():
            _service = HospitalApplicationService(
                patients=PostgresPatientRepository(),
                admissions=PostgresAdmissionRepository(),
                encounters=PostgresEncounterRepository(),
            )
        else:
            _service = HospitalApplicationService(
                patients=InMemoryPatientRepository(),
                admissions=InMemoryAdmissionRepository(),
                encounters=InMemoryEncounterRepository(),
            )
    return _service


def reset_hospital_service() -> None:
    global _service
    _service = None
