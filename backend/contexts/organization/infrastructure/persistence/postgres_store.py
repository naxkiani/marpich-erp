"""PostgreSQL repositories — Organization bounded context."""
from __future__ import annotations

from uuid import UUID

from sqlalchemy import delete, func, select

from contexts.organization.domain.aggregates.membership import Membership
from contexts.organization.domain.aggregates.org_unit import OrgUnit, OrgUnitType
from contexts.organization.domain.aggregates.organization import Organization
from contexts.organization.domain.ports.repositories import (
    IMembershipRepository,
    IOrganizationRepository,
    IOrgUnitRepository,
)
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.database.engine import session_scope
from shared.infrastructure.database.orm import MembershipRow, OrganizationRow, OrgUnitRow


class PostgresOrganizationRepository(IOrganizationRepository):
    async def save(self, org: Organization) -> None:
        async with session_scope() as session:
            row = await session.get(OrganizationRow, UUID(str(org.id)))
            if row is None:
                row = OrganizationRow(
                    id=UUID(str(org.id)),
                    tenant_id=org.tenant_id,
                    name=org.name,
                    legal_name=org.legal_name,
                    root_unit_id=UUID(str(org.root_unit_id)) if org.root_unit_id else None,
                    created_at=org.created_at,
                )
                session.add(row)
            else:
                row.name = org.name
                row.legal_name = org.legal_name
                row.root_unit_id = UUID(str(org.root_unit_id)) if org.root_unit_id else None

    async def find_by_tenant(self, tenant_id: str) -> Organization | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(OrganizationRow).where(OrganizationRow.tenant_id == tenant_id)
            )
            return _organization_from_row(row) if row else None

    async def exists(self, tenant_id: str) -> bool:
        async with session_scope() as session:
            count = await session.scalar(
                select(func.count()).select_from(OrganizationRow).where(
                    OrganizationRow.tenant_id == tenant_id
                )
            )
            return bool(count)


class PostgresOrgUnitRepository(IOrgUnitRepository):
    async def save(self, unit: OrgUnit) -> None:
        async with session_scope() as session:
            row = await session.get(OrgUnitRow, UUID(str(unit.id)))
            if row is None:
                row = OrgUnitRow(
                    id=UUID(str(unit.id)),
                    tenant_id=unit.tenant_id,
                    organization_id=UUID(str(unit.organization_id)),
                    parent_id=UUID(str(unit.parent_id)) if unit.parent_id else None,
                    unit_type=unit.unit_type.value,
                    code=unit.code,
                    name=unit.name,
                    is_active=unit.is_active,
                    created_at=unit.created_at,
                )
                session.add(row)
            else:
                row.name = unit.name
                row.is_active = unit.is_active
                row.parent_id = UUID(str(unit.parent_id)) if unit.parent_id else None

    async def find_by_id(self, tenant_id: str, unit_id: UniqueId) -> OrgUnit | None:
        async with session_scope() as session:
            row = await session.get(OrgUnitRow, UUID(str(unit_id)))
            if row and row.tenant_id == tenant_id:
                return _org_unit_from_row(row)
            return None

    async def find_by_code(self, tenant_id: str, code: str) -> OrgUnit | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(OrgUnitRow).where(
                    OrgUnitRow.tenant_id == tenant_id,
                    OrgUnitRow.code == code.upper(),
                )
            )
            return _org_unit_from_row(row) if row else None

    async def list_by_org(self, tenant_id: str, organization_id: UniqueId) -> list[OrgUnit]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(OrgUnitRow).where(
                        OrgUnitRow.tenant_id == tenant_id,
                        OrgUnitRow.organization_id == UUID(str(organization_id)),
                    )
                )
            ).all()
        return [_org_unit_from_row(r) for r in rows]


class PostgresMembershipRepository(IMembershipRepository):
    async def save(self, membership: Membership) -> None:
        async with session_scope() as session:
            row = await session.get(MembershipRow, UUID(str(membership.id)))
            if row is None:
                row = MembershipRow(
                    id=UUID(str(membership.id)),
                    tenant_id=membership.tenant_id,
                    org_unit_id=UUID(str(membership.org_unit_id)),
                    user_id=membership.user_id,
                    title=membership.title,
                    is_primary=membership.is_primary,
                    created_at=membership.created_at,
                )
                session.add(row)
            else:
                row.title = membership.title
                row.is_primary = membership.is_primary

    async def find(self, tenant_id: str, org_unit_id: UniqueId, user_id: str) -> Membership | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(MembershipRow).where(
                    MembershipRow.tenant_id == tenant_id,
                    MembershipRow.org_unit_id == UUID(str(org_unit_id)),
                    MembershipRow.user_id == user_id,
                )
            )
            return _membership_from_row(row) if row else None

    async def delete(self, tenant_id: str, org_unit_id: UniqueId, user_id: str) -> bool:
        async with session_scope() as session:
            result = await session.execute(
                delete(MembershipRow).where(
                    MembershipRow.tenant_id == tenant_id,
                    MembershipRow.org_unit_id == UUID(str(org_unit_id)),
                    MembershipRow.user_id == user_id,
                )
            )
            return result.rowcount > 0

    async def list_by_user(self, tenant_id: str, user_id: str) -> list[Membership]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(MembershipRow).where(
                        MembershipRow.tenant_id == tenant_id,
                        MembershipRow.user_id == user_id,
                    )
                )
            ).all()
        return [_membership_from_row(r) for r in rows]

    async def list_by_unit(self, tenant_id: str, org_unit_id: UniqueId) -> list[Membership]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(MembershipRow).where(
                        MembershipRow.tenant_id == tenant_id,
                        MembershipRow.org_unit_id == UUID(str(org_unit_id)),
                    )
                )
            ).all()
        return [_membership_from_row(r) for r in rows]


def _organization_from_row(row: OrganizationRow) -> Organization:
    return Organization(
        id=UniqueId(str(row.id)),
        tenant_id=row.tenant_id,
        name=row.name,
        legal_name=row.legal_name,
        root_unit_id=UniqueId(str(row.root_unit_id)) if row.root_unit_id else None,
        created_at=row.created_at,
    )


def _org_unit_from_row(row: OrgUnitRow) -> OrgUnit:
    return OrgUnit(
        id=UniqueId(str(row.id)),
        tenant_id=row.tenant_id,
        organization_id=UniqueId(str(row.organization_id)),
        parent_id=UniqueId(str(row.parent_id)) if row.parent_id else None,
        unit_type=OrgUnitType(row.unit_type),
        code=row.code,
        name=row.name,
        is_active=row.is_active,
        created_at=row.created_at,
    )


def _membership_from_row(row: MembershipRow) -> Membership:
    return Membership(
        id=UniqueId(str(row.id)),
        tenant_id=row.tenant_id,
        org_unit_id=UniqueId(str(row.org_unit_id)),
        user_id=row.user_id,
        title=row.title,
        is_primary=row.is_primary,
        created_at=row.created_at,
    )
