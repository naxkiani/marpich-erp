"""Municipality permit aggregate."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId

from contexts.municipality.domain.events.integration_events import PermitIssuedIntegration


class PermitStatus(StrEnum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    ISSUED = "issued"
    REJECTED = "rejected"


@dataclass(eq=False, kw_only=True)
class Permit(AggregateRoot):
    tenant_id: str
    applicant_name: str
    permit_type: str
    description: str
    status: PermitStatus = PermitStatus.DRAFT
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    issued_at: datetime | None = None

    @classmethod
    def apply(
        cls,
        *,
        tenant_id: str,
        applicant_name: str,
        permit_type: str,
        description: str,
    ) -> Permit:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            applicant_name=applicant_name.strip(),
            permit_type=permit_type.strip(),
            description=description.strip(),
            status=PermitStatus.SUBMITTED,
        )

    def issue(self, *, correlation_id: str) -> PermitIssuedIntegration:
        if self.status == PermitStatus.ISSUED:
            raise ValueError("municipality.errors.permit_already_issued")
        self.status = PermitStatus.ISSUED
        self.issued_at = datetime.now(UTC)
        return PermitIssuedIntegration(
            tenant_id=TenantId.create(self.tenant_id),
            correlation_id=correlation_id,
            permit_id=self.id,
            permit_type=self.permit_type,
            applicant_name=self.applicant_name,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "applicant_name": self.applicant_name,
            "permit_type": self.permit_type,
            "description": self.description,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "issued_at": self.issued_at.isoformat() if self.issued_at else None,
        }
