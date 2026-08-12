"""Accounting application service — hospital billing + CAP-ENT-023 AR invoices.

Sales orders → draft invoice (ACL). Issue publishes accounting.invoice.issued + journal intent.
Receive payment on issued invoices publishes accounting.payment.received + cash/AR journal intent.
"""
from __future__ import annotations

import json
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation

from contexts.accounting.application.commands.create_billing_from_encounter import (
    CreateBillingFromEncounterCommand,
)
from contexts.accounting.application.ports.hospital_events import IHospitalEventAdapter
from contexts.accounting.domain.aggregates.billing_encounter import BillingEncounter
from contexts.accounting.domain.aggregates.invoice import Invoice
from contexts.accounting.domain.events.integration_events import (
    BillingEncounterCreatedIntegration,
    JournalPostedIntegration,
)
from contexts.accounting.domain.ports.repositories import IBillingRepository, IInvoiceRepository
from contexts.accounting.infrastructure.acl.sales_events import (
    DraftInvoiceFromSalesOrderCommand,
    SalesOrderEventAdapter,
)
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class ConsoleAccountingAudit:
    async def log(self, **kwargs: object) -> None:
        entry = {
            "type": "audit",
            "context": "accounting",
            **kwargs,
            "occurred_at": datetime.now(UTC).isoformat(),
        }
        print(json.dumps(entry, default=str))


