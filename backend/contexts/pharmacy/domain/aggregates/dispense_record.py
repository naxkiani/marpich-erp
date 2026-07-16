"""Pharmacy dispense record — CAP-HLT-008."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class DispenseRecord(AggregateRoot):
    tenant_id: str
    prescription_id: UniqueId
    patient_ref: str
    drug_code: str
    quantity_dispensed: float
    dispensed_by: str | None = None
    dispensed_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        prescription_id: UniqueId,
        patient_ref: str,
        drug_code: str,
        quantity_dispensed: float,
        dispensed_by: str | None = None,
    ) -> DispenseRecord:
        qty = float(quantity_dispensed)
        if qty <= 0:
            raise ValueError("pharmacy.errors.invalid_quantity")
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            prescription_id=prescription_id,
            patient_ref=patient_ref,
            drug_code=drug_code,
            quantity_dispensed=qty,
            dispensed_by=dispensed_by,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "prescription_id": str(self.prescription_id),
            "patient_ref": self.patient_ref,
            "drug_code": self.drug_code,
            "quantity_dispensed": self.quantity_dispensed,
            "dispensed_by": self.dispensed_by,
            "dispensed_at": self.dispensed_at.isoformat(),
        }
