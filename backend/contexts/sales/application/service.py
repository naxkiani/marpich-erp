"""Sales application service — CAP-ENT-002 Sales Lifecycle.

CRM won opportunities → draft quotation (ACL). Audit via integration events.
"""
from __future__ import annotations

from decimal import Decimal, InvalidOperation

from contexts.sales.domain.aggregates.quotation import Quotation
from contexts.sales.domain.aggregates.sales_order import SalesOrder
from contexts.sales.domain.ports.repositories import IQuotationRepository, ISalesOrderRepository
from contexts.sales.infrastructure.acl.event_routes import (
    DraftQuotationFromOpportunityCommand,
    SalesCrmEventAdapter,
)
from shared.application.result import Result
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class SalesApplicationService:
    def __init__(
        self,
        quotations: IQuotationRepository,
        orders: ISalesOrderRepository,
        event_adapter: SalesCrmEventAdapter | None = None,
    ) -> None:
        self._quotations = quotations
        self._orders = orders
        self._event_adapter = event_adapter or SalesCrmEventAdapter()

    async def handle_integration_event(self, envelope: dict) -> None:
        command = await self._event_adapter.parse_integration_event(envelope)
        if command:
            await self.draft_quotation_from_opportunity(command)

    async def draft_quotation_from_opportunity(
        self, command: DraftQuotationFromOpportunityCommand
    ) -> Result[dict]:
        opportunity_id = UniqueId.from_string(command.opportunity_id)
        existing = await self._quotations.find_by_opportunity(command.tenant_id, opportunity_id)
        if existing:
            return Result.ok(existing.to_dict())
        try:
            amount = Decimal(command.amount)
        except (InvalidOperation, ValueError):
            return Result.fail("sales.errors.invalid_amount")
        try:
            quotation = Quotation.draft_from_opportunity(
                tenant_id=command.tenant_id,
                contact_id=UniqueId.from_string(command.contact_id),
                opportunity_id=opportunity_id,
                title=command.title,
                amount=amount,
                currency=command.currency,
            )
        except ValueError as exc:
            return Result.fail(str(exc))
        await self._quotations.save(quotation)
        return Result.ok(quotation.to_dict())

    async def create_quotation(
        self,
        *,
        tenant_id: str,
        contact_id: str,
        title: str,
        amount: str,
        correlation_id: str,
        currency: str = "USD",
        opportunity_id: str | None = None,
    ) -> Result[dict]:
        try:
            money = Decimal(amount)
        except (InvalidOperation, ValueError):
            return Result.fail("sales.errors.invalid_amount")
        try:
            quotation = Quotation.create(
                tenant_id=tenant_id,
                contact_id=UniqueId.from_string(contact_id),
                title=title,
                amount=money,
                currency=currency,
                opportunity_id=UniqueId.from_string(opportunity_id) if opportunity_id else None,
            )
        except ValueError as exc:
            return Result.fail(str(exc))
        await self._quotations.save(quotation)
        return Result.ok(quotation.to_dict())

    async def list_quotations(
        self, tenant_id: str, *, limit: int = 50, offset: int = 0
    ) -> Result[dict]:
        limit = max(1, min(limit, 100))
        offset = max(0, offset)
        items = await self._quotations.list_quotations(tenant_id)
        page = items[offset : offset + limit]
        return Result.ok(
            {
                "items": [q.to_dict() for q in page],
                "total": len(items),
                "limit": limit,
                "offset": offset,
            }
        )

    async def send_quotation(
        self, *, tenant_id: str, quotation_id: str, correlation_id: str
    ) -> Result[dict]:
        quotation = await self._quotations.find_by_id(
            tenant_id, UniqueId.from_string(quotation_id)
        )
        if not quotation:
            return Result.fail("sales.errors.quotation_not_found")
        try:
            event = quotation.send(correlation_id=correlation_id)
        except ValueError as exc:
            return Result.fail(str(exc))
        await self._quotations.save(quotation)
        await publish_integration_event(event)
        return Result.ok(quotation.to_dict())

    async def convert_quotation_to_order(
        self, *, tenant_id: str, quotation_id: str, correlation_id: str
    ) -> Result[dict]:
        quotation = await self._quotations.find_by_id(
            tenant_id, UniqueId.from_string(quotation_id)
        )
        if not quotation:
            return Result.fail("sales.errors.quotation_not_found")
        try:
            quotation.accept()
        except ValueError as exc:
            return Result.fail(str(exc))
        order, event = SalesOrder.from_quotation(
            tenant_id=tenant_id,
            quotation_id=quotation.id,
            contact_id=quotation.contact_id,
            title=quotation.title,
            amount=quotation.amount,
            currency=quotation.currency,
            opportunity_id=quotation.opportunity_id,
            correlation_id=correlation_id,
        )
        quotation.mark_converted()
        await self._orders.save(order)
        await self._quotations.save(quotation)
        await publish_integration_event(event)
        return Result.ok({"order": order.to_dict(), "quotation": quotation.to_dict()})

    async def list_orders(
        self, tenant_id: str, *, limit: int = 50, offset: int = 0
    ) -> Result[dict]:
        limit = max(1, min(limit, 100))
        offset = max(0, offset)
        items = await self._orders.list_orders(tenant_id)
        page = items[offset : offset + limit]
        return Result.ok(
            {
                "items": [o.to_dict() for o in page],
                "total": len(items),
                "limit": limit,
                "offset": offset,
            }
        )
