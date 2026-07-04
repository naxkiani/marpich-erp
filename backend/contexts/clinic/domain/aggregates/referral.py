"""Referral aggregate — clinic to specialist/hospital."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId

from contexts.clinic.domain.events.integration_events import ReferralSentIntegration


class ReferralStatus(StrEnum):
    DRAFT = "draft"
    SENT = "sent"
    ACCEPTED = "accepted"
    CANCELLED = "cancelled"


@dataclass(eq=False, kw_only=True)
class Referral(AggregateRoot):
    tenant_id: str
    encounter_id: UniqueId
    patient_id: UniqueId
    target_specialty: str
    reason: str
    status: ReferralStatus = ReferralStatus.DRAFT
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    sent_at: datetime | None = None

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        encounter_id: UniqueId,
        patient_id: UniqueId,
        target_specialty: str,
        reason: str,
    ) -> Referral:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            encounter_id=encounter_id,
            patient_id=patient_id,
            target_specialty=target_specialty.strip(),
            reason=reason.strip(),
        )

    def send(self, *, correlation_id: str) -> ReferralSentIntegration:
        if self.status == ReferralStatus.SENT:
            raise ValueError("clinic.errors.referral_already_sent")
        self.status = ReferralStatus.SENT
        self.sent_at = datetime.now(UTC)
        return ReferralSentIntegration(
            tenant_id=TenantId.create(self.tenant_id),
            correlation_id=correlation_id,
            referral_id=self.id,
            encounter_id=self.encounter_id,
            patient_id=self.patient_id,
            target_specialty=self.target_specialty,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "encounter_id": str(self.encounter_id),
            "patient_id": str(self.patient_id),
            "target_specialty": self.target_specialty,
            "reason": self.reason,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "sent_at": self.sent_at.isoformat() if self.sent_at else None,
        }
