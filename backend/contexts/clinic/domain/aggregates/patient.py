"""Clinic patient aggregate — ambulatory care (CAP-HLT-002).

Stores document_id references only — clinical files live in Document Exchange.
Never share tables with hospital.patient.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class ClinicPatient(AggregateRoot):
    tenant_id: str
    patient_number: str
    first_name: str
    last_name: str
    date_of_birth: str
    document_id: str | None = None
    identity_user_id: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(
        cls,
        *,
        tenant_id: str,
        patient_number: str,
        first_name: str,
        last_name: str,
        date_of_birth: str,
        document_id: str | None = None,
        identity_user_id: str | None = None,
    ) -> ClinicPatient:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            patient_number=patient_number.strip().upper(),
            first_name=first_name.strip(),
            last_name=last_name.strip(),
            date_of_birth=date_of_birth,
            document_id=document_id,
            identity_user_id=identity_user_id,
        )

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def attach_chart_document(self, document_id: str) -> None:
        self.document_id = document_id

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "patient_number": self.patient_number,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "date_of_birth": self.date_of_birth,
            "document_id": self.document_id,
            "identity_user_id": self.identity_user_id,
            "created_at": self.created_at.isoformat(),
        }
