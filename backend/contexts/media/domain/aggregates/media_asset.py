"""Media asset metadata."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class AssetStatus(StrEnum):
    PENDING = "pending"
    READY = "ready"
    DELETED = "deleted"


class MediaKind(StrEnum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"


@dataclass(eq=False, kw_only=True)
class MediaAsset(AggregateRoot):
    tenant_id: str
    file_name: str
    content_type: str
    media_kind: MediaKind
    status: AssetStatus
    storage_key: str | None
    source_ref: str | None
    metadata: dict
    created_by: str | None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(
        cls,
        *,
        tenant_id: str,
        file_name: str,
        content_type: str,
        media_kind: MediaKind,
        source_ref: str | None = None,
        metadata: dict | None = None,
        created_by: str | None = None,
    ) -> MediaAsset:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            file_name=file_name.strip(),
            content_type=content_type,
            media_kind=media_kind,
            status=AssetStatus.PENDING,
            storage_key=None,
            source_ref=source_ref,
            metadata=metadata or {},
            created_by=created_by,
        )

    def complete(self, storage_key: str) -> None:
        self.storage_key = storage_key
        self.status = AssetStatus.READY

    def soft_delete(self) -> None:
        self.status = AssetStatus.DELETED

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "file_name": self.file_name,
            "content_type": self.content_type,
            "media_kind": self.media_kind.value,
            "status": self.status.value,
            "storage_key": self.storage_key,
            "source_ref": self.source_ref,
            "metadata": self.metadata,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat(),
        }
