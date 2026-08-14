"""ACL — laboratory.result.available → Clinic local note (peer IDs only)."""
from __future__ import annotations

from contexts.clinic.application.commands.note_lab_result import NoteLabResultCommand


class LaboratoryEventAdapter:
    def parse_result_available(self, envelope: dict) -> NoteLabResultCommand:
        payload = envelope.get("payload") if isinstance(envelope.get("payload"), dict) else {}
        return NoteLabResultCommand(
            tenant_id=str(envelope.get("tenant_id") or ""),
            correlation_id=str(envelope.get("correlation_id") or envelope.get("event_id") or ""),
            order_ref=str(payload.get("order_id") or payload.get("order_number") or ""),
            patient_ref=str(payload.get("patient_ref") or payload.get("patient_id") or ""),
            test_code=str(payload.get("test_code") or ""),
            result_value=str(payload.get("result_value") or ""),
            result_unit=str(payload.get("result_unit") or ""),
        )


async def handle_laboratory_result_available(envelope: dict) -> None:
    if str(envelope.get("event_name") or "") != "laboratory.result.available":
        return
    from contexts.clinic.container import get_clinic_service

    cmd = LaboratoryEventAdapter().parse_result_available(envelope)
    await get_clinic_service().note_lab_result(cmd)
