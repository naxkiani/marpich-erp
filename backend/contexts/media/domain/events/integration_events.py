"""Media integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(frozen=True, kw_only=True)
class AssetUploadedIntegration(IntegrationEvent):
    asset_id: UniqueId
    file_name: str
    media_kind: str

    @property
    def event_name(self) -> str:
        return "media.asset.uploaded"

    @property
    def source_context(self) -> str:
        return "media"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "asset_id": str(self.asset_id),
            "file_name": self.file_name,
            "media_kind": self.media_kind,
        }


@dataclass(frozen=True, kw_only=True)
class TranscodeCompletedIntegration(IntegrationEvent):
    asset_id: UniqueId
    job_id: UniqueId
    profile: str
    variant_url: str

    @property
    def event_name(self) -> str:
        return "media.transcode.completed"

    @property
    def source_context(self) -> str:
        return "media"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "asset_id": str(self.asset_id),
            "job_id": str(self.job_id),
            "profile": self.profile,
            "variant_url": self.variant_url,
        }


@dataclass(frozen=True, kw_only=True)
class AssetDeletedIntegration(IntegrationEvent):
    asset_id: UniqueId
    file_name: str

    @property
    def event_name(self) -> str:
        return "media.asset.deleted"

    @property
    def source_context(self) -> str:
        return "media"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"asset_id": str(self.asset_id), "file_name": self.file_name}
