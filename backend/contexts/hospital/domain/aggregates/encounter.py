"""Encounter aggregate — Hospital bounded context."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId

from contexts.hospital.domain.events.integration_events import EncounterCompletedIntegration


class EncounterStatus(StrEnum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass(eq=False, kw_only=True)
class Encounter(AggregateRoot):
    tenant_id: str
    patient_id: UniqueId
    admission_id: UniqueId
    status: EncounterStatus = EncounterStatus.IN_PROGRESS
    procedure_codes: list[str] = field(default_factory=list)
    diagnosis_codes: list[str] = field(default_factory=list)
    started_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    completed_at: datetime | None = None

    @classmethod
    def start(
        cls,
        *,
        tenant_id: str,
        patient_id: UniqueId,
        admission_id: UniqueId,
    ) -> Encounter:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            patient_id=patient_id,
            admission_id=admission_id,
        )

    def add_procedure(self, code: str) -> None:
        if self.status != EncounterStatus.IN_PROGRESS:
            raise ValueError("Cannot modify completed encounter")
        if code not in self.procedure_codes:
            self.procedure_codes.append(code)

    def complete(
        self,
        *,
        correlation_id: str,
    ) -> EncounterCompletedIntegration:
        if self.status == EncounterStatus.COMPLETED:
            raise ValueError("Encounter already completed")
        self.status = EncounterStatus.COMPLETED
        self.completed_at = datetime.now(UTC)
        return EncounterCompletedIntegration(
            tenant_id=TenantId.create(self.tenant_id),
            correlation_id=correlation_id,
            encounter_id=self.id,
            patient_id=self.patient_id,
            admission_id=self.admission_id,
            procedure_codes=tuple(self.procedure_codes),
            diagnosis_codes=tuple(self.diagnosis_codes),
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "patient_id": str(self.patient_id),
            "admission_id": str(self.admission_id),
            "status": self.status.value,
            "procedure_codes": self.procedure_codes,
            "diagnosis_codes": self.diagnosis_codes,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }
