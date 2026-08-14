"""PostgreSQL repositories — CRM bounded context."""
from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from sqlalchemy import select

from contexts.crm.domain.aggregates.contact import Contact
from contexts.crm.domain.aggregates.opportunity import Opportunity, OpportunityStage
from contexts.crm.domain.ports.repositories import IContactRepository, IOpportunityRepository
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.database.engine import session_scope
from shared.infrastructure.database.orm import CrmContactRow, CrmOpportunityRow


class PostgresContactRepository(IContactRepository):
    async def save(self, contact: Contact) -> None:
        async with session_scope(tenant_id=contact.tenant_id) as session:
            row = await session.get(CrmContactRow, UUID(str(contact.id)))
            if row is None:
                row = CrmContactRow(
                    id=UUID(str(contact.id)),
                    tenant_id=contact.tenant_id,
                    email=contact.email,
                    full_name=contact.full_name,
                    company=contact.company,
                    phone=contact.phone,
                    status=contact.status,
                )
                session.add(row)
            else:
                row.email = contact.email
                row.full_name = contact.full_name
                row.company = contact.company
                row.phone = contact.phone
                row.status = contact.status
                row.updated_at = contact.updated_at

    async def find_by_id(self, tenant_id: str, contact_id: UniqueId) -> Contact | None:
        async with session_scope(tenant_id=tenant_id) as session:
            row = await session.get(CrmContactRow, UUID(str(contact_id)))
            return _contact_from_row(row) if row and row.tenant_id == tenant_id else None

    async def find_by_email(self, tenant_id: str, email: str) -> Contact | None:
        async with session_scope(tenant_id=tenant_id) as session:
            row = await session.scalar(
                select(CrmContactRow).where(
                    CrmContactRow.tenant_id == tenant_id,
                    CrmContactRow.email == email.strip().lower(),
                )
            )
            return _contact_from_row(row) if row else None

    async def list_contacts(self, tenant_id: str) -> list[Contact]:
        async with session_scope(tenant_id=tenant_id) as session:
            rows = (
                await session.scalars(select(CrmContactRow).where(CrmContactRow.tenant_id == tenant_id))
            ).all()
        return [_contact_from_row(r) for r in rows]


class PostgresOpportunityRepository(IOpportunityRepository):
    async def save(self, opportunity: Opportunity) -> None:
        async with session_scope(tenant_id=opportunity.tenant_id) as session:
            row = await session.get(CrmOpportunityRow, UUID(str(opportunity.id)))
            if row is None:
                row = CrmOpportunityRow(
                    id=UUID(str(opportunity.id)),
                    tenant_id=opportunity.tenant_id,
                    contact_id=UUID(str(opportunity.contact_id)),
                    title=opportunity.title,
                    amount=opportunity.amount,
                    currency=opportunity.currency,
                    stage=opportunity.stage.value,
                    closed_at=opportunity.closed_at,
                )
                session.add(row)
            else:
                row.title = opportunity.title
                row.amount = opportunity.amount
                row.currency = opportunity.currency
                row.stage = opportunity.stage.value
                row.closed_at = opportunity.closed_at
                row.updated_at = opportunity.updated_at

    async def find_by_id(self, tenant_id: str, opportunity_id: UniqueId) -> Opportunity | None:
        async with session_scope(tenant_id=tenant_id) as session:
            row = await session.get(CrmOpportunityRow, UUID(str(opportunity_id)))
            return _opportunity_from_row(row) if row and row.tenant_id == tenant_id else None

    async def list_opportunities(self, tenant_id: str) -> list[Opportunity]:
        async with session_scope(tenant_id=tenant_id) as session:
            rows = (
                await session.scalars(
                    select(CrmOpportunityRow).where(CrmOpportunityRow.tenant_id == tenant_id)
                )
            ).all()
        return [_opportunity_from_row(r) for r in rows]


def _contact_from_row(row: CrmContactRow) -> Contact:
    return Contact(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        email=row.email,
        full_name=row.full_name,
        company=row.company,
        phone=row.phone,
        status=row.status,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def _opportunity_from_row(row: CrmOpportunityRow) -> Opportunity:
    return Opportunity(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        contact_id=UniqueId.from_string(str(row.contact_id)),
        title=row.title,
        amount=Decimal(str(row.amount)),
        currency=row.currency,
        stage=OpportunityStage(row.stage),
        created_at=row.created_at,
        updated_at=row.updated_at,
        closed_at=row.closed_at,
    )
