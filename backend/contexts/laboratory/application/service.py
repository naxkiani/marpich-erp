"""Laboratory application service — CAP-HLT-007."""
from __future__ import annotations

import logging

from contexts.laboratory.application.commands.link_hospital_encounter import (
    LinkHospitalEncounterCommand,
)
from contexts.laboratory.domain.aggregates.sample import Sample
from contexts.laboratory.domain.aggregates.test_order import TestOrder
from contexts.laboratory.domain.events.integration_events import (
    ResultAvailableIntegration,
    SampleReceivedIntegration,
)
from contexts.laboratory.domain.ports.repositories import ISampleRepository, ITestOrderRepository
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.messaging.event_bus import publish_integration_event

logger = logging.getLogger(__name__)


class LaboratoryApplicationService:
    def __init__(
        self,
        orders: ITestOrderRepository,
        samples: ISampleRepository,
    ) -> None:
        self._orders = orders
        self._samples = samples

    async def link_hospital_encounter(self, command: LinkHospitalEncounterCommand) -> Result[dict]:
        """Idempotent encounter-linked review order — peer IDs only (ACL entry)."""
        return await self._link_care_encounter(command, order_prefix="HOSP")

    async def link_clinic_encounter(self, command: LinkHospitalEncounterCommand) -> Result[dict]:
        """Idempotent clinic encounter → REVIEW order (peer IDs only)."""
        return await self._link_care_encounter(command, order_prefix="CLN")

    async def _link_care_encounter(
        self, command: LinkHospitalEncounterCommand, *, order_prefix: str
    ) -> Result[dict]:
        if not command.tenant_id or not command.encounter_ref or not command.patient_ref:
            return Result.fail("laboratory.errors.invalid_encounter_link")
        short = command.encounter_ref.replace("-", "")[:12].upper()
        order_number = f"{order_prefix}-{short}"
        existing = await self._orders.find_by_number(command.tenant_id, order_number)
        if existing:
            return Result.ok(existing.to_dict())
        if command.phase == "started":
            logger.info(
                "laboratory encounter started noted tenant=%s encounter=%s",
                command.tenant_id,
                command.encounter_ref,
            )
            return Result.ok({"noted": True, "phase": "started", "encounter_ref": command.encounter_ref})
        return await self.place_order(
            tenant_id=command.tenant_id,
            order_number=order_number,
            patient_ref=command.patient_ref,
            test_code="REVIEW",
            correlation_id=command.correlation_id,
            source_encounter_ref=command.encounter_ref,
        )

    async def place_order(
        self,
        *,
        tenant_id: str,
        order_number: str,
        patient_ref: str,
        test_code: str,
        correlation_id: str,
        source_encounter_ref: str | None = None,
    ) -> Result[dict]:
        if await self._orders.find_by_number(tenant_id, order_number):
            return Result.fail("laboratory.errors.order_number_exists")
        try:
            order = TestOrder.place(
                tenant_id=tenant_id,
                order_number=order_number,
                patient_ref=patient_ref,
                test_code=test_code,
                source_encounter_ref=source_encounter_ref,
            )
        except ValueError as exc:
            return Result.fail(str(exc))
        await self._orders.save(order)
        return Result.ok(order.to_dict())

    async def list_orders(
        self, tenant_id: str, *, limit: int = 50, offset: int = 0
    ) -> Result[dict]:
        limit = max(1, min(limit, 100))
        offset = max(0, offset)
        rows = await self._orders.list_orders(tenant_id)
        page = rows[offset : offset + limit]
        return Result.ok(
            {"items": [r.to_dict() for r in page], "total": len(rows), "limit": limit, "offset": offset}
        )

    async def receive_sample(
        self,
        *,
        tenant_id: str,
        order_id: str,
        accession_number: str,
        specimen_type: str,
        correlation_id: str,
    ) -> Result[dict]:
        order = await self._orders.find_by_id(tenant_id, UniqueId.from_string(order_id))
        if not order:
            return Result.fail("laboratory.errors.order_not_found")
        try:
            sample = Sample.receive(
                tenant_id=tenant_id,
                order_id=order.id,
                accession_number=accession_number,
                specimen_type=specimen_type,
                patient_ref=order.patient_ref,
            )
            order.mark_sample_received()
        except ValueError as exc:
            return Result.fail(str(exc))
        await self._samples.save(sample)
        await self._orders.save(order)
        await publish_integration_event(
            SampleReceivedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                sample_id=sample.id,
                order_id=order.id,
                accession_number=sample.accession_number,
                patient_ref=sample.patient_ref,
            )
        )
        return Result.ok(sample.to_dict())

    async def list_samples(
        self, tenant_id: str, *, limit: int = 50, offset: int = 0
    ) -> Result[dict]:
        limit = max(1, min(limit, 100))
        offset = max(0, offset)
        rows = await self._samples.list_samples(tenant_id)
        page = rows[offset : offset + limit]
        return Result.ok(
            {"items": [r.to_dict() for r in page], "total": len(rows), "limit": limit, "offset": offset}
        )

    async def finalize_result(
        self,
        *,
        tenant_id: str,
        order_id: str,
        result_value: str,
        correlation_id: str,
        result_unit: str | None = None,
    ) -> Result[dict]:
        order = await self._orders.find_by_id(tenant_id, UniqueId.from_string(order_id))
        if not order:
            return Result.fail("laboratory.errors.order_not_found")
        try:
            order.finalize_result(result_value=result_value, result_unit=result_unit)
        except ValueError as exc:
            return Result.fail(str(exc))
        await self._orders.save(order)
        await publish_integration_event(
            ResultAvailableIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                order_id=order.id,
                patient_ref=order.patient_ref,
                test_code=order.test_code,
                result_value=order.result_value or "",
                result_unit=order.result_unit,
            )
        )
        return Result.ok(order.to_dict())
