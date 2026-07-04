"""Document version — immutable content snapshot."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class DocumentVersion(AggregateRoot):
    tenant_id: str
    document_id: UniqueId
    version_number: int
    file_name: str
    content_type: str
    content: str
    checksum: str
    storage_key: str | None
    created_by: str | None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        document_id: UniqueId,
        version_number: int,
        file_name: str,
        content_type: str,
        content: str,
        checksum: str,
        storage_key: str | None = None,
        created_by: str | None = None,
    ) -> DocumentVersion:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            document_id=document_id,
            version_number=version_number,
            file_name=file_name.strip(),
            content_type=content_type,
            content=content,
            checksum=checksum,
            storage_key=storage_key,
            created_by=created_by,
        )

    def to_dict(self, *, include_content: bool = False) -> dict:
        result = {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "document_id": str(self.document_id),
            "version_number": self.version_number,
            "file_name": self.file_name,
            "content_type": self.content_type,
            "checksum": self.checksum,
            "storage_key": self.storage_key,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat(),
        }
        if include_content:
            result["content"] = self.content
        return result
