"""CRM Opportunity aggregate — CAP-ENT-001 pipeline."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from decimal import Decimal
from enum import StrEnum

from contexts.crm.domain.events.integration_events import (
    OpportunityLostIntegration,
    OpportunityWonIntegration,
)
from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId


class OpportunityStage(StrEnum):
    QUALIFYING = "qualifying"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    WON = "won"
    LOST = "lost"


@dataclass(eq=False, kw_only=True)
class Opportunity(AggregateRoot):
    tenant_id: str
    contact_id: UniqueId
    title: str
    amount: Decimal
    currency: str = "USD"
    stage: OpportunityStage = OpportunityStage.QUALIFYING
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    closed_at: datetime | None = None

    @classmethod
    def open(
        cls,
        *,
        tenant_id: str,
        contact_id: UniqueId,
        title: str,
        amount: Decimal,
        currency: str = "USD",
    ) -> Opportunity:
        if amount < 0:
            raise ValueError("crm.errors.amount_negative")
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            contact_id=contact_id,
            title=title.strip(),
            amount=amount,
            currency=currency.strip().upper() or "USD",
        )

    def win(self, *, correlation_id: str) -> OpportunityWonIntegration:
        if self.stage in (OpportunityStage.WON, OpportunityStage.LOST):
            raise ValueError("crm.errors.opportunity_closed")
        self.stage = OpportunityStage.WON
        self.closed_at = datetime.now(UTC)
        self.updated_at = self.closed_at
        return OpportunityWonIntegration(
            tenant_id=TenantId.create(self.tenant_id),
            correlation_id=correlation_id,
            opportunity_id=self.id,
            contact_id=self.contact_id,
            title=self.title,
            amount=str(self.amount),
            currency=self.currency,
        )

    def lose(self, *, correlation_id: str, reason: str | None = None) -> OpportunityLostIntegration:
        if self.stage in (OpportunityStage.WON, OpportunityStage.LOST):
            raise ValueError("crm.errors.opportunity_closed")
        self.stage = OpportunityStage.LOST
        self.closed_at = datetime.now(UTC)
        self.updated_at = self.closed_at
        return OpportunityLostIntegration(
            tenant_id=TenantId.create(self.tenant_id),
            correlation_id=correlation_id,
            opportunity_id=self.id,
            contact_id=self.contact_id,
            title=self.title,
            reason=reason or "",
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "contact_id": str(self.contact_id),
            "title": self.title,
            "amount": str(self.amount),
            "currency": self.currency,
            "stage": self.stage.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "closed_at": self.closed_at.isoformat() if self.closed_at else None,
        }
