"""CRM repository ports."""
from __future__ import annotations

from abc import ABC, abstractmethod

from contexts.crm.domain.aggregates.contact import Contact
from contexts.crm.domain.aggregates.opportunity import Opportunity
from shared.domain.value_objects.unique_id import UniqueId


class IContactRepository(ABC):
    @abstractmethod
    async def save(self, contact: Contact) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, contact_id: UniqueId) -> Contact | None: ...

    @abstractmethod
    async def find_by_email(self, tenant_id: str, email: str) -> Contact | None: ...

    @abstractmethod
    async def list_contacts(self, tenant_id: str) -> list[Contact]: ...


class IOpportunityRepository(ABC):
    @abstractmethod
    async def save(self, opportunity: Opportunity) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, opportunity_id: UniqueId) -> Opportunity | None: ...

    @abstractmethod
    async def list_opportunities(self, tenant_id: str) -> list[Opportunity]: ...
