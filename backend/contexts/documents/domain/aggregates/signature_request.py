"""E-signature request aggregate."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class SignatureStatus(StrEnum):
    PENDING = "pending"
    SIGNED = "signed"
    REJECTED = "rejected"


@dataclass(eq=False, kw_only=True)
class SignatureRequest(AggregateRoot):
    tenant_id: str
    document_id: UniqueId
    version_id: UniqueId
    requester_id: str
    signers: list[str]
    status: SignatureStatus
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    completed_at: datetime | None = None

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        document_id: UniqueId,
        version_id: UniqueId,
        requester_id: str,
        signers: list[str],
    ) -> SignatureRequest:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            document_id=document_id,
            version_id=version_id,
            requester_id=requester_id,
            signers=signers,
            status=SignatureStatus.PENDING,
        )

    def mark_signed(self) -> None:
        self.status = SignatureStatus.SIGNED
        self.completed_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "document_id": str(self.document_id),
            "version_id": str(self.version_id),
            "requester_id": self.requester_id,
            "signers": self.signers,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }
