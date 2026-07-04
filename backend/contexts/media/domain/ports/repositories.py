"""Media repository ports."""
from __future__ import annotations

from abc import ABC, abstractmethod

from contexts.media.domain.aggregates.media_asset import MediaAsset
from contexts.media.domain.aggregates.media_variant import MediaVariant
from contexts.media.domain.aggregates.transcode_job import TranscodeJob
from shared.domain.value_objects.unique_id import UniqueId


class IAssetRepository(ABC):
    @abstractmethod
    async def save(self, asset: MediaAsset) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, asset_id: UniqueId) -> MediaAsset | None: ...


class IVariantRepository(ABC):
    @abstractmethod
    async def save(self, variant: MediaVariant) -> None: ...

    @abstractmethod
    async def find_by_profile(
        self, tenant_id: str, asset_id: UniqueId, profile: str
    ) -> MediaVariant | None: ...

    @abstractmethod
    async def list_by_asset(self, tenant_id: str, asset_id: UniqueId) -> list[MediaVariant]: ...


class ITranscodeJobRepository(ABC):
    @abstractmethod
    async def save(self, job: TranscodeJob) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, job_id: UniqueId) -> TranscodeJob | None: ...
