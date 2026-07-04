"""Accounting application service."""
from __future__ import annotations

import json
from datetime import UTC, datetime

from contexts.accounting.application.commands.create_billing_from_encounter import (
    CreateBillingFromEncounterCommand,
)
from contexts.accounting.application.ports.hospital_events import IHospitalEventAdapter
from contexts.accounting.domain.aggregates.billing_encounter import BillingEncounter
from contexts.accounting.domain.events.integration_events import (
    BillingEncounterCreatedIntegration,
    JournalPostedIntegration,
)
from contexts.accounting.domain.ports.repositories import IBillingRepository
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class ConsoleAccountingAudit:
    async def log(self, **kwargs: object) -> None:
        entry = {"type": "audit", "context": "accounting", **kwargs, "occurred_at": datetime.now(UTC).isoformat()}
        print(json.dumps(entry, default=str))


class AccountingApplicationService:
    def __init__(
        self,
        billings: IBillingRepository,
        hospital_events: IHospitalEventAdapter,
        audit: ConsoleAccountingAudit | None = None,
    ) -> None:
        self._billings = billings
        self._hospital_events = hospital_events
        self._audit = audit or ConsoleAccountingAudit()

    async def handle_hospital_encounter_completed(self, envelope: dict) -> None:
        """ACL entry point — called by event bus, never imports Hospital."""
        command = await self._hospital_events.parse_encounter_completed(envelope)
        await self.create_billing_from_encounter(command)

    async def create_billing_from_encounter(
        self, command: CreateBillingFromEncounterCommand
    ) -> Result[dict]:
        existing = await self._billings.find_by_external_encounter(
            command.tenant_id, command.external_encounter_id
        )
        if existing:
            return Result.ok(existing.to_dict())

        billing = BillingEncounter.from_hospital_event(
            tenant_id=command.tenant_id,
            correlation_id=command.correlation_id,
            external_encounter_id=command.external_encounter_id,
            patient_ref=command.patient_ref,
            procedure_codes=command.procedure_codes,
        )
        billing.post()

        await self._billings.save(billing)

        event = BillingEncounterCreatedIntegration(
            tenant_id=TenantId.create(command.tenant_id),
            correlation_id=command.correlation_id,
            billing_id=billing.id,
            external_encounter_id=command.external_encounter_id,
            total_amount=billing.total_amount,
            currency=billing.currency,
        )
        await publish_integration_event(event)

        journal_event = JournalPostedIntegration(
            tenant_id=TenantId.create(command.tenant_id),
            correlation_id=command.correlation_id,
            journal_id=UniqueId.generate(),
            source_type="billing_encounter",
            source_id=str(billing.id),
            currency=billing.currency,
            lines=(
                {"account_code": "1200", "account_name": "Accounts Receivable", "debit": billing.total_amount, "credit": 0.0},
                {"account_code": "4000", "account_name": "Clinical Revenue", "debit": 0.0, "credit": billing.total_amount},
            ),
        )
        await publish_integration_event(journal_event)

        await self._audit.log(
            tenant_id=command.tenant_id,
            correlation_id=command.correlation_id,
            action="accounting.billing.created",
            resource_type="billing_encounter",
            resource_id=str(billing.id),
            payload={"total_amount": billing.total_amount, "external_encounter_id": command.external_encounter_id},
        )
        return Result.ok(billing.to_dict())

    async def get_billing(self, tenant_id: str, billing_id: str) -> Result[dict]:
        billing = await self._billings.find_by_id(tenant_id, UniqueId.from_string(billing_id))
        if not billing:
            return Result.fail("accounting.errors.billing_not_found")
        return Result.ok(billing.to_dict())

    async def list_billings(self, tenant_id: str) -> Result[list[dict]]:
        billings = await self._billings.list_billings(tenant_id)
        return Result.ok([b.to_dict() for b in billings])

    async def find_by_encounter(self, tenant_id: str, encounter_id: str) -> Result[dict]:
        billing = await self._billings.find_by_external_encounter(tenant_id, encounter_id)
        if not billing:
            return Result.fail("accounting.errors.billing_not_found")
        return Result.ok(billing.to_dict())
