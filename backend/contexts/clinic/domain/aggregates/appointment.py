"""Clinic appointment aggregate."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId

from contexts.clinic.domain.events.integration_events import AppointmentScheduledIntegration


class AppointmentStatus(StrEnum):
    SCHEDULED = "scheduled"
    CHECKED_IN = "checked_in"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


@dataclass(eq=False, kw_only=True)
class Appointment(AggregateRoot):
    tenant_id: str
    patient_id: UniqueId
    provider_name: str
    scheduled_at: datetime
    status: AppointmentStatus = AppointmentStatus.SCHEDULED
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def schedule(
        cls,
        *,
        tenant_id: str,
        patient_id: UniqueId,
        provider_name: str,
        scheduled_at: datetime,
        correlation_id: str,
    ) -> tuple[Appointment, AppointmentScheduledIntegration]:
        appointment = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            patient_id=patient_id,
            provider_name=provider_name.strip(),
            scheduled_at=scheduled_at,
        )
        event = AppointmentScheduledIntegration(
            tenant_id=TenantId.create(tenant_id),
            correlation_id=correlation_id,
            appointment_id=appointment.id,
            patient_id=patient_id,
            scheduled_at=scheduled_at.isoformat(),
        )
        return appointment, event

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "patient_id": str(self.patient_id),
            "provider_name": self.provider_name,
            "scheduled_at": self.scheduled_at.isoformat(),
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
        }
