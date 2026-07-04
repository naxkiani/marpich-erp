"""PostgreSQL repositories — Media bounded context."""
from __future__ import annotations

from uuid import UUID

from sqlalchemy import select

from contexts.media.domain.aggregates.media_asset import AssetStatus, MediaAsset, MediaKind
from contexts.media.domain.aggregates.media_variant import MediaVariant
from contexts.media.domain.aggregates.transcode_job import TranscodeJob, TranscodeStatus
from contexts.media.domain.ports.repositories import (
    IAssetRepository,
    ITranscodeJobRepository,
    IVariantRepository,
)
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.database.engine import session_scope
from shared.infrastructure.database.orm import MediaAssetRow, MediaVariantRow, TranscodeJobRow


class PostgresAssetRepository(IAssetRepository):
    async def save(self, asset: MediaAsset) -> None:
        async with session_scope() as session:
            row = await session.get(MediaAssetRow, UUID(str(asset.id)))
            if row is None:
                session.add(
                    MediaAssetRow(
                        id=UUID(str(asset.id)),
                        tenant_id=asset.tenant_id,
                        file_name=asset.file_name,
                        content_type=asset.content_type,
                        media_kind=asset.media_kind.value,
                        status=asset.status.value,
                        storage_key=asset.storage_key,
                        source_ref=asset.source_ref,
                        asset_metadata=asset.metadata,
                        created_by=asset.created_by,
                        created_at=asset.created_at,
                    )
                )
            else:
                row.status = asset.status.value
                row.storage_key = asset.storage_key
                row.asset_metadata = asset.metadata

    async def find_by_id(self, tenant_id: str, asset_id: UniqueId) -> MediaAsset | None:
        async with session_scope() as session:
            row = await session.get(MediaAssetRow, UUID(str(asset_id)))
            if row and row.tenant_id == tenant_id:
                return _asset_from_row(row)
            return None


class PostgresVariantRepository(IVariantRepository):
    async def save(self, variant: MediaVariant) -> None:
        async with session_scope() as session:
            row = await session.scalar(
                select(MediaVariantRow).where(
                    MediaVariantRow.asset_id == UUID(str(variant.asset_id)),
                    MediaVariantRow.profile == variant.profile,
                )
            )
            if row is None:
                session.add(
                    MediaVariantRow(
                        id=UUID(str(variant.id)),
                        tenant_id=variant.tenant_id,
                        asset_id=UUID(str(variant.asset_id)),
                        profile=variant.profile,
                        url=variant.url,
                        width=variant.width,
                        height=variant.height,
                        created_at=variant.created_at,
                    )
                )
            else:
                row.url = variant.url
                row.width = variant.width
                row.height = variant.height

    async def find_by_profile(
        self, tenant_id: str, asset_id: UniqueId, profile: str
    ) -> MediaVariant | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(MediaVariantRow).where(
                    MediaVariantRow.tenant_id == tenant_id,
                    MediaVariantRow.asset_id == UUID(str(asset_id)),
                    MediaVariantRow.profile == profile.lower(),
                )
            )
            return _variant_from_row(row) if row else None

    async def list_by_asset(self, tenant_id: str, asset_id: UniqueId) -> list[MediaVariant]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(MediaVariantRow).where(
                        MediaVariantRow.tenant_id == tenant_id,
                        MediaVariantRow.asset_id == UUID(str(asset_id)),
                    )
                )
            ).all()
        return [_variant_from_row(r) for r in rows]


class PostgresTranscodeJobRepository(ITranscodeJobRepository):
    async def save(self, job: TranscodeJob) -> None:
        async with session_scope() as session:
            row = await session.get(TranscodeJobRow, UUID(str(job.id)))
            if row is None:
                session.add(
                    TranscodeJobRow(
                        id=UUID(str(job.id)),
                        tenant_id=job.tenant_id,
                        asset_id=UUID(str(job.asset_id)),
                        profile=job.profile,
                        status=job.status.value,
                        error=job.error,
                        created_at=job.created_at,
                        completed_at=job.completed_at,
                    )
                )
            else:
                row.status = job.status.value
                row.error = job.error
                row.completed_at = job.completed_at

    async def find_by_id(self, tenant_id: str, job_id: UniqueId) -> TranscodeJob | None:
        async with session_scope() as session:
            row = await session.get(TranscodeJobRow, UUID(str(job_id)))
            if row and row.tenant_id == tenant_id:
                return _job_from_row(row)
            return None


def _asset_from_row(row: MediaAssetRow) -> MediaAsset:
    return MediaAsset(
        id=UniqueId(str(row.id)),
        tenant_id=row.tenant_id,
        file_name=row.file_name,
        content_type=row.content_type,
        media_kind=MediaKind(row.media_kind),
        status=AssetStatus(row.status),
        storage_key=row.storage_key,
        source_ref=row.source_ref,
        metadata=row.asset_metadata,
        created_by=row.created_by,
        created_at=row.created_at,
    )


def _variant_from_row(row: MediaVariantRow) -> MediaVariant:
    return MediaVariant(
        id=UniqueId(str(row.id)),
        tenant_id=row.tenant_id,
        asset_id=UniqueId(str(row.asset_id)),
        profile=row.profile,
        url=row.url,
        width=row.width,
        height=row.height,
        created_at=row.created_at,
    )


def _job_from_row(row: TranscodeJobRow) -> TranscodeJob:
    return TranscodeJob(
        id=UniqueId(str(row.id)),
        tenant_id=row.tenant_id,
        asset_id=UniqueId(str(row.asset_id)),
        profile=row.profile,
        status=TranscodeStatus(row.status),
        error=row.error,
        created_at=row.created_at,
        completed_at=row.completed_at,
    )
