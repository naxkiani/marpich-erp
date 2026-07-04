"""Outpatient encounter aggregate — clinic bounded context."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId

from contexts.clinic.domain.events.integration_events import EncounterCompletedIntegration


class OutpatientEncounterStatus(StrEnum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass(eq=False, kw_only=True)
class OutpatientEncounter(AggregateRoot):
    tenant_id: str
    patient_id: UniqueId
    appointment_id: UniqueId
    status: OutpatientEncounterStatus = OutpatientEncounterStatus.IN_PROGRESS
    diagnosis_codes: list[str] = field(default_factory=list)
    started_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    completed_at: datetime | None = None

    @classmethod
    def start(
        cls,
        *,
        tenant_id: str,
        patient_id: UniqueId,
        appointment_id: UniqueId,
    ) -> OutpatientEncounter:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            patient_id=patient_id,
            appointment_id=appointment_id,
        )

    def complete(self, *, correlation_id: str, diagnosis_codes: list[str] | None = None) -> EncounterCompletedIntegration:
        if self.status == OutpatientEncounterStatus.COMPLETED:
            raise ValueError("clinic.errors.encounter_already_completed")
        if diagnosis_codes:
            self.diagnosis_codes.extend(diagnosis_codes)
        self.status = OutpatientEncounterStatus.COMPLETED
        self.completed_at = datetime.now(UTC)
        return EncounterCompletedIntegration(
            tenant_id=TenantId.create(self.tenant_id),
            correlation_id=correlation_id,
            encounter_id=self.id,
            patient_id=self.patient_id,
            appointment_id=self.appointment_id,
            diagnosis_codes=tuple(self.diagnosis_codes),
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "patient_id": str(self.patient_id),
            "appointment_id": str(self.appointment_id),
            "status": self.status.value,
            "diagnosis_codes": self.diagnosis_codes,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }
