"""ACL — Pharmacy integration envelopes → Hospital care-event commands."""
from __future__ import annotations

from contexts.hospital.application.commands.record_care_event import (
    RecordPharmacyDispenseCareEventCommand,
)


class PharmacyEventAdapter:
    def parse_dispense_completed(
        self, envelope: dict
    ) -> RecordPharmacyDispenseCareEventCommand:
        payload = envelope.get("payload") or {}
        qty = payload.get("quantity_dispensed")
        try:
            quantity = float(qty) if qty is not None else 0.0
        except (TypeError, ValueError):
            quantity = 0.0
        return RecordPharmacyDispenseCareEventCommand(
            tenant_id=str(envelope.get("tenant_id") or ""),
            correlation_id=str(envelope.get("correlation_id") or ""),
            source_event_id=str(envelope.get("event_id") or ""),
            patient_ref=str(payload.get("patient_ref") or ""),
            peer_dispense_id=str(payload.get("dispense_id") or ""),
            peer_prescription_id=str(payload.get("prescription_id") or ""),
            drug_code=str(payload.get("drug_code") or ""),
            quantity_dispensed=quantity,
        )


def parse_dispense_completed(envelope: dict) -> RecordPharmacyDispenseCareEventCommand:
    return PharmacyEventAdapter().parse_dispense_completed(envelope)
