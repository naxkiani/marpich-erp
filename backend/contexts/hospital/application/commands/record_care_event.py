"""Commands — project peer care events into Hospital (peer IDs + summary only)."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RecordLabResultCareEventCommand:
    tenant_id: str
    correlation_id: str
    source_event_id: str
    patient_ref: str
    peer_order_id: str
    test_code: str
    result_value: str
    result_unit: str | None


@dataclass(frozen=True, slots=True)
class RecordPharmacyDispenseCareEventCommand:
    tenant_id: str
    correlation_id: str
    source_event_id: str
    patient_ref: str
    peer_dispense_id: str
    peer_prescription_id: str
    drug_code: str
    quantity_dispensed: float
