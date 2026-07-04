"""Transcoded or thumbnail variant."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class MediaVariant(AggregateRoot):
    tenant_id: str
    asset_id: UniqueId
    profile: str
    url: str
    width: int | None
    height: int | None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        asset_id: UniqueId,
        profile: str,
        url: str,
        width: int | None = None,
        height: int | None = None,
    ) -> MediaVariant:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            asset_id=asset_id,
            profile=profile.strip().lower(),
            url=url,
            width=width,
            height=height,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "asset_id": str(self.asset_id),
            "profile": self.profile,
            "url": self.url,
            "width": self.width,
            "height": self.height,
            "created_at": self.created_at.isoformat(),
        }
