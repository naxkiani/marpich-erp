"""Document metadata aggregate."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from contexts.documents.domain.value_objects.physical_location import PhysicalLocation
from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class DocumentStatus(StrEnum):
    ACTIVE = "active"
    ARCHIVED = "archived"


@dataclass(eq=False, kw_only=True)
class Document(AggregateRoot):
    tenant_id: str
    folder_id: UniqueId
    title: str
    description: str
    current_version_id: UniqueId | None
    status: DocumentStatus
    metadata: dict
    created_by: str | None
    qr_token: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        folder_id: UniqueId,
        title: str,
        description: str = "",
        metadata: dict | None = None,
        created_by: str | None = None,
    ) -> Document:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            folder_id=folder_id,
            title=title.strip(),
            description=description.strip(),
            current_version_id=None,
            status=DocumentStatus.ACTIVE,
            metadata=metadata or {},
            created_by=created_by,
            qr_token=None,
        )

    def set_current_version(self, version_id: UniqueId) -> None:
        self.current_version_id = version_id

    def set_qr_token(self, token: str) -> None:
        self.qr_token = token
        self.metadata = {**self.metadata, "qr_token": token}

    def archive(self) -> None:
        self.status = DocumentStatus.ARCHIVED

    def physical_location(self) -> PhysicalLocation | None:
        return PhysicalLocation.from_dict(self.metadata.get("physical_location"))

    def assign_physical_location(self, location: PhysicalLocation) -> None:
        if self.status == DocumentStatus.ARCHIVED:
            raise ValueError("documents.errors.document_archived")
        self.metadata = {**self.metadata, "physical_location": location.to_dict()}

    def to_dict(self) -> dict:
        location = self.physical_location()
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "folder_id": str(self.folder_id),
            "title": self.title,
            "description": self.description,
            "current_version_id": str(self.current_version_id) if self.current_version_id else None,
            "status": self.status.value,
            "metadata": self.metadata,
            "physical_location": location.to_dict() if location else None,
            "qr_token": self.qr_token or self.metadata.get("qr_token"),
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat(),
        }
