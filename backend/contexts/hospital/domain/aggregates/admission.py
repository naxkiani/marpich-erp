"""Admission aggregate."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId

from contexts.hospital.domain.events.integration_events import AdmissionRegisteredIntegration


class AdmissionStatus(StrEnum):
    ACTIVE = "active"
    DISCHARGED = "discharged"


@dataclass(eq=False, kw_only=True)
class Admission(AggregateRoot):
    tenant_id: str
    patient_id: UniqueId
    ward: str
    status: AdmissionStatus = AdmissionStatus.ACTIVE
    admitted_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(
        cls,
        *,
        tenant_id: str,
        patient_id: UniqueId,
        ward: str,
        correlation_id: str,
    ) -> tuple[Admission, AdmissionRegisteredIntegration]:
        admission = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            patient_id=patient_id,
            ward=ward.strip(),
        )
        event = AdmissionRegisteredIntegration(
            tenant_id=TenantId.create(tenant_id),
            correlation_id=correlation_id,
            admission_id=admission.id,
            patient_id=patient_id,
        )
        return admission, event

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "patient_id": str(self.patient_id),
            "ward": self.ward,
            "status": self.status.value,
            "admitted_at": self.admitted_at.isoformat(),
        }
