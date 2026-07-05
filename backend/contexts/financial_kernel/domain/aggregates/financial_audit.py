"""Enterprise financial audit aggregates — immutable append-only trail."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class FinancialAuditAction(StrEnum):
    CREATED = "created"
    APPROVED = "approved"
    POSTED = "posted"
    MODIFIED = "modified"
    REVERSED = "reversed"


@dataclass(eq=False, kw_only=True)
class FinancialAuditEntry(AggregateRoot):
    tenant_id: str
    organization_id: str | None
    resource_type: str
    resource_id: str
    action: str
    actor_id: str
    correlation_id: str
    ip_address: str | None
    device: str | None
    reason: str
    before_state: dict | None
    after_state: dict | None
    payload_checksum: str
    tamper_hash: str
    immutable: bool = True
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    recorded_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def record(
        cls,
        *,
        tenant_id: str,
        organization_id: str | None,
        resource_type: str,
        resource_id: str,
        action: str,
        actor_id: str,
        correlation_id: str,
        payload_checksum: str,
        tamper_hash: str,
        ip_address: str | None = None,
        device: str | None = None,
        reason: str = "",
        before_state: dict | None = None,
        after_state: dict | None = None,
    ) -> FinancialAuditEntry:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            organization_id=organization_id,
            resource_type=resource_type,
            resource_id=resource_id,
            action=action,
            actor_id=actor_id,
            correlation_id=correlation_id,
            ip_address=ip_address,
            device=device,
            reason=reason,
            before_state=before_state,
            after_state=after_state,
            payload_checksum=payload_checksum,
            tamper_hash=tamper_hash,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "organization_id": self.organization_id,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "action": self.action,
            "actor_id": self.actor_id,
            "correlation_id": self.correlation_id,
            "ip_address": self.ip_address,
            "device": self.device,
            "reason": self.reason,
            "before_state": self.before_state,
            "after_state": self.after_state,
            "payload_checksum": self.payload_checksum,
            "tamper_hash": self.tamper_hash,
            "immutable": self.immutable,
            "occurred_at": self.occurred_at.isoformat(),
            "recorded_at": self.recorded_at.isoformat(),
        }
