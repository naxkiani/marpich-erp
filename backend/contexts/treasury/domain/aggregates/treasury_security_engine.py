"""Treasury Security aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class SecurityPolicyType(StrEnum):
    MAKER_CHECKER = "maker_checker"
    FOUR_EYES = "four_eyes"
    SEGREGATION_OF_DUTIES = "segregation_of_duties"
    TRANSACTION_LIMITS = "transaction_limits"
    APPROVAL_MATRIX = "approval_matrix"
    DIGITAL_SIGNATURE = "digital_signature"
    ROLE_BASED_ACCESS = "role_based_access"
    ATTRIBUTE_BASED_ACCESS = "attribute_based_access"
    DEVICE_VERIFICATION = "device_verification"
    RISK_BASED_AUTH = "risk_based_authentication"
    TRANSACTION_LOCKING = "transaction_locking"
    EMERGENCY_FREEZE = "emergency_freeze"


class OperationStatus(StrEnum):
    DRAFT = "draft"
    PENDING_CHECKER = "pending_checker"
    APPROVED = "approved"
    REJECTED = "rejected"
    LOCKED = "locked"


class FreezeScope(StrEnum):
    TENANT = "tenant"
    ACCOUNT = "account"
    OPERATION_TYPE = "operation_type"


@dataclass(eq=False, kw_only=True)
class TreasurySecurityPolicy(AggregateRoot):
    tenant_id: str
    name: str
    policy_type: str
    rules: dict
    is_active: bool = True
    description: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        name: str,
        policy_type: str,
        rules: dict,
        description: str = "",
    ) -> TreasurySecurityPolicy:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            name=name.strip(),
            policy_type=policy_type,
            rules=rules,
            description=description,
        )

    def deactivate(self) -> None:
        self.is_active = False

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "name": self.name,
            "policy_type": self.policy_type,
            "rules": self.rules,
            "is_active": self.is_active,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class TreasuryTransactionLimit(AggregateRoot):
    tenant_id: str
    operation_type: str
    name: str
    max_amount: float
    currency: str
    daily_limit: float | None = None
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        operation_type: str,
        name: str,
        max_amount: float,
        currency: str = "USD",
        daily_limit: float | None = None,
    ) -> TreasuryTransactionLimit:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            operation_type=operation_type,
            name=name.strip(),
            max_amount=round(max_amount, 2),
            currency=currency.strip().upper(),
            daily_limit=round(daily_limit, 2) if daily_limit is not None else None,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "operation_type": self.operation_type,
            "name": self.name,
            "max_amount": self.max_amount,
            "currency": self.currency,
            "daily_limit": self.daily_limit,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class TreasuryApprovalMatrix(AggregateRoot):
    tenant_id: str
    operation_type: str
    role: str
    min_amount: float
    max_amount: float
    approval_level: int
    currency: str = "USD"
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        operation_type: str,
        role: str,
        min_amount: float,
        max_amount: float,
        approval_level: int,
        currency: str = "USD",
    ) -> TreasuryApprovalMatrix:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            operation_type=operation_type,
            role=role.strip(),
            min_amount=round(min_amount, 2),
            max_amount=round(max_amount, 2),
            approval_level=approval_level,
            currency=currency.strip().upper(),
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "operation_type": self.operation_type,
            "role": self.role,
            "min_amount": self.min_amount,
            "max_amount": self.max_amount,
            "approval_level": self.approval_level,
            "currency": self.currency,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class TreasuryAccessRule(AggregateRoot):
    tenant_id: str
    rule_type: str
    name: str
    roles: list[str] = field(default_factory=list)
    attributes: dict = field(default_factory=dict)
    allowed_operations: list[str] = field(default_factory=list)
    denied_operations: list[str] = field(default_factory=list)
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        rule_type: str,
        name: str,
        roles: list[str] | None = None,
        attributes: dict | None = None,
        allowed_operations: list[str] | None = None,
        denied_operations: list[str] | None = None,
    ) -> TreasuryAccessRule:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            rule_type=rule_type,
            name=name.strip(),
            roles=roles or [],
            attributes=attributes or {},
            allowed_operations=allowed_operations or [],
            denied_operations=denied_operations or [],
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "rule_type": self.rule_type,
            "name": self.name,
            "roles": self.roles,
            "attributes": self.attributes,
            "allowed_operations": self.allowed_operations,
            "denied_operations": self.denied_operations,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class TreasurySecurityLock(AggregateRoot):
    tenant_id: str
    lock_type: str
    subject_ref: str
    subject_type: str
    reason: str
    locked_by: str
    is_active: bool = True
    released_at: datetime | None = None
    released_by: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        lock_type: str,
        subject_ref: str,
        subject_type: str,
        reason: str,
        locked_by: str,
    ) -> TreasurySecurityLock:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            lock_type=lock_type,
            subject_ref=subject_ref,
            subject_type=subject_type,
            reason=reason,
            locked_by=locked_by,
        )

    def release(self, *, released_by: str) -> None:
        if not self.is_active:
            raise ValueError("lock_already_released")
        self.is_active = False
        self.released_at = datetime.now(UTC)
        self.released_by = released_by

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "lock_type": self.lock_type,
            "subject_ref": self.subject_ref,
            "subject_type": self.subject_type,
            "reason": self.reason,
            "locked_by": self.locked_by,
            "is_active": self.is_active,
            "released_at": self.released_at.isoformat() if self.released_at else None,
            "released_by": self.released_by,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class TreasurySecurityOperation(AggregateRoot):
    tenant_id: str
    operation_type: str
    subject_ref: str
    amount: float
    currency: str
    maker_id: str
    checker_id: str | None = None
    status: str = OperationStatus.DRAFT.value
    required_approvers: int = 2
    approvers: list[dict] = field(default_factory=list)
    digital_signatures: list[dict] = field(default_factory=list)
    risk_score: float = 0.0
    device_verified: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        operation_type: str,
        subject_ref: str,
        amount: float,
        currency: str,
        maker_id: str,
        required_approvers: int = 2,
        risk_score: float = 0.0,
        device_verified: bool = False,
    ) -> TreasurySecurityOperation:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            operation_type=operation_type,
            subject_ref=subject_ref,
            amount=round(amount, 2),
            currency=currency.strip().upper(),
            maker_id=maker_id,
            required_approvers=required_approvers,
            risk_score=risk_score,
            device_verified=device_verified,
        )

    def submit_for_checker(self) -> None:
        if self.status != OperationStatus.DRAFT.value:
            raise ValueError("only_draft_can_submit")
        self.status = OperationStatus.PENDING_CHECKER.value
        self.updated_at = datetime.now(UTC)

    def approve_by_checker(
        self,
        *,
        checker_id: str,
        signature_hash: str | None = None,
    ) -> None:
        if self.status != OperationStatus.PENDING_CHECKER.value:
            raise ValueError("not_pending_checker")
        if checker_id == self.maker_id:
            raise ValueError("maker_cannot_be_checker")
        if any(a.get("approver_id") == checker_id for a in self.approvers):
            raise ValueError("checker_already_approved")

        self.approvers.append(
            {
                "approver_id": checker_id,
                "approved_at": datetime.now(UTC).isoformat(),
            }
        )
        if signature_hash:
            self.digital_signatures.append(
                {
                    "approver_id": checker_id,
                    "signature_hash": signature_hash,
                    "signed_at": datetime.now(UTC).isoformat(),
                }
            )

        if len(self.approvers) >= self.required_approvers:
            self.status = OperationStatus.APPROVED.value
            self.checker_id = checker_id

        self.updated_at = datetime.now(UTC)

    def reject(self, *, checker_id: str, reason: str = "") -> None:
        if self.status != OperationStatus.PENDING_CHECKER.value:
            raise ValueError("not_pending_checker")
        self.status = OperationStatus.REJECTED.value
        self.approvers.append(
            {
                "approver_id": checker_id,
                "action": "rejected",
                "reason": reason,
                "at": datetime.now(UTC).isoformat(),
            }
        )
        self.updated_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "operation_type": self.operation_type,
            "subject_ref": self.subject_ref,
            "amount": self.amount,
            "currency": self.currency,
            "maker_id": self.maker_id,
            "checker_id": self.checker_id,
            "status": self.status,
            "required_approvers": self.required_approvers,
            "approvers": self.approvers,
            "digital_signatures": self.digital_signatures,
            "risk_score": self.risk_score,
            "device_verified": self.device_verified,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class TreasurySecurityAudit(AggregateRoot):
    tenant_id: str
    action: str
    actor_id: str | None
    subject_ref: str
    subject_type: str
    detail: str
    sensitivity: str = "high"
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        action: str,
        actor_id: str | None = None,
        subject_ref: str = "",
        subject_type: str = "security",
        detail: str = "",
        sensitivity: str = "high",
    ) -> TreasurySecurityAudit:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            action=action,
            actor_id=actor_id,
            subject_ref=subject_ref,
            subject_type=subject_type,
            detail=detail,
            sensitivity=sensitivity,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "action": self.action,
            "actor_id": self.actor_id,
            "subject_ref": self.subject_ref,
            "subject_type": self.subject_type,
            "detail": self.detail,
            "sensitivity": self.sensitivity,
            "occurred_at": self.occurred_at.isoformat(),
        }
