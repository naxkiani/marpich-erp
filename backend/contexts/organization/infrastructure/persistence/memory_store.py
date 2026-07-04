"""In-memory organization repositories."""
from __future__ import annotations

from contexts.organization.domain.aggregates.membership import Membership
from contexts.organization.domain.aggregates.org_unit import OrgUnit
from contexts.organization.domain.aggregates.organization import Organization
from contexts.organization.domain.ports.repositories import (
    IMembershipRepository,
    IOrganizationRepository,
    IOrgUnitRepository,
)
from shared.domain.value_objects.unique_id import UniqueId


class OrganizationMemoryStore:
    orgs: dict[str, Organization] = {}
    units: dict[str, OrgUnit] = {}
    memberships: dict[str, Membership] = {}

    @classmethod
    def reset(cls) -> None:
        cls.orgs.clear()
        cls.units.clear()
        cls.memberships.clear()


class InMemoryOrganizationRepository(IOrganizationRepository):
    async def save(self, org: Organization) -> None:
        OrganizationMemoryStore.orgs[org.tenant_id] = org

    async def find_by_tenant(self, tenant_id: str) -> Organization | None:
        return OrganizationMemoryStore.orgs.get(tenant_id)

    async def exists(self, tenant_id: str) -> bool:
        return tenant_id in OrganizationMemoryStore.orgs


class InMemoryOrgUnitRepository(IOrgUnitRepository):
    async def save(self, unit: OrgUnit) -> None:
        OrganizationMemoryStore.units[str(unit.id)] = unit

    async def find_by_id(self, tenant_id: str, unit_id: UniqueId) -> OrgUnit | None:
        unit = OrganizationMemoryStore.units.get(str(unit_id))
        return unit if unit and unit.tenant_id == tenant_id else None

    async def find_by_code(self, tenant_id: str, code: str) -> OrgUnit | None:
        for unit in OrganizationMemoryStore.units.values():
            if unit.tenant_id == tenant_id and unit.code == code.upper():
                return unit
        return None

    async def list_by_org(self, tenant_id: str, organization_id: UniqueId) -> list[OrgUnit]:
        return [
            u
            for u in OrganizationMemoryStore.units.values()
            if u.tenant_id == tenant_id and str(u.organization_id) == str(organization_id)
        ]


class InMemoryMembershipRepository(IMembershipRepository):
    def _key(self, tenant_id: str, org_unit_id: str, user_id: str) -> str:
        return f"{tenant_id}:{org_unit_id}:{user_id}"

    async def save(self, membership: Membership) -> None:
        key = self._key(membership.tenant_id, str(membership.org_unit_id), membership.user_id)
        OrganizationMemoryStore.memberships[key] = membership

    async def find(self, tenant_id: str, org_unit_id: UniqueId, user_id: str) -> Membership | None:
        return OrganizationMemoryStore.memberships.get(
            self._key(tenant_id, str(org_unit_id), user_id)
        )

    async def delete(self, tenant_id: str, org_unit_id: UniqueId, user_id: str) -> bool:
        key = self._key(tenant_id, str(org_unit_id), user_id)
        if key in OrganizationMemoryStore.memberships:
            del OrganizationMemoryStore.memberships[key]
            return True
        return False

    async def list_by_user(self, tenant_id: str, user_id: str) -> list[Membership]:
        return [
            m
            for m in OrganizationMemoryStore.memberships.values()
            if m.tenant_id == tenant_id and m.user_id == user_id
        ]

    async def list_by_unit(self, tenant_id: str, org_unit_id: UniqueId) -> list[Membership]:
        return [
            m
            for m in OrganizationMemoryStore.memberships.values()
            if m.tenant_id == tenant_id and str(m.org_unit_id) == str(org_unit_id)
        ]
