"""Clinic integration events — published language."""
from __future__ import annotations

from dataclasses import dataclass, field

from shared.domain.events.integration_event import IntegrationEvent
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(frozen=True, kw_only=True)
class AppointmentScheduledIntegration(IntegrationEvent):
    appointment_id: UniqueId
    patient_id: UniqueId
    scheduled_at: str

    @property
    def event_name(self) -> str:
        return "clinic.appointment.scheduled"

    @property
    def source_context(self) -> str:
        return "clinic"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "appointment_id": str(self.appointment_id),
            "patient_id": str(self.patient_id),
            "scheduled_at": self.scheduled_at,
        }


@dataclass(frozen=True, kw_only=True)
class EncounterCompletedIntegration(IntegrationEvent):
    encounter_id: UniqueId
    patient_id: UniqueId
    appointment_id: UniqueId
    diagnosis_codes: tuple[str, ...] = field(default_factory=tuple)

    @property
    def event_name(self) -> str:
        return "clinic.encounter.completed"

    @property
    def source_context(self) -> str:
        return "clinic"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "encounter_id": str(self.encounter_id),
            "patient_id": str(self.patient_id),
            "appointment_id": str(self.appointment_id),
            "diagnosis_codes": list(self.diagnosis_codes),
        }


@dataclass(frozen=True, kw_only=True)
class ReferralSentIntegration(IntegrationEvent):
    referral_id: UniqueId
    encounter_id: UniqueId
    patient_id: UniqueId
    target_specialty: str

    @property
    def event_name(self) -> str:
        return "clinic.referral.sent"

    @property
    def source_context(self) -> str:
        return "clinic"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "referral_id": str(self.referral_id),
            "encounter_id": str(self.encounter_id),
            "patient_id": str(self.patient_id),
            "target_specialty": self.target_specialty,
        }
