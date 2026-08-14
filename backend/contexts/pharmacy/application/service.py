"""Pharmacy application service — CAP-HLT-008."""
from __future__ import annotations

import logging

from contexts.pharmacy.application.commands.link_hospital_encounter import (
    LinkHospitalEncounterCommand,
)
from contexts.pharmacy.application.commands.note_stock_adjusted import NoteStockAdjustedCommand
from contexts.pharmacy.domain.aggregates.dispense_record import DispenseRecord
from contexts.pharmacy.domain.aggregates.prescription import Prescription
from contexts.pharmacy.domain.events.integration_events import (
    DispenseCompletedIntegration,
    PrescriptionReceivedIntegration,
)
from contexts.pharmacy.domain.ports.repositories import IDispenseRepository, IPrescriptionRepository
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.messaging.event_bus import publish_integration_event

logger = logging.getLogger(__name__)


class PharmacyApplicationService:
    def __init__(
        self,
        prescriptions: IPrescriptionRepository,
        dispenses: IDispenseRepository,
    ) -> None:
        self._prescriptions = prescriptions
        self._dispenses = dispenses

    async def link_hospital_encounter(self, command: LinkHospitalEncounterCommand) -> Result[dict]:
        """Idempotent encounter-linked review Rx — peer IDs only (ACL entry)."""
        return await self._link_care_encounter(command, rx_prefix="HOSP")

    async def link_clinic_encounter(self, command: LinkHospitalEncounterCommand) -> Result[dict]:
        """Idempotent clinic encounter → REVIEW Rx (peer IDs only)."""
        return await self._link_care_encounter(command, rx_prefix="CLN")

    async def _link_care_encounter(
        self, command: LinkHospitalEncounterCommand, *, rx_prefix: str
    ) -> Result[dict]:
        if not command.tenant_id or not command.encounter_ref or not command.patient_ref:
            return Result.fail("pharmacy.errors.invalid_encounter_link")
        short = command.encounter_ref.replace("-", "")[:12].upper()
        rx_number = f"{rx_prefix}-{short}"
        existing = await self._prescriptions.find_by_rx_number(command.tenant_id, rx_number)
        if existing:
            return Result.ok(existing.to_dict())
        return await self.receive_prescription(
            tenant_id=command.tenant_id,
            rx_number=rx_number,
            patient_ref=command.patient_ref,
            drug_code="REVIEW",
            drug_name="Encounter review",
            quantity=1.0,
            correlation_id=command.correlation_id,
            source_encounter_ref=command.encounter_ref,
        )

    async def note_stock_adjusted(self, command: NoteStockAdjustedCommand) -> Result[dict]:
        """Inventory stock fact — pharmacy never queries inventory schema."""
        if not command.tenant_id or not command.sku:
            return Result.fail("pharmacy.errors.invalid_stock_fact")
        logger.info(
            "pharmacy noted stock adjust tenant=%s sku=%s qty=%s reason=%s",
            command.tenant_id,
            command.sku,
            command.quantity_on_hand,
            command.reason,
        )
        return Result.ok(
            {
                "noted": True,
                "sku": command.sku,
                "quantity_on_hand": command.quantity_on_hand,
            }
        )

    async def receive_prescription(
        self,
        *,
        tenant_id: str,
        rx_number: str,
        patient_ref: str,
        drug_code: str,
        drug_name: str,
        quantity: float,
        correlation_id: str,
        source_encounter_ref: str | None = None,
    ) -> Result[dict]:
        if await self._prescriptions.find_by_rx_number(tenant_id, rx_number):
            return Result.fail("pharmacy.errors.rx_number_exists")
        try:
            prescription = Prescription.receive(
                tenant_id=tenant_id,
                rx_number=rx_number,
                patient_ref=patient_ref,
                drug_code=drug_code,
                drug_name=drug_name,
                quantity=quantity,
                source_encounter_ref=source_encounter_ref,
            )
        except ValueError as exc:
            return Result.fail(str(exc))
        await self._prescriptions.save(prescription)
        await publish_integration_event(
            PrescriptionReceivedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                prescription_id=prescription.id,
                rx_number=prescription.rx_number,
                patient_ref=prescription.patient_ref,
                drug_code=prescription.drug_code,
            )
        )
        return Result.ok(prescription.to_dict())

    async def list_prescriptions(
        self, tenant_id: str, *, limit: int = 50, offset: int = 0
    ) -> Result[dict]:
        limit = max(1, min(limit, 100))
        offset = max(0, offset)
        rows = await self._prescriptions.list_prescriptions(tenant_id)
        page = rows[offset : offset + limit]
        return Result.ok(
            {"items": [r.to_dict() for r in page], "total": len(rows), "limit": limit, "offset": offset}
        )

    async def dispense(
        self,
        *,
        tenant_id: str,
        prescription_id: str,
        quantity_dispensed: float | None,
        correlation_id: str,
        dispensed_by: str | None = None,
    ) -> Result[dict]:
        prescription = await self._prescriptions.find_by_id(
            tenant_id, UniqueId.from_string(prescription_id)
        )
        if not prescription:
            return Result.fail("pharmacy.errors.prescription_not_found")
        qty = float(quantity_dispensed) if quantity_dispensed is not None else prescription.quantity
        try:
            prescription.mark_dispensed()
            dispense = DispenseRecord.create(
                tenant_id=tenant_id,
                prescription_id=prescription.id,
                patient_ref=prescription.patient_ref,
                drug_code=prescription.drug_code,
                quantity_dispensed=qty,
                dispensed_by=dispensed_by,
            )
        except ValueError as exc:
            return Result.fail(str(exc))
        await self._prescriptions.save(prescription)
        await self._dispenses.save(dispense)
        await publish_integration_event(
            DispenseCompletedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                dispense_id=dispense.id,
                prescription_id=prescription.id,
                patient_ref=dispense.patient_ref,
                drug_code=dispense.drug_code,
                quantity_dispensed=dispense.quantity_dispensed,
            )
        )
        return Result.ok(dispense.to_dict())

    async def list_dispenses(
        self, tenant_id: str, *, limit: int = 50, offset: int = 0
    ) -> Result[dict]:
        limit = max(1, min(limit, 100))
        offset = max(0, offset)
        rows = await self._dispenses.list_dispenses(tenant_id)
        page = rows[offset : offset + limit]
        return Result.ok(
            {"items": [r.to_dict() for r in page], "total": len(rows), "limit": limit, "offset": offset}
        )
