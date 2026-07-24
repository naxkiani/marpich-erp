"""ACL — Laboratory integration envelopes → Hospital care-event commands."""
from __future__ import annotations

from contexts.hospital.application.commands.record_care_event import (
    RecordLabResultCareEventCommand,
)


class LaboratoryEventAdapter:
    def parse_result_available(self, envelope: dict) -> RecordLabResultCareEventCommand:
        payload = envelope.get("payload") or {}
        return RecordLabResultCareEventCommand(
            tenant_id=str(envelope.get("tenant_id") or ""),
            correlation_id=str(envelope.get("correlation_id") or ""),
            source_event_id=str(envelope.get("event_id") or ""),
            patient_ref=str(payload.get("patient_ref") or ""),
            peer_order_id=str(payload.get("order_id") or ""),
            test_code=str(payload.get("test_code") or ""),
            result_value=str(payload.get("result_value") or ""),
            result_unit=payload.get("result_unit"),
        )


def parse_result_available(envelope: dict) -> RecordLabResultCareEventCommand:
    return LaboratoryEventAdapter().parse_result_available(envelope)
