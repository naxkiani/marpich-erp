"""PostgreSQL tenant repository — Core Platform."""
from __future__ import annotations

from uuid import UUID

from sqlalchemy import select

from contexts.core_platform.domain.aggregates.tenant import Tenant, TenantStatus, TenantTier
from contexts.core_platform.domain.ports.repositories import ITenantRepository
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.database.engine import session_scope
from shared.infrastructure.database.orm import TenantRow


class PostgresTenantRepository(ITenantRepository):
    async def save(self, tenant: Tenant) -> None:
        async with session_scope() as session:
            row = await session.get(TenantRow, UUID(str(tenant.id)))
            if row is None:
                row = TenantRow(
                    id=UUID(str(tenant.id)),
                    slug=tenant.slug,
                    name=tenant.name,
                    industry_pack=tenant.industry_pack,
                )
                session.add(row)
            row.slug = tenant.slug
            row.name = tenant.name
            row.industry_pack = tenant.industry_pack
            row.tier = tenant.tier.value
            row.status = tenant.status.value
            row.enabled_modules = list(tenant.enabled_modules)
            row.locale = tenant.locale
            row.timezone = tenant.timezone
            row.data_region = tenant.data_region
            row.updated_at = tenant.updated_at

    async def find_by_slug(self, slug: str) -> Tenant | None:
        async with session_scope() as session:
            row = await session.scalar(select(TenantRow).where(TenantRow.slug == slug.lower()))
            return _tenant_from_row(row) if row else None

    async def find_by_id(self, tenant_id: UniqueId) -> Tenant | None:
        async with session_scope() as session:
            row = await session.get(TenantRow, UUID(str(tenant_id)))
            return _tenant_from_row(row) if row else None

    async def exists_by_slug(self, slug: str) -> bool:
        tenant = await self.find_by_slug(slug)
        return tenant is not None

    async def list_tenants(self) -> list[Tenant]:
        async with session_scope() as session:
            rows = (await session.scalars(select(TenantRow))).all()
        return [_tenant_from_row(r) for r in rows]


def _tenant_from_row(row: TenantRow) -> Tenant:
    return Tenant(
        id=UniqueId.from_string(str(row.id)),
        slug=row.slug,
        name=row.name,
        industry_pack=row.industry_pack,
        tier=TenantTier(row.tier),
        status=TenantStatus(row.status),
        enabled_modules=list(row.enabled_modules or []),
        locale=row.locale,
        timezone=row.timezone,
        data_region=row.data_region,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )
