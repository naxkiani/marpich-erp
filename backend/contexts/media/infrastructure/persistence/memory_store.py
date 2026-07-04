"""In-memory media repositories."""
from __future__ import annotations

from contexts.media.domain.aggregates.media_asset import MediaAsset
from contexts.media.domain.aggregates.media_variant import MediaVariant
from contexts.media.domain.aggregates.transcode_job import TranscodeJob
from contexts.media.domain.ports.repositories import (
    IAssetRepository,
    ITranscodeJobRepository,
    IVariantRepository,
)
from shared.domain.value_objects.unique_id import UniqueId


class MediaMemoryStore:
    assets: dict[str, MediaAsset] = {}
    variants: dict[str, MediaVariant] = {}
    jobs: dict[str, TranscodeJob] = {}

    @classmethod
    def reset(cls) -> None:
        cls.assets.clear()
        cls.variants.clear()
        cls.jobs.clear()


class InMemoryAssetRepository(IAssetRepository):
    async def save(self, asset: MediaAsset) -> None:
        MediaMemoryStore.assets[str(asset.id)] = asset

    async def find_by_id(self, tenant_id: str, asset_id: UniqueId) -> MediaAsset | None:
        asset = MediaMemoryStore.assets.get(str(asset_id))
        return asset if asset and asset.tenant_id == tenant_id else None


class InMemoryVariantRepository(IVariantRepository):
    async def save(self, variant: MediaVariant) -> None:
        MediaMemoryStore.variants[str(variant.id)] = variant

    async def find_by_profile(
        self, tenant_id: str, asset_id: UniqueId, profile: str
    ) -> MediaVariant | None:
        for variant in MediaMemoryStore.variants.values():
            if (
                variant.tenant_id == tenant_id
                and str(variant.asset_id) == str(asset_id)
                and variant.profile == profile.lower()
            ):
                return variant
        return None

    async def list_by_asset(self, tenant_id: str, asset_id: UniqueId) -> list[MediaVariant]:
        return [
            v
            for v in MediaMemoryStore.variants.values()
            if v.tenant_id == tenant_id and str(v.asset_id) == str(asset_id)
        ]


class InMemoryTranscodeJobRepository(ITranscodeJobRepository):
    async def save(self, job: TranscodeJob) -> None:
        MediaMemoryStore.jobs[str(job.id)] = job

    async def find_by_id(self, tenant_id: str, job_id: UniqueId) -> TranscodeJob | None:
        job = MediaMemoryStore.jobs.get(str(job_id))
        return job if job and job.tenant_id == tenant_id else None
