"""CRM in-memory repositories."""
from __future__ import annotations

from contexts.crm.domain.aggregates.contact import Contact
from contexts.crm.domain.aggregates.opportunity import Opportunity
from contexts.crm.domain.ports.repositories import IContactRepository, IOpportunityRepository
from shared.domain.value_objects.unique_id import UniqueId


class CrmMemoryStore:
    contacts: dict[str, Contact] = {}
    opportunities: dict[str, Opportunity] = {}

    @classmethod
    def reset(cls) -> None:
        cls.contacts.clear()
        cls.opportunities.clear()


class InMemoryContactRepository(IContactRepository):
    async def save(self, contact: Contact) -> None:
        CrmMemoryStore.contacts[str(contact.id)] = contact

    async def find_by_id(self, tenant_id: str, contact_id: UniqueId) -> Contact | None:
        c = CrmMemoryStore.contacts.get(str(contact_id))
        return c if c and c.tenant_id == tenant_id else None

    async def find_by_email(self, tenant_id: str, email: str) -> Contact | None:
        target = email.strip().lower()
        for c in CrmMemoryStore.contacts.values():
            if c.tenant_id == tenant_id and c.email == target:
                return c
        return None

    async def list_contacts(self, tenant_id: str) -> list[Contact]:
        items = [c for c in CrmMemoryStore.contacts.values() if c.tenant_id == tenant_id]
        return sorted(items, key=lambda c: c.created_at, reverse=True)


class InMemoryOpportunityRepository(IOpportunityRepository):
    async def save(self, opportunity: Opportunity) -> None:
        CrmMemoryStore.opportunities[str(opportunity.id)] = opportunity

    async def find_by_id(self, tenant_id: str, opportunity_id: UniqueId) -> Opportunity | None:
        o = CrmMemoryStore.opportunities.get(str(opportunity_id))
        return o if o and o.tenant_id == tenant_id else None

    async def list_opportunities(self, tenant_id: str) -> list[Opportunity]:
        items = [o for o in CrmMemoryStore.opportunities.values() if o.tenant_id == tenant_id]
        return sorted(items, key=lambda o: o.created_at, reverse=True)
