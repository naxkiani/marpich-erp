"""Enterprise financial security aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class SecurityControlType(StrEnum):
    MAKER_CHECKER = "maker_checker"
    FOUR_EYES = "four_eyes"
    DUAL_APPROVAL = "dual_approval"


class SecurityRequestStatus(StrEnum):
    PENDING = "pending"
    FIRST_APPROVED = "first_approved"
    APPROVED = "approved"
    REJECTED = "rejected"


class PolicyType(StrEnum):
    RBAC = "rbac"
    ABAC = "abac"


class CloseType(StrEnum):
    PERIOD = "period"
    FISCAL_YEAR = "fiscal_year"


@dataclass(eq=False, kw_only=True)
class SecurityAuditRecord(AggregateRoot):
    tenant_id: str
    action: str
    actor_id: str
    resource_type: str
    resource_id: str
    payload_checksum: str
    before_state: dict | None
    after_state: dict | None
    tamper_hash: str
    correlation_id: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def record(
        cls,
        *,
        tenant_id: str,
        action: str,
        actor_id: str,
        resource_type: str,
        resource_id: str,
        payload_checksum: str,
        tamper_hash: str,
        correlation_id: str = "",
        before_state: dict | None = None,
        after_state: dict | None = None,
    ) -> SecurityAuditRecord:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            action=action,
            actor_id=actor_id,
            resource_type=resource_type,
            resource_id=resource_id,
            payload_checksum=payload_checksum,
            before_state=before_state,
            after_state=after_state,
            tamper_hash=tamper_hash,
            correlation_id=correlation_id,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "action": self.action,
            "actor_id": self.actor_id,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "payload_checksum": self.payload_checksum,
            "before_state": self.before_state,
            "after_state": self.after_state,
            "tamper_hash": self.tamper_hash,
            "correlation_id": self.correlation_id,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class SecurityPolicy(AggregateRoot):
    tenant_id: str
    name: str
    policy_type: str
    resource_type: str
    rules: dict
    is_active: bool
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        name: str,
        policy_type: str,
        resource_type: str,
        rules: dict,
    ) -> SecurityPolicy:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            name=name.strip(),
            policy_type=policy_type,
            resource_type=resource_type,
            rules=rules,
            is_active=True,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "name": self.name,
            "policy_type": self.policy_type,
            "resource_type": self.resource_type,
            "rules": self.rules,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class MakerCheckerRequest(AggregateRoot):
    tenant_id: str
    control_type: str
    resource_type: str
    resource_id: str
    idempotency_key: str
    maker_id: str
    checker_id: str | None
    second_approver_id: str | None
    status: SecurityRequestStatus
    payload: dict
    payload_checksum: str
    encrypted_payload: str | None
    signature: dict | None
    correlation_id: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    completed_at: datetime | None = None

    @classmethod
    def submit(
        cls,
        *,
        tenant_id: str,
        control_type: str,
        resource_type: str,
        resource_id: str,
        idempotency_key: str,
        maker_id: str,
        payload: dict,
        payload_checksum: str,
        encrypted_payload: str | None,
        correlation_id: str,
        checker_id: str | None = None,
        second_approver_id: str | None = None,
    ) -> MakerCheckerRequest:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            control_type=control_type,
            resource_type=resource_type,
            resource_id=resource_id,
            idempotency_key=idempotency_key,
            maker_id=maker_id,
            checker_id=checker_id,
            second_approver_id=second_approver_id,
            status=SecurityRequestStatus.PENDING,
            payload=payload,
            payload_checksum=payload_checksum,
            encrypted_payload=encrypted_payload,
            signature=None,
            correlation_id=correlation_id,
        )

    def approve(self, approver_id: str) -> None:
        if self.status == SecurityRequestStatus.REJECTED:
            raise ValueError("request_rejected")
        if approver_id == self.maker_id:
            raise ValueError("maker_cannot_approve")

        if self.control_type == SecurityControlType.MAKER_CHECKER.value:
            if self.checker_id and approver_id != self.checker_id:
                raise ValueError("invalid_checker")
            self.status = SecurityRequestStatus.APPROVED
            self.completed_at = datetime.now(UTC)
        elif self.control_type in (
            SecurityControlType.FOUR_EYES.value,
            SecurityControlType.DUAL_APPROVAL.value,
        ):
            if self.status == SecurityRequestStatus.PENDING:
                if self.second_approver_id and approver_id == self.second_approver_id:
                    raise ValueError("same_approver_not_allowed")
                self.checker_id = approver_id
                self.status = SecurityRequestStatus.FIRST_APPROVED
            elif self.status == SecurityRequestStatus.FIRST_APPROVED:
                if approver_id == self.checker_id:
                    raise ValueError("same_approver_not_allowed")
                self.second_approver_id = approver_id
                self.status = SecurityRequestStatus.APPROVED
                self.completed_at = datetime.now(UTC)
        else:
            raise ValueError("invalid_control_type")

    def reject(self, actor_id: str) -> None:
        if actor_id == self.maker_id:
            raise ValueError("maker_cannot_reject_own_submission")
        self.status = SecurityRequestStatus.REJECTED
        self.completed_at = datetime.now(UTC)

    def sign(self, signature: dict) -> None:
        if self.status != SecurityRequestStatus.APPROVED:
            raise ValueError("not_approved")
        self.signature = signature

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "control_type": self.control_type,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "idempotency_key": self.idempotency_key,
            "maker_id": self.maker_id,
            "checker_id": self.checker_id,
            "second_approver_id": self.second_approver_id,
            "status": self.status.value,
            "payload_checksum": self.payload_checksum,
            "encrypted_payload": self.encrypted_payload,
            "signature": self.signature,
            "correlation_id": self.correlation_id,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }


@dataclass(eq=False, kw_only=True)
class TransactionLock(AggregateRoot):
    tenant_id: str
    resource_type: str
    resource_id: str
    locked_by: str
    reason: str
    is_active: bool
    locked_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    released_at: datetime | None = None

    @classmethod
    def lock(
        cls,
        *,
        tenant_id: str,
        resource_type: str,
        resource_id: str,
        locked_by: str,
        reason: str,
    ) -> TransactionLock:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            resource_type=resource_type,
            resource_id=resource_id,
            locked_by=locked_by,
            reason=reason.strip(),
            is_active=True,
        )

    def release(self) -> None:
        self.is_active = False
        self.released_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "locked_by": self.locked_by,
            "reason": self.reason,
            "is_active": self.is_active,
            "locked_at": self.locked_at.isoformat(),
            "released_at": self.released_at.isoformat() if self.released_at else None,
        }


@dataclass(eq=False, kw_only=True)
class PeriodCloseRequest(AggregateRoot):
    tenant_id: str
    close_type: str
    target_id: str
    requester_id: str
    first_approver_id: str | None
    second_approver_id: str | None
    status: SecurityRequestStatus
    correlation_id: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    closed_at: datetime | None = None

    @classmethod
    def request(
        cls,
        *,
        tenant_id: str,
        close_type: str,
        target_id: str,
        requester_id: str,
        correlation_id: str,
    ) -> PeriodCloseRequest:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            close_type=close_type,
            target_id=target_id,
            requester_id=requester_id,
            first_approver_id=None,
            second_approver_id=None,
            status=SecurityRequestStatus.PENDING,
            correlation_id=correlation_id,
        )

    def approve(self, approver_id: str) -> None:
        if approver_id == self.requester_id:
            raise ValueError("requester_cannot_approve")
        if self.status == SecurityRequestStatus.PENDING:
            self.first_approver_id = approver_id
            self.status = SecurityRequestStatus.FIRST_APPROVED
        elif self.status == SecurityRequestStatus.FIRST_APPROVED:
            if approver_id == self.first_approver_id:
                raise ValueError("same_approver_not_allowed")
            self.second_approver_id = approver_id
            self.status = SecurityRequestStatus.APPROVED
            self.closed_at = datetime.now(UTC)
        else:
            raise ValueError("invalid_status")

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "close_type": self.close_type,
            "target_id": self.target_id,
            "requester_id": self.requester_id,
            "first_approver_id": self.first_approver_id,
            "second_approver_id": self.second_approver_id,
            "status": self.status.value,
            "correlation_id": self.correlation_id,
            "created_at": self.created_at.isoformat(),
            "closed_at": self.closed_at.isoformat() if self.closed_at else None,
        }
