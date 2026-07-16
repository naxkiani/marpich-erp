"""Pharmacy application service — CAP-HLT-008."""
from __future__ import annotations

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


class PharmacyApplicationService:
    def __init__(
        self,
        prescriptions: IPrescriptionRepository,
        dispenses: IDispenseRepository,
    ) -> None:
        self._prescriptions = prescriptions
        self._dispenses = dispenses

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
