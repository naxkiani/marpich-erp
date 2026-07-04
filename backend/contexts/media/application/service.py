"""Media application service."""
from __future__ import annotations

from contexts.media.application.constants.media_extensions import (
    AUDIO_EXTENSIONS,
    IMAGE_EXTENSIONS,
    VIDEO_EXTENSIONS,
)
from contexts.media.application.ports.document_events import IDocumentEventAdapter
from contexts.media.domain.aggregates.media_asset import AssetStatus, MediaAsset, MediaKind
from contexts.media.domain.aggregates.media_variant import MediaVariant
from contexts.media.domain.aggregates.transcode_job import TranscodeJob
from contexts.media.domain.events.integration_events import (
    AssetDeletedIntegration,
    AssetUploadedIntegration,
    TranscodeCompletedIntegration,
)
from contexts.media.domain.ports.repositories import (
    IAssetRepository,
    ITranscodeJobRepository,
    IVariantRepository,
)
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.messaging.event_bus import publish_integration_event


def _infer_kind(file_name: str, content_type: str) -> MediaKind:
    lower = file_name.lower()
    if any(lower.endswith(ext) for ext in VIDEO_EXTENSIONS) or content_type.startswith("video/"):
        return MediaKind.VIDEO
    if any(lower.endswith(ext) for ext in AUDIO_EXTENSIONS) or content_type.startswith("audio/"):
        return MediaKind.AUDIO
    if any(lower.endswith(ext) for ext in IMAGE_EXTENSIONS) or content_type.startswith("image/"):
        return MediaKind.IMAGE
    return MediaKind.DOCUMENT


def _dev_cdn_url(tenant_id: str, asset_id: str, profile: str) -> str:
    return f"https://cdn.marpich.dev/{tenant_id}/{asset_id}/{profile}"


