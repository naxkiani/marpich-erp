"""Admission aggregate — CAP-HLT-001 + CAP-HLT-004 bed/transfer/discharge."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from contexts.hospital.domain.events.integration_events import (
    AdmissionDischargedIntegration,
    AdmissionRegisteredIntegration,
    AdmissionTransferredIntegration,
    BedAssignedIntegration,
)
from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId


class AdmissionStatus(StrEnum):
    ACTIVE = "active"
    DISCHARGED = "discharged"


@dataclass(eq=False, kw_only=True)
class Admission(AggregateRoot):
    tenant_id: str
    patient_id: UniqueId
    ward: str
    status: AdmissionStatus = AdmissionStatus.ACTIVE
    bed_id: UniqueId | None = None
    admitted_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    discharged_at: datetime | None = None

    def _ensure_active(self) -> None:
        if self.status != AdmissionStatus.ACTIVE:
            raise ValueError("hospital.errors.admission_not_active")

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
            ward=admission.ward,
        )
        return admission, event

    def assign_bed(
        self,
        *,
        bed_id: UniqueId,
        ward: str,
        correlation_id: str,
    ) -> BedAssignedIntegration:
        self._ensure_active()
        self.bed_id = bed_id
        self.ward = ward.strip()
        return BedAssignedIntegration(
            tenant_id=TenantId.create(self.tenant_id),
            correlation_id=correlation_id,
            admission_id=self.id,
            patient_id=self.patient_id,
            bed_id=bed_id,
            ward=self.ward,
        )

    def transfer(
        self,
        *,
        to_ward: str,
        to_bed_id: UniqueId | None,
        correlation_id: str,
    ) -> AdmissionTransferredIntegration:
        self._ensure_active()
        from_ward = self.ward
        from_bed_id = self.bed_id
        self.ward = to_ward.strip()
        self.bed_id = to_bed_id
        return AdmissionTransferredIntegration(
            tenant_id=TenantId.create(self.tenant_id),
            correlation_id=correlation_id,
            admission_id=self.id,
            patient_id=self.patient_id,
            from_ward=from_ward,
            to_ward=self.ward,
            from_bed_id=from_bed_id,
            to_bed_id=to_bed_id,
        )

    def discharge(self, *, correlation_id: str) -> AdmissionDischargedIntegration:
        self._ensure_active()
        bed_id = self.bed_id
        self.status = AdmissionStatus.DISCHARGED
        self.discharged_at = datetime.now(UTC)
        self.bed_id = None
        return AdmissionDischargedIntegration(
            tenant_id=TenantId.create(self.tenant_id),
            correlation_id=correlation_id,
            admission_id=self.id,
            patient_id=self.patient_id,
            ward=self.ward,
            bed_id=bed_id,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "patient_id": str(self.patient_id),
            "ward": self.ward,
            "status": self.status.value,
            "bed_id": str(self.bed_id) if self.bed_id else None,
            "admitted_at": self.admitted_at.isoformat(),
            "discharged_at": self.discharged_at.isoformat() if self.discharged_at else None,
        }