class AccountingApplicationService:
    def __init__(
        self,
        billings: IBillingRepository,
        hospital_events: IHospitalEventAdapter,
        invoices: IInvoiceRepository | None = None,
        sales_events: SalesOrderEventAdapter | None = None,
        audit: ConsoleAccountingAudit | None = None,
    ) -> None:
        self._billings = billings
        self._hospital_events = hospital_events
        self._invoices = invoices
        self._sales_events = sales_events or SalesOrderEventAdapter()
        self._audit = audit or ConsoleAccountingAudit()

    async def handle_hospital_encounter_completed(self, envelope: dict) -> None:
        """ACL entry point — called by event bus, never imports Hospital."""
        command = await self._hospital_events.parse_encounter_completed(envelope)
        await self.create_billing_from_encounter(command)

    async def handle_sales_order_placed(self, envelope: dict) -> None:
        command = await self._sales_events.parse_integration_event(envelope)
        if command:
            await self.draft_invoice_from_sales_order(command)

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
                {
                    "account_code": "1200",
                    "account_name": "Accounts Receivable",
                    "debit": billing.total_amount,
                    "credit": 0.0,
                },
                {
                    "account_code": "4000",
                    "account_name": "Clinical Revenue",
                    "debit": 0.0,
                    "credit": billing.total_amount,
                },
            ),
        )
        await publish_integration_event(journal_event)

        await self._audit.log(
            tenant_id=command.tenant_id,
            correlation_id=command.correlation_id,
            action="accounting.billing.created",
            resource_type="billing_encounter",
            resource_id=str(billing.id),
            payload={
                "total_amount": billing.total_amount,
                "external_encounter_id": command.external_encounter_id,
            },
        )
        return Result.ok(billing.to_dict())

    async def draft_invoice_from_sales_order(
        self, command: DraftInvoiceFromSalesOrderCommand
    ) -> Result[dict]:
        if self._invoices is None:
            return Result.fail("accounting.errors.invoices_unavailable")
        order_id = UniqueId.from_string(command.sales_order_id)
        existing = await self._invoices.find_by_sales_order(command.tenant_id, order_id)
        if existing:
            return Result.ok(existing.to_dict())
        try:
            amount = Decimal(command.amount)
        except (InvalidOperation, ValueError):
            return Result.fail("accounting.errors.invalid_amount")
        try:
            invoice = Invoice.draft_from_sales_order(
                tenant_id=command.tenant_id,
                sales_order_id=order_id,
                contact_id=UniqueId.from_string(command.contact_id),
                title=command.title,
                amount=amount,
                currency=command.currency,
                line_items=list(command.line_items),
                correlation_id=command.correlation_id,
            )
        except ValueError as exc:
            return Result.fail(str(exc))
        await self._invoices.save(invoice)
        await self._audit.log(
            tenant_id=command.tenant_id,
            correlation_id=command.correlation_id,
            action="accounting.invoice.drafted",
            resource_type="invoice",
            resource_id=str(invoice.id),
            payload={"sales_order_id": command.sales_order_id, "amount": str(amount)},
        )
        return Result.ok(invoice.to_dict())

    async def issue_invoice(
        self, *, tenant_id: str, invoice_id: str, correlation_id: str
    ) -> Result[dict]:
        if self._invoices is None:
            return Result.fail("accounting.errors.invoices_unavailable")
        invoice = await self._invoices.find_by_id(tenant_id, UniqueId.from_string(invoice_id))
        if not invoice:
            return Result.fail("accounting.errors.invoice_not_found")
        try:
            issued_event = invoice.issue(correlation_id=correlation_id)
        except ValueError as exc:
            return Result.fail(str(exc))
        await self._invoices.save(invoice)
        await publish_integration_event(issued_event)

        amount = float(invoice.amount)
        journal_event = JournalPostedIntegration(
            tenant_id=TenantId.create(tenant_id),
            correlation_id=correlation_id,
            journal_id=UniqueId.generate(),
            source_type="ar_invoice",
            source_id=str(invoice.id),
            currency=invoice.currency,
            lines=(
                {
                    "account_code": "1200",
                    "account_name": "Accounts Receivable",
                    "debit": amount,
                    "credit": 0.0,
                },
                {
                    "account_code": "4100",
                    "account_name": "Sales Revenue",
                    "debit": 0.0,
                    "credit": amount,
                },
            ),
        )
        await publish_integration_event(journal_event)
        await self._audit.log(
            tenant_id=tenant_id,
            correlation_id=correlation_id,
            action="accounting.invoice.issued",
            resource_type="invoice",
            resource_id=str(invoice.id),
            payload={"sales_order_id": str(invoice.sales_order_id), "amount": str(invoice.amount)},
        )
        return Result.ok(invoice.to_dict())

    async def receive_payment(
        self, *, tenant_id: str, invoice_id: str, correlation_id: str
    ) -> Result[dict]:
        if self._invoices is None:
            return Result.fail("accounting.errors.invoices_unavailable")
        invoice = await self._invoices.find_by_id(tenant_id, UniqueId.from_string(invoice_id))
        if not invoice:
            return Result.fail("accounting.errors.invoice_not_found")
        try:
            payment_event = invoice.receive_payment(correlation_id=correlation_id)
        except ValueError as exc:
            return Result.fail(str(exc))
        await self._invoices.save(invoice)
        await publish_integration_event(payment_event)

        amount = float(invoice.amount)
        journal_event = JournalPostedIntegration(
            tenant_id=TenantId.create(tenant_id),
            correlation_id=correlation_id,
            journal_id=UniqueId.generate(),
            source_type="ar_payment",
            source_id=str(invoice.id),
            currency=invoice.currency,
            lines=(
                {
                    "account_code": "1000",
                    "account_name": "Cash",
                    "debit": amount,
                    "credit": 0.0,
                },
                {
                    "account_code": "1200",
                    "account_name": "Accounts Receivable",
                    "debit": 0.0,
                    "credit": amount,
                },
            ),
        )
        await publish_integration_event(journal_event)
        await self._audit.log(
            tenant_id=tenant_id,
            correlation_id=correlation_id,
            action="accounting.payment.received",
            resource_type="invoice",
            resource_id=str(invoice.id),
            payload={
                "sales_order_id": str(invoice.sales_order_id),
                "amount": str(invoice.amount),
                "currency": invoice.currency,
            },
        )
        return Result.ok(invoice.to_dict())

    async def list_invoices(
        self, tenant_id: str, *, limit: int = 50, offset: int = 0
    ) -> Result[dict]:
        if self._invoices is None:
            return Result.fail("accounting.errors.invoices_unavailable")
        limit = max(1, min(limit, 100))
        offset = max(0, offset)
        items = await self._invoices.list_invoices(tenant_id)
        page = items[offset : offset + limit]
        return Result.ok(
            {
                "items": [i.to_dict() for i in page],
                "total": len(items),
                "limit": limit,
                "offset": offset,
            }
        )

    async def get_invoice(self, tenant_id: str, invoice_id: str) -> Result[dict]:
        if self._invoices is None:
            return Result.fail("accounting.errors.invoices_unavailable")
        invoice = await self._invoices.find_by_id(tenant_id, UniqueId.from_string(invoice_id))
        if not invoice:
            return Result.fail("accounting.errors.invoice_not_found")
        return Result.ok(invoice.to_dict())

    async def find_invoice_by_order(self, tenant_id: str, order_id: str) -> Result[dict]:
        if self._invoices is None:
            return Result.fail("accounting.errors.invoices_unavailable")
        invoice = await self._invoices.find_by_sales_order(
            tenant_id, UniqueId.from_string(order_id)
        )
        if not invoice:
            return Result.fail("accounting.errors.invoice_not_found")
        return Result.ok(invoice.to_dict())

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
