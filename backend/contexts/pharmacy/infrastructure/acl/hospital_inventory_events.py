"""ACL — Hospital + Inventory envelopes → Pharmacy commands (no peer domain imports)."""
from __future__ import annotations

import logging

from contexts.pharmacy.application.commands.link_hospital_encounter import (
    LinkHospitalEncounterCommand,
)
from contexts.pharmacy.application.commands.note_stock_adjusted import NoteStockAdjustedCommand

logger = logging.getLogger(__name__)


class HospitalEventAdapter:
    def parse_encounter_completed(self, envelope: dict) -> LinkHospitalEncounterCommand:
        payload = envelope.get("payload") if isinstance(envelope.get("payload"), dict) else {}
        return LinkHospitalEncounterCommand(
            tenant_id=str(envelope.get("tenant_id") or ""),
            correlation_id=str(envelope.get("correlation_id") or envelope.get("event_id") or ""),
            encounter_ref=str(payload.get("encounter_id") or ""),
            patient_ref=str(payload.get("patient_id") or ""),
        )


class InventoryEventAdapter:
    def parse_stock_adjusted(self, envelope: dict) -> NoteStockAdjustedCommand:
        payload = envelope.get("payload") if isinstance(envelope.get("payload"), dict) else {}
        return NoteStockAdjustedCommand(
            tenant_id=str(envelope.get("tenant_id") or ""),
            correlation_id=str(envelope.get("correlation_id") or envelope.get("event_id") or ""),
            sku=str(payload.get("sku") or ""),
            quantity_on_hand=float(payload.get("quantity_on_hand") or 0),
            reason=str(payload.get("reason") or ""),
        )


async def handle_hospital_encounter_completed(envelope: dict) -> None:
    if str(envelope.get("event_name") or "") != "hospital.encounter.completed":
        return
    from contexts.pharmacy.container import get_pharmacy_service

    cmd = HospitalEventAdapter().parse_encounter_completed(envelope)
    await get_pharmacy_service().link_hospital_encounter(cmd)


async def handle_inventory_stock_adjusted(envelope: dict) -> None:
    if str(envelope.get("event_name") or "") != "inventory.stock.adjusted":
        return
    from contexts.pharmacy.container import get_pharmacy_service

    cmd = InventoryEventAdapter().parse_stock_adjusted(envelope)
    result = await get_pharmacy_service().note_stock_adjusted(cmd)
    if not result.succeeded:
        logger.warning("pharmacy stock ACL: %s", result.error)
