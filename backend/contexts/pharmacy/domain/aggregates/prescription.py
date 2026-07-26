"""Pharmacy prescription aggregate — CAP-HLT-008.

Lifecycle: received → dispensed → counselled.
Stores peer patient_ref only (hospital/clinic UniqueId string) — never shared patient tables.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class Prescription(AggregateRoot):
    tenant_id: str
    rx_number: str
    patient_ref: str
    drug_code: str
    drug_name: str
    quantity: float
    status: str = "received"
    source_encounter_ref: str | None = None
    counseling_notes: str | None = None
    counselled_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def receive(
        cls,
        *,
        tenant_id: str,
        rx_number: str,
        patient_ref: str,
        drug_code: str,
        drug_name: str,
        quantity: float,
        source_encounter_ref: str | None = None,
    ) -> Prescription:
        qty = float(quantity)
        if qty <= 0:
            raise ValueError("pharmacy.errors.invalid_quantity")
        ref = patient_ref.strip()
        if not ref:
            raise ValueError("pharmacy.errors.patient_ref_required")
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            rx_number=rx_number.strip().upper(),
            patient_ref=ref,
            drug_code=drug_code.strip().upper(),
            drug_name=drug_name.strip(),
            quantity=qty,
            status="received",
            source_encounter_ref=source_encounter_ref,
        )

    def mark_dispensed(self) -> None:
        if self.status != "received":
            raise ValueError("pharmacy.errors.dispense_requires_received")
        self.status = "dispensed"

    def record_counseling(self, *, notes: str | None = None) -> None:
        if self.status != "dispensed":
            raise ValueError("pharmacy.errors.counsel_requires_dispensed")
        text = (notes or "").strip()
        self.counseling_notes = text or None
        self.counselled_at = datetime.now(UTC)
        self.status = "counselled"

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "rx_number": self.rx_number,
            "patient_ref": self.patient_ref,
            "drug_code": self.drug_code,
            "drug_name": self.drug_name,
            "quantity": self.quantity,
            "status": self.status,
            "source_encounter_ref": self.source_encounter_ref,
            "counseling_notes": self.counseling_notes,
            "counselled_at": self.counselled_at.isoformat() if self.counselled_at else None,
            "created_at": self.created_at.isoformat(),
        }