class MediaApplicationService:
    def __init__(
        self,
        assets: IAssetRepository,
        variants: IVariantRepository,
        jobs: ITranscodeJobRepository,
        document_events: IDocumentEventAdapter,
    ) -> None:
        self._assets = assets
        self._variants = variants
        self._jobs = jobs
        self._document_events = document_events

    async def handle_document_uploaded(self, envelope: dict) -> None:
        command = await self._document_events.parse_document_uploaded(envelope)
        if not command:
            return

        asset = MediaAsset.register(
            tenant_id=command.tenant_id,
            file_name=command.file_name,
            content_type="application/octet-stream",
            media_kind=_infer_kind(command.file_name, ""),
            source_ref=f"document:{command.document_id}",
            metadata={"document_id": command.document_id},
        )
        storage_key = f"{command.tenant_id}/{asset.id}/original"
        asset.complete(storage_key)
        await self._assets.save(asset)

        original = MediaVariant.create(
            tenant_id=command.tenant_id,
            asset_id=asset.id,
            profile="original",
            url=_dev_cdn_url(command.tenant_id, str(asset.id), "original"),
        )
        await self._variants.save(original)

        await publish_integration_event(
            AssetUploadedIntegration(
                tenant_id=TenantId.create(command.tenant_id),
                correlation_id=command.correlation_id,
                asset_id=asset.id,
                file_name=asset.file_name,
                media_kind=asset.media_kind.value,
            )
        )

    async def register_upload(
        self,
        *,
        tenant_id: str,
        file_name: str,
        content_type: str,
        metadata: dict | None,
        created_by: str | None,
    ) -> Result[dict]:
        asset = MediaAsset.register(
            tenant_id=tenant_id,
            file_name=file_name,
            content_type=content_type,
            media_kind=_infer_kind(file_name, content_type),
            metadata=metadata,
            created_by=created_by,
        )
        await self._assets.save(asset)
        presigned_url = f"https://upload.marpich.dev/{tenant_id}/{asset.id}?expires=3600"
        return Result.ok(
            {
                "asset": asset.to_dict(),
                "presigned_url": presigned_url,
                "upload_method": "PUT",
            }
        )

    async def complete_upload(
        self, tenant_id: str, correlation_id: str, asset_id: str, checksum: str | None = None
    ) -> Result[dict]:
        asset = await self._assets.find_by_id(tenant_id, UniqueId.from_string(asset_id))
        if not asset:
            return Result.fail("media.errors.asset_not_found")
        if asset.status != AssetStatus.PENDING:
            return Result.ok(asset.to_dict())

        storage_key = f"{tenant_id}/{asset.id}/original"
        asset.complete(storage_key)
        if checksum:
            asset.metadata["checksum"] = checksum
        await self._assets.save(asset)

        original = MediaVariant.create(
            tenant_id=tenant_id,
            asset_id=asset.id,
            profile="original",
            url=_dev_cdn_url(tenant_id, str(asset.id), "original"),
        )
        await self._variants.save(original)

        await publish_integration_event(
            AssetUploadedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                asset_id=asset.id,
                file_name=asset.file_name,
                media_kind=asset.media_kind.value,
            )
        )
        return Result.ok(asset.to_dict())

    async def get_asset(self, tenant_id: str, asset_id: str) -> Result[dict]:
        asset = await self._assets.find_by_id(tenant_id, UniqueId.from_string(asset_id))
        if not asset or asset.status == AssetStatus.DELETED:
            return Result.fail("media.errors.asset_not_found")

        variants = await self._variants.list_by_asset(tenant_id, asset.id)
        return Result.ok({"asset": asset.to_dict(), "variants": [v.to_dict() for v in variants]})

    async def request_transcode(
        self, tenant_id: str, correlation_id: str, asset_id: str, profile: str
    ) -> Result[dict]:
        asset = await self._assets.find_by_id(tenant_id, UniqueId.from_string(asset_id))
        if not asset or asset.status != AssetStatus.READY:
            return Result.fail("media.errors.asset_not_found")

        existing = await self._variants.find_by_profile(tenant_id, asset.id, profile)
        if existing:
            return Result.ok({"job": None, "variant": existing.to_dict()})

        job = TranscodeJob.create(tenant_id=tenant_id, asset_id=asset.id, profile=profile)
        job.complete()
        await self._jobs.save(job)

        variant = MediaVariant.create(
            tenant_id=tenant_id,
            asset_id=asset.id,
            profile=profile,
            url=_dev_cdn_url(tenant_id, str(asset.id), profile),
            width=320 if profile == "thumbnail" else None,
            height=320 if profile == "thumbnail" else None,
        )
        await self._variants.save(variant)

        await publish_integration_event(
            TranscodeCompletedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                asset_id=asset.id,
                job_id=job.id,
                profile=profile,
                variant_url=variant.url,
            )
        )
        return Result.ok({"job": job.to_dict(), "variant": variant.to_dict()})

    async def get_variant(self, tenant_id: str, asset_id: str, profile: str) -> Result[dict]:
        asset = await self._assets.find_by_id(tenant_id, UniqueId.from_string(asset_id))
        if not asset or asset.status == AssetStatus.DELETED:
            return Result.fail("media.errors.asset_not_found")

        variant = await self._variants.find_by_profile(tenant_id, asset.id, profile)
        if not variant:
            return Result.fail("media.errors.variant_not_found")
        return Result.ok(variant.to_dict())

    async def delete_asset(self, tenant_id: str, correlation_id: str, asset_id: str) -> Result[dict]:
        asset = await self._assets.find_by_id(tenant_id, UniqueId.from_string(asset_id))
        if not asset or asset.status == AssetStatus.DELETED:
            return Result.fail("media.errors.asset_not_found")

        asset.soft_delete()
        await self._assets.save(asset)

        await publish_integration_event(
            AssetDeletedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                asset_id=asset.id,
                file_name=asset.file_name,
            )
        )
        return Result.ok(asset.to_dict())
