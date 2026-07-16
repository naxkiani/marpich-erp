"""Pharmacy integration events — CAP-HLT-008 published language."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(frozen=True, kw_only=True)
class PrescriptionReceivedIntegration(IntegrationEvent):
    prescription_id: UniqueId
    rx_number: str
    patient_ref: str
    drug_code: str

    @property
    def event_name(self) -> str:
        return "pharmacy.prescription.received"

    @property
    def source_context(self) -> str:
        return "pharmacy"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "prescription_id": str(self.prescription_id),
            "rx_number": self.rx_number,
            "patient_ref": self.patient_ref,
            "drug_code": self.drug_code,
        }


@dataclass(frozen=True, kw_only=True)
class DispenseCompletedIntegration(IntegrationEvent):
    dispense_id: UniqueId
    prescription_id: UniqueId
    patient_ref: str
    drug_code: str
    quantity_dispensed: float

    @property
    def event_name(self) -> str:
        return "pharmacy.dispense.completed"

    @property
    def source_context(self) -> str:
        return "pharmacy"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "dispense_id": str(self.dispense_id),
            "prescription_id": str(self.prescription_id),
            "patient_ref": self.patient_ref,
            "drug_code": self.drug_code,
            "quantity_dispensed": self.quantity_dispensed,
        }
