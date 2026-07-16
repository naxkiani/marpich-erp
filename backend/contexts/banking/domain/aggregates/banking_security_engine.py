"""Banking Security Platform aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class ApprovalStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


class FreezeStatus(StrEnum):
    ACTIVE = "active"
    RELEASED = "released"


class SessionStatus(StrEnum):
    ACTIVE = "active"
    EXPIRED = "expired"
    TERMINATED = "terminated"


@dataclass(eq=False, kw_only=True)
class SecurityApprovalRequest(AggregateRoot):
    tenant_id: str
    request_ref: str
    action_type: str
    resource_id: str
    maker_id: str
    checker_id: str | None = None
    approvers: list[str] = field(default_factory=list)
    required_approvals: int = 1
    status: str = ApprovalStatus.PENDING.value
    payload_checksum: str = ""
    digital_signature: dict | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    completed_at: datetime | None = None

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        request_ref: str,
        action_type: str,
        resource_id: str,
        maker_id: str,
        payload_checksum: str = "",
        required_approvals: int = 1,
    ) -> SecurityApprovalRequest:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            request_ref=request_ref,
            action_type=action_type,
            resource_id=resource_id,
            maker_id=maker_id,
            payload_checksum=payload_checksum,
            required_approvals=required_approvals,
        )

    def approve(self, approver_id: str) -> None:
        if self.status != ApprovalStatus.PENDING.value:
            raise ValueError("not_pending")
        if approver_id == self.maker_id:
            raise ValueError("maker_checker_violation")
        if approver_id in self.approvers:
            raise ValueError("duplicate_approver")
        self.approvers.append(approver_id)
        self.checker_id = approver_id
        if len(self.approvers) >= self.required_approvals:
            self.status = ApprovalStatus.APPROVED.value
            self.completed_at = datetime.now(UTC)

    def reject(self) -> None:
        if self.status != ApprovalStatus.PENDING.value:
            raise ValueError("not_pending")
        self.status = ApprovalStatus.REJECTED.value
        self.completed_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "request_ref": self.request_ref,
            "action_type": self.action_type,
            "resource_id": self.resource_id,
            "maker_id": self.maker_id,
            "checker_id": self.checker_id,
            "approvers": self.approvers,
            "required_approvals": self.required_approvals,
            "status": self.status,
            "payload_checksum": self.payload_checksum,
            "digital_signature": self.digital_signature,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }


@dataclass(eq=False, kw_only=True)
class SecurityDevice(AggregateRoot):
    tenant_id: str
    user_id: str
    device_ref: str
    device_fingerprint: str
    trusted: bool = False
    last_verified_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        user_id: str,
        device_ref: str,
        device_fingerprint: str,
    ) -> SecurityDevice:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            user_id=user_id,
            device_ref=device_ref,
            device_fingerprint=device_fingerprint,
        )

    def verify(self) -> None:
        self.trusted = True
        self.last_verified_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "user_id": self.user_id,
            "device_ref": self.device_ref,
            "device_fingerprint": self.device_fingerprint,
            "trusted": self.trusted,
            "last_verified_at": self.last_verified_at.isoformat() if self.last_verified_at else None,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class SecuritySession(AggregateRoot):
    tenant_id: str
    user_id: str
    session_ref: str
    device_id: str | None = None
    ip_address: str = ""
    status: str = SessionStatus.ACTIVE.value
    risk_score: float = 100.0
    last_activity_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        user_id: str,
        session_ref: str,
        device_id: str | None = None,
        ip_address: str = "",
    ) -> SecuritySession:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            user_id=user_id,
            session_ref=session_ref,
            device_id=device_id,
            ip_address=ip_address,
        )

    def heartbeat(self, *, risk_score: float | None = None) -> None:
        self.last_activity_at = datetime.now(UTC)
        if risk_score is not None:
            self.risk_score = risk_score

    def terminate(self) -> None:
        self.status = SessionStatus.TERMINATED.value

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "user_id": self.user_id,
            "session_ref": self.session_ref,
            "device_id": self.device_id,
            "ip_address": self.ip_address,
            "status": self.status,
            "risk_score": self.risk_score,
            "last_activity_at": self.last_activity_at.isoformat(),
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class TransactionMonitorAlert(AggregateRoot):
    tenant_id: str
    alert_ref: str
    user_id: str
    action_type: str
    amount: float
    currency: str = "USD"
    risk_score: float = 0.0
    factors: list[dict] = field(default_factory=list)
    status: str = "open"
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        alert_ref: str,
        user_id: str,
        action_type: str,
        amount: float,
        currency: str = "USD",
        risk_score: float = 0.0,
        factors: list[dict] | None = None,
    ) -> TransactionMonitorAlert:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            alert_ref=alert_ref,
            user_id=user_id,
            action_type=action_type,
            amount=round(amount, 2),
            currency=currency,
            risk_score=risk_score,
            factors=list(factors or []),
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "alert_ref": self.alert_ref,
            "user_id": self.user_id,
            "action_type": self.action_type,
            "amount": self.amount,
            "currency": self.currency,
            "risk_score": self.risk_score,
            "factors": self.factors,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class EmergencyFreeze(AggregateRoot):
    tenant_id: str
    freeze_ref: str
    scope: str = "tenant"
    reason: str = ""
    activated_by: str = ""
    status: str = FreezeStatus.ACTIVE.value
    activated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    released_at: datetime | None = None

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        freeze_ref: str,
        scope: str = "tenant",
        reason: str = "",
        activated_by: str = "",
    ) -> EmergencyFreeze:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            freeze_ref=freeze_ref,
            scope=scope,
            reason=reason,
            activated_by=activated_by,
        )

    def release(self) -> None:
        self.status = FreezeStatus.RELEASED.value
        self.released_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "freeze_ref": self.freeze_ref,
            "scope": self.scope,
            "reason": self.reason,
            "activated_by": self.activated_by,
            "status": self.status,
            "activated_at": self.activated_at.isoformat(),
            "released_at": self.released_at.isoformat() if self.released_at else None,
        }


@dataclass(eq=False, kw_only=True)
class SecurityAuditEntry(AggregateRoot):
    tenant_id: str
    audit_ref: str
    action: str
    actor_id: str
    resource_type: str
    resource_id: str
    payload_checksum: str
    tamper_hash: str
    detail: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        audit_ref: str,
        action: str,
        actor_id: str,
        resource_type: str,
        resource_id: str,
        payload_checksum: str,
        tamper_hash: str,
        detail: str = "",
    ) -> SecurityAuditEntry:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            audit_ref=audit_ref,
            action=action,
            actor_id=actor_id,
            resource_type=resource_type,
            resource_id=resource_id,
            payload_checksum=payload_checksum,
            tamper_hash=tamper_hash,
            detail=detail,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "audit_ref": self.audit_ref,
            "action": self.action,
            "actor_id": self.actor_id,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "payload_checksum": self.payload_checksum,
            "tamper_hash": self.tamper_hash,
            "detail": self.detail,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class LimitUsageTracker(AggregateRoot):
    tenant_id: str
    user_id: str
    usage_date: str
    daily_total: float = 0.0
    velocity_count: int = 0
    currency: str = "USD"

    def add_transaction(self, amount: float) -> None:
        self.daily_total = round(self.daily_total + amount, 2)
        self.velocity_count += 1

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "user_id": self.user_id,
            "usage_date": self.usage_date,
            "daily_total": self.daily_total,
            "velocity_count": self.velocity_count,
            "currency": self.currency,
        }
