"""PostgreSQL repository — Settings bounded context."""
from __future__ import annotations

from uuid import UUID

from sqlalchemy import func, select

from contexts.settings.domain.aggregates.tenant_settings import TenantSettings
from contexts.settings.domain.ports.repositories import ITenantSettingsRepository
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.database.engine import session_scope
from shared.infrastructure.database.orm import TenantSettingsRow


class PostgresTenantSettingsRepository(ITenantSettingsRepository):
    async def save(self, settings: TenantSettings) -> None:
        async with session_scope() as session:
            row = await session.scalar(
                select(TenantSettingsRow).where(TenantSettingsRow.tenant_id == settings.tenant_id)
            )
            if row is None:
                session.add(
                    TenantSettingsRow(
                        id=UUID(str(settings.id)),
                        tenant_id=settings.tenant_id,
                        industry_pack=settings.industry_pack,
                        config=settings.config,
                        features=settings.features,
                        branding=settings.branding,
                        created_at=settings.created_at,
                        updated_at=settings.updated_at,
                    )
                )
            else:
                row.industry_pack = settings.industry_pack
                row.config = settings.config
                row.features = settings.features
                row.branding = settings.branding
                row.updated_at = settings.updated_at

    async def find_by_tenant(self, tenant_id: str) -> TenantSettings | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(TenantSettingsRow).where(TenantSettingsRow.tenant_id == tenant_id)
            )
            return _settings_from_row(row) if row else None

    async def exists(self, tenant_id: str) -> bool:
        async with session_scope() as session:
            count = await session.scalar(
                select(func.count())
                .select_from(TenantSettingsRow)
                .where(TenantSettingsRow.tenant_id == tenant_id)
            )
            return bool(count)


def _settings_from_row(row: TenantSettingsRow) -> TenantSettings:
    return TenantSettings(
        id=UniqueId(str(row.id)),
        tenant_id=row.tenant_id,
        industry_pack=row.industry_pack,
        config=row.config,
        features=row.features,
        branding=row.branding,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )
