"""Hospital integration events — published language."""
from __future__ import annotations

from dataclasses import dataclass, field

from shared.domain.events.integration_event import IntegrationEvent
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(frozen=True, kw_only=True)
class EncounterCompletedIntegration(IntegrationEvent):
    encounter_id: UniqueId
    patient_id: UniqueId
    admission_id: UniqueId
    procedure_codes: tuple[str, ...] = field(default_factory=tuple)
    diagnosis_codes: tuple[str, ...] = field(default_factory=tuple)

    @property
    def event_name(self) -> str:
        return "hospital.encounter.completed"

    @property
    def source_context(self) -> str:
        return "hospital"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "encounter_id": str(self.encounter_id),
            "patient_id": str(self.patient_id),
            "admission_id": str(self.admission_id),
            "procedure_codes": list(self.procedure_codes),
            "diagnosis_codes": list(self.diagnosis_codes),
        }


@dataclass(frozen=True, kw_only=True)
class AdmissionRegisteredIntegration(IntegrationEvent):
    admission_id: UniqueId
    patient_id: UniqueId

    @property
    def event_name(self) -> str:
        return "hospital.admission.registered"

    @property
    def source_context(self) -> str:
        return "hospital"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "admission_id": str(self.admission_id),
            "patient_id": str(self.patient_id),
        }
