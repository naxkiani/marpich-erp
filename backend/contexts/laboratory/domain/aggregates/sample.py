"""Laboratory sample — CAP-HLT-007."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class Sample(AggregateRoot):
    tenant_id: str
    order_id: UniqueId
    accession_number: str
    specimen_type: str
    patient_ref: str
    received_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def receive(
        cls,
        *,
        tenant_id: str,
        order_id: UniqueId,
        accession_number: str,
        specimen_type: str,
        patient_ref: str,
    ) -> Sample:
        accession = accession_number.strip().upper()
        if not accession:
            raise ValueError("laboratory.errors.accession_required")
        specimen = specimen_type.strip()
        if not specimen:
            raise ValueError("laboratory.errors.specimen_type_required")
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            order_id=order_id,
            accession_number=accession,
            specimen_type=specimen,
            patient_ref=patient_ref,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "order_id": str(self.order_id),
            "accession_number": self.accession_number,
            "specimen_type": self.specimen_type,
            "patient_ref": self.patient_ref,
            "received_at": self.received_at.isoformat(),
        }
