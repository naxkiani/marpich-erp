"""Hospital DI container."""
from __future__ import annotations

from contexts.hospital.application.ai_service import HospitalAIService
from contexts.hospital.application.service import HospitalApplicationService
from contexts.hospital.infrastructure.acl.laboratory_events import LaboratoryEventAdapter
from contexts.hospital.infrastructure.acl.pharmacy_events import PharmacyEventAdapter
from contexts.hospital.infrastructure.persistence.memory_store import (
    InMemoryAdmissionRepository,
    InMemoryBedRepository,
    InMemoryCareEventProjectionRepository,
    InMemoryEncounterRepository,
    InMemoryPatientRepository,
)
from contexts.hospital.infrastructure.persistence.postgres_store import (
    PostgresAdmissionRepository,
    PostgresBedRepository,
    PostgresCareEventProjectionRepository,
    PostgresEncounterRepository,
    PostgresPatientRepository,
)
from shared.infrastructure.messaging.event_bus import InProcessEventBus
from shared.infrastructure.settings import use_postgres

_service: HospitalApplicationService | None = None
_ai_service: HospitalAIService | None = None
_registered = False


def get_hospital_service() -> HospitalApplicationService:
    global _service, _registered
    if _service is None:
        lab_acl = LaboratoryEventAdapter()
        pharmacy_acl = PharmacyEventAdapter()
        if use_postgres():
            _service = HospitalApplicationService(
                patients=PostgresPatientRepository(),
                admissions=PostgresAdmissionRepository(),
                encounters=PostgresEncounterRepository(),
                beds=PostgresBedRepository(),
                care_events=PostgresCareEventProjectionRepository(),
                laboratory_events=lab_acl,
                pharmacy_events=pharmacy_acl,
            )
        else:
            _service = HospitalApplicationService(
                patients=InMemoryPatientRepository(),
                admissions=InMemoryAdmissionRepository(),
                encounters=InMemoryEncounterRepository(),
                beds=InMemoryBedRepository(),
                care_events=InMemoryCareEventProjectionRepository(),
                laboratory_events=lab_acl,
                pharmacy_events=pharmacy_acl,
            )
    if not _registered:
        InProcessEventBus.subscribe(
            "laboratory.result.available",
            _service.handle_laboratory_result_available,
        )
        InProcessEventBus.subscribe(
            "pharmacy.dispense.completed",
            _service.handle_pharmacy_dispense_completed,
        )
        _registered = True
    return _service


def get_hospital_ai_service() -> HospitalAIService:
    global _ai_service
    if _ai_service is None:
        _ai_service = HospitalAIService()
    return _ai_service


def reset_hospital_service() -> None:
    global _service, _ai_service, _registered
    _service = None
    _ai_service = None
    _registered = False
