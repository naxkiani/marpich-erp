"""PostgreSQL repositories — Localization bounded context."""
from __future__ import annotations

from uuid import UUID

from sqlalchemy import select

from contexts.localization.domain.aggregates.locale import Locale, TextDirection
from contexts.localization.domain.aggregates.translation_bundle import TranslationBundle
from contexts.localization.domain.aggregates.translation_key import TranslationKey
from contexts.localization.domain.ports.repositories import (
    ILocaleRepository,
    ITranslationBundleRepository,
    ITranslationKeyRepository,
)
from shared.infrastructure.database.engine import session_scope
from shared.infrastructure.database.orm import (
    LocalizationBundleRow,
    LocalizationKeyRow,
    LocalizationLocaleRow,
)


class PostgresLocaleRepository(ILocaleRepository):
    async def save(self, locale: Locale) -> None:
        async with session_scope() as session:
            row = await session.scalar(
                select(LocalizationLocaleRow).where(
                    LocalizationLocaleRow.tenant_id == locale.tenant_id,
                    LocalizationLocaleRow.code == locale.code,
                )
            )
            if row is None:
                session.add(
                    LocalizationLocaleRow(
                        id=UUID(str(locale.id)),
                        tenant_id=locale.tenant_id,
                        code=locale.code,
                        name=locale.name,
                        direction=locale.direction.value,
                        is_default=locale.is_default,
                    )
                )

    async def find_by_code(self, tenant_id: str, code: str) -> Locale | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(LocalizationLocaleRow).where(
                    LocalizationLocaleRow.tenant_id == tenant_id,
                    LocalizationLocaleRow.code == code.lower(),
                )
            )
            return _locale_from_row(row) if row else None

    async def list_locales(self, tenant_id: str) -> list[Locale]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(LocalizationLocaleRow).where(LocalizationLocaleRow.tenant_id == tenant_id)
                )
            ).all()
        return [_locale_from_row(r) for r in rows]

    async def exists(self, tenant_id: str) -> bool:
        async with session_scope() as session:
            row = await session.scalar(
                select(LocalizationLocaleRow.id).where(LocalizationLocaleRow.tenant_id == tenant_id).limit(1)
            )
            return row is not None


class PostgresTranslationKeyRepository(ITranslationKeyRepository):
    async def save(self, translation_key: TranslationKey) -> None:
        async with session_scope() as session:
            row = await session.scalar(
                select(LocalizationKeyRow).where(
                    LocalizationKeyRow.tenant_id == translation_key.tenant_id,
                    LocalizationKeyRow.namespace == translation_key.namespace,
                    LocalizationKeyRow.key == translation_key.key,
                )
            )
            if row is None:
                session.add(
                    LocalizationKeyRow(
                        id=UUID(str(translation_key.id)),
                        tenant_id=translation_key.tenant_id,
                        namespace=translation_key.namespace,
                        key=translation_key.key,
                        default_value=translation_key.default_value,
                        description=translation_key.description,
                    )
                )
            else:
                row.default_value = translation_key.default_value
                row.description = translation_key.description

    async def find(self, tenant_id: str, namespace: str, key: str) -> TranslationKey | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(LocalizationKeyRow).where(
                    LocalizationKeyRow.tenant_id == tenant_id,
                    LocalizationKeyRow.namespace == namespace,
                    LocalizationKeyRow.key == key,
                )
            )
            return _key_from_row(row) if row else None

    async def list_keys(self, tenant_id: str, namespace: str | None = None) -> list[TranslationKey]:
        async with session_scope() as session:
            stmt = select(LocalizationKeyRow).where(LocalizationKeyRow.tenant_id == tenant_id)
            if namespace:
                stmt = stmt.where(LocalizationKeyRow.namespace == namespace)
            rows = (await session.scalars(stmt)).all()
        return [_key_from_row(r) for r in rows]


class PostgresTranslationBundleRepository(ITranslationBundleRepository):
    async def save(self, bundle: TranslationBundle) -> None:
        async with session_scope() as session:
            row = await session.scalar(
                select(LocalizationBundleRow).where(
                    LocalizationBundleRow.tenant_id == bundle.tenant_id,
                    LocalizationBundleRow.locale_code == bundle.locale_code,
                    LocalizationBundleRow.namespace == bundle.namespace,
                )
            )
            if row is None:
                session.add(
                    LocalizationBundleRow(
                        id=UUID(str(bundle.id)),
                        tenant_id=bundle.tenant_id,
                        locale_code=bundle.locale_code,
                        namespace=bundle.namespace,
                        entries=bundle.entries,
                    )
                )
            else:
                row.entries = bundle.entries

    async def find(self, tenant_id: str, locale_code: str, namespace: str) -> TranslationBundle | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(LocalizationBundleRow).where(
                    LocalizationBundleRow.tenant_id == tenant_id,
                    LocalizationBundleRow.locale_code == locale_code.lower(),
                    LocalizationBundleRow.namespace == namespace,
                )
            )
            return _bundle_from_row(row) if row else None

    async def list_for_locale(self, tenant_id: str, locale_code: str) -> list[TranslationBundle]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(LocalizationBundleRow).where(
                        LocalizationBundleRow.tenant_id == tenant_id,
                        LocalizationBundleRow.locale_code == locale_code.lower(),
                    )
                )
            ).all()
        return [_bundle_from_row(r) for r in rows]


def _locale_from_row(row: LocalizationLocaleRow) -> Locale:
    from shared.domain.value_objects.unique_id import UniqueId

    return Locale(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        code=row.code,
        name=row.name,
        direction=TextDirection(row.direction),
        is_default=row.is_default,
        created_at=row.created_at,
    )


def _key_from_row(row: LocalizationKeyRow) -> TranslationKey:
    from shared.domain.value_objects.unique_id import UniqueId

    return TranslationKey(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        namespace=row.namespace,
        key=row.key,
        default_value=row.default_value,
        description=row.description or "",
        updated_at=row.updated_at,
    )


def _bundle_from_row(row: LocalizationBundleRow) -> TranslationBundle:
    from shared.domain.value_objects.unique_id import UniqueId

    return TranslationBundle(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        locale_code=row.locale_code,
        namespace=row.namespace,
        entries=dict(row.entries or {}),
        updated_at=row.updated_at,
    )
