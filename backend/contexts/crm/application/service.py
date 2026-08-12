"""CRM application service — CAP-ENT-001 Customer Management.

Audit via integration events → Audit Platform (no local audit tables).
"""
from __future__ import annotations

from decimal import Decimal, InvalidOperation

from contexts.crm.domain.aggregates.contact import Contact
from contexts.crm.domain.aggregates.opportunity import Opportunity
from contexts.crm.domain.events.integration_events import ContactCreatedIntegration
from contexts.crm.domain.ports.repositories import IContactRepository, IOpportunityRepository
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class CrmApplicationService:
    def __init__(
        self,
        contacts: IContactRepository,
        opportunities: IOpportunityRepository,
    ) -> None:
        self._contacts = contacts
        self._opportunities = opportunities

    async def create_contact(
        self,
        *,
        tenant_id: str,
        email: str,
        full_name: str,
        correlation_id: str,
        company: str | None = None,
        phone: str | None = None,
    ) -> Result[dict]:
        if await self._contacts.find_by_email(tenant_id, email):
            return Result.fail("crm.errors.contact_email_exists")
        contact = Contact.create(
            tenant_id=tenant_id,
            email=email,
            full_name=full_name,
            company=company,
            phone=phone,
        )
        await self._contacts.save(contact)
        await publish_integration_event(
            ContactCreatedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                contact_id=contact.id,
                email=contact.email,
                full_name=contact.full_name,
            )
        )
        return Result.ok(contact.to_dict())

    async def list_contacts(
        self, tenant_id: str, *, limit: int = 50, offset: int = 0
    ) -> Result[dict]:
        limit = max(1, min(limit, 100))
        offset = max(0, offset)
        items = await self._contacts.list_contacts(tenant_id)
        page = items[offset : offset + limit]
        return Result.ok(
            {
                "items": [c.to_dict() for c in page],
                "total": len(items),
                "limit": limit,
                "offset": offset,
            }
        )

    async def create_opportunity(
        self,
        *,
        tenant_id: str,
        contact_id: str,
        title: str,
        amount: str,
        correlation_id: str,
        currency: str = "USD",
    ) -> Result[dict]:
        contact = await self._contacts.find_by_id(tenant_id, UniqueId.from_string(contact_id))
        if not contact:
            return Result.fail("crm.errors.contact_not_found")
        try:
            money = Decimal(amount)
        except (InvalidOperation, ValueError):
            return Result.fail("crm.errors.invalid_amount")
        try:
            opportunity = Opportunity.open(
                tenant_id=tenant_id,
                contact_id=contact.id,
                title=title,
                amount=money,
                currency=currency,
            )
        except ValueError as exc:
            return Result.fail(str(exc))
        await self._opportunities.save(opportunity)
        return Result.ok(opportunity.to_dict())

    async def list_opportunities(
        self, tenant_id: str, *, limit: int = 50, offset: int = 0
    ) -> Result[dict]:
        limit = max(1, min(limit, 100))
        offset = max(0, offset)
        items = await self._opportunities.list_opportunities(tenant_id)
        page = items[offset : offset + limit]
        return Result.ok(
            {
                "items": [o.to_dict() for o in page],
                "total": len(items),
                "limit": limit,
                "offset": offset,
            }
        )

    async def win_opportunity(
        self, *, tenant_id: str, opportunity_id: str, correlation_id: str
    ) -> Result[dict]:
        opportunity = await self._opportunities.find_by_id(
            tenant_id, UniqueId.from_string(opportunity_id)
        )
        if not opportunity:
            return Result.fail("crm.errors.opportunity_not_found")
        try:
            event = opportunity.win(correlation_id=correlation_id)
        except ValueError as exc:
            return Result.fail(str(exc))
        await self._opportunities.save(opportunity)
        await publish_integration_event(event)
        return Result.ok(opportunity.to_dict())

    async def lose_opportunity(
        self,
        *,
        tenant_id: str,
        opportunity_id: str,
        correlation_id: str,
        reason: str | None = None,
    ) -> Result[dict]:
        opportunity = await self._opportunities.find_by_id(
            tenant_id, UniqueId.from_string(opportunity_id)
        )
        if not opportunity:
            return Result.fail("crm.errors.opportunity_not_found")
        try:
            event = opportunity.lose(correlation_id=correlation_id, reason=reason)
        except ValueError as exc:
            return Result.fail(str(exc))
        await self._opportunities.save(opportunity)
        await publish_integration_event(event)
        return Result.ok(opportunity.to_dict())
