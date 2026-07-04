"""Repository ports — Organization."""
from __future__ import annotations

from abc import ABC, abstractmethod

from contexts.organization.domain.aggregates.membership import Membership
from contexts.organization.domain.aggregates.org_unit import OrgUnit
from contexts.organization.domain.aggregates.organization import Organization
from shared.domain.value_objects.unique_id import UniqueId


class IOrganizationRepository(ABC):
    @abstractmethod
    async def save(self, org: Organization) -> None: ...

    @abstractmethod
    async def find_by_tenant(self, tenant_id: str) -> Organization | None: ...

    @abstractmethod
    async def exists(self, tenant_id: str) -> bool: ...


class IOrgUnitRepository(ABC):
    @abstractmethod
    async def save(self, unit: OrgUnit) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, unit_id: UniqueId) -> OrgUnit | None: ...

    @abstractmethod
    async def find_by_code(self, tenant_id: str, code: str) -> OrgUnit | None: ...

    @abstractmethod
    async def list_by_org(self, tenant_id: str, organization_id: UniqueId) -> list[OrgUnit]: ...


class IMembershipRepository(ABC):
    @abstractmethod
    async def save(self, membership: Membership) -> None: ...

    @abstractmethod
    async def find(
        self, tenant_id: str, org_unit_id: UniqueId, user_id: str
    ) -> Membership | None: ...

    @abstractmethod
    async def delete(self, tenant_id: str, org_unit_id: UniqueId, user_id: str) -> bool: ...

    @abstractmethod
    async def list_by_user(self, tenant_id: str, user_id: str) -> list[Membership]: ...

    @abstractmethod
    async def list_by_unit(self, tenant_id: str, org_unit_id: UniqueId) -> list[Membership]: ...
