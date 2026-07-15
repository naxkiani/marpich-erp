"""Enterprise Identity Lifecycle Platform aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class LifecycleCapability(StrEnum):
    LIFECYCLE_WORKFLOW_ENGINE = "lifecycle_workflow_engine"
    REGISTRATION_INVITATION = "registration_invitation"
    VERIFICATION_ORCHESTRATION = "verification_orchestration"
    KYC_AML_COMPLIANCE = "kyc_aml_compliance"
    ACCOUNT_STATE_MANAGEMENT = "account_state_management"
    IDENTITY_MERGE_SPLIT = "identity_merge_split"
    ARCHIVE_RECOVERY = "archive_recovery"
    DELETION_GOVERNANCE = "deletion_governance"
    CONSENT_MANAGEMENT = "consent_management"
    LIFECYCLE_AUDIT_TRAIL = "lifecycle_audit_trail"
    AI_LIFECYCLE_ASSISTANT = "ai_lifecycle_assistant"
    POLICY_DRIVEN_LIFECYCLE = "policy_driven_lifecycle"
    LIFECYCLE_DASHBOARD = "lifecycle_dashboard"
    LIFECYCLE_API = "lifecycle_api"


class LifecycleState(StrEnum):
    DRAFT = "draft"
    INVITED = "invited"
    REGISTERED = "registered"
    PENDING_VERIFICATION = "pending_verification"
    VERIFIED = "verified"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    TEMPORARILY_DISABLED = "temporarily_disabled"
    ARCHIVED = "archived"
    RECOVERY_PENDING = "recovery_pending"
    MERGED = "merged"
    SOFT_DELETED = "soft_deleted"
    HARD_DELETED = "hard_deleted"


class LifecycleAction(StrEnum):
    REGISTRATION = "registration"
    INVITATION = "invitation"
    IDENTITY_VERIFICATION = "identity_verification"
    EMAIL_VERIFICATION = "email_verification"
    PHONE_VERIFICATION = "phone_verification"
    GOVERNMENT_ID_VERIFICATION = "government_id_verification"
    KYC = "kyc"
    AML = "aml"
    BACKGROUND_VERIFICATION = "background_verification"
    ACCOUNT_ACTIVATION = "account_activation"
    SUSPENSION = "suspension"
    TEMPORARY_DISABLE = "temporary_disable"
    REACTIVATION = "reactivation"
    MERGE_IDENTITIES = "merge_identities"
    SPLIT_IDENTITY = "split_identity"
    IDENTITY_ARCHIVE = "identity_archive"
    IDENTITY_RECOVERY = "identity_recovery"
    IDENTITY_DELETION = "identity_deletion"
    SOFT_DELETE = "soft_delete"
    HARD_DELETE = "hard_delete"
    CONSENT_MANAGEMENT = "consent_management"


class VerificationStatus(StrEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    PASSED = "passed"
    FAILED = "failed"
    EXPIRED = "expired"


@dataclass(eq=False, kw_only=True)
class LifecycleProfile(AggregateRoot):
    tenant_id: str
    profile_ref: str
    registration_enabled: bool = True
    invitation_enabled: bool = True
    kyc_required: bool = False
    aml_required: bool = False
    consent_required: bool = True
    soft_delete_retention_days: int = 30
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(cls, *, tenant_id: str, profile_ref: str) -> LifecycleProfile:
        return cls(id=UniqueId.generate(), tenant_id=tenant_id, profile_ref=profile_ref)

    def to_dict(self) -> dict:
        return {
            "profile_ref": self.profile_ref,
            "tenant_id": self.tenant_id,
            "registration_enabled": self.registration_enabled,
            "invitation_enabled": self.invitation_enabled,
            "kyc_required": self.kyc_required,
            "aml_required": self.aml_required,
            "consent_required": self.consent_required,
            "soft_delete_retention_days": self.soft_delete_retention_days,
        }


@dataclass(eq=False, kw_only=True)
class LifecycleCase(AggregateRoot):
    tenant_id: str
    case_ref: str
    identity_ref: str
    email: str
    display_name: str
    state: str = LifecycleState.DRAFT.value
    user_id: str | None = None
    merged_into: str | None = None
    metadata: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def open(
        cls,
        *,
        tenant_id: str,
        case_ref: str,
        identity_ref: str,
        email: str,
        display_name: str,
        user_id: str | None = None,
    ) -> LifecycleCase:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            case_ref=case_ref,
            identity_ref=identity_ref,
            email=email.lower(),
            display_name=display_name,
            user_id=user_id,
            state=LifecycleState.REGISTERED.value,
        )

    def transition(self, new_state: str) -> None:
        self.state = new_state
        self.updated_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "case_ref": self.case_ref,
            "tenant_id": self.tenant_id,
            "identity_ref": self.identity_ref,
            "email": self.email,
            "display_name": self.display_name,
            "state": self.state,
            "user_id": self.user_id,
            "merged_into": self.merged_into,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class LifecycleTransition(AggregateRoot):
    tenant_id: str
    transition_ref: str
    case_ref: str
    action: str
    from_state: str
    to_state: str
    actor_id: str | None = None
    reason: str = ""
    metadata: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def record(
        cls,
        *,
        tenant_id: str,
        transition_ref: str,
        case_ref: str,
        action: str,
        from_state: str,
        to_state: str,
        actor_id: str | None = None,
        reason: str = "",
        metadata: dict | None = None,
    ) -> LifecycleTransition:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            transition_ref=transition_ref,
            case_ref=case_ref,
            action=action,
            from_state=from_state,
            to_state=to_state,
            actor_id=actor_id,
            reason=reason,
            metadata=metadata or {},
        )

    def to_dict(self) -> dict:
        return {
            "transition_ref": self.transition_ref,
            "case_ref": self.case_ref,
            "action": self.action,
            "from_state": self.from_state,
            "to_state": self.to_state,
            "actor_id": self.actor_id,
            "reason": self.reason,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class VerificationTask(AggregateRoot):
    tenant_id: str
    task_ref: str
    case_ref: str
    verification_type: str
    status: str = VerificationStatus.PENDING.value
    result: dict = field(default_factory=dict)
    expires_at: datetime | None = None
    completed_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        task_ref: str,
        case_ref: str,
        verification_type: str,
    ) -> VerificationTask:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            task_ref=task_ref,
            case_ref=case_ref,
            verification_type=verification_type,
        )

    def mark_passed(self, result: dict | None = None) -> None:
        self.status = VerificationStatus.PASSED.value
        self.result = result or {"verified": True}
        self.completed_at = datetime.now(UTC)

    def mark_failed(self, reason: str) -> None:
        self.status = VerificationStatus.FAILED.value
        self.result = {"verified": False, "reason": reason}
        self.completed_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "task_ref": self.task_ref,
            "case_ref": self.case_ref,
            "verification_type": self.verification_type,
            "status": self.status,
            "result": self.result,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class ConsentRecord(AggregateRoot):
    tenant_id: str
    consent_ref: str
    case_ref: str
    purpose: str
    granted: bool
    version: str = "1.0"
    granted_at: datetime | None = None
    revoked_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def grant(
        cls,
        *,
        tenant_id: str,
        consent_ref: str,
        case_ref: str,
        purpose: str,
        version: str = "1.0",
    ) -> ConsentRecord:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            consent_ref=consent_ref,
            case_ref=case_ref,
            purpose=purpose,
            granted=True,
            version=version,
            granted_at=datetime.now(UTC),
        )

    def revoke(self) -> None:
        self.granted = False
        self.revoked_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "consent_ref": self.consent_ref,
            "case_ref": self.case_ref,
            "purpose": self.purpose,
            "granted": self.granted,
            "version": self.version,
            "granted_at": self.granted_at.isoformat() if self.granted_at else None,
            "revoked_at": self.revoked_at.isoformat() if self.revoked_at else None,
        }


@dataclass(eq=False, kw_only=True)
class LifecycleAuditEntry(AggregateRoot):
    tenant_id: str
    audit_ref: str
    case_ref: str
    action: str
    actor_id: str | None
    details: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def log(
        cls,
        *,
        tenant_id: str,
        audit_ref: str,
        case_ref: str,
        action: str,
        actor_id: str | None,
        details: dict | None = None,
    ) -> LifecycleAuditEntry:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            audit_ref=audit_ref,
            case_ref=case_ref,
            action=action,
            actor_id=actor_id,
            details=details or {},
        )

    def to_dict(self) -> dict:
        return {
            "audit_ref": self.audit_ref,
            "case_ref": self.case_ref,
            "action": self.action,
            "actor_id": self.actor_id,
            "details": self.details,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class LifecycleInvitation(AggregateRoot):
    tenant_id: str
    invitation_ref: str
    case_ref: str
    email: str
    token: str
    expires_at: datetime
    accepted_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def issue(
        cls,
        *,
        tenant_id: str,
        invitation_ref: str,
        case_ref: str,
        email: str,
        token: str,
        expires_at: datetime,
    ) -> LifecycleInvitation:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            invitation_ref=invitation_ref,
            case_ref=case_ref,
            email=email.lower(),
            token=token,
            expires_at=expires_at,
        )

    def accept(self) -> None:
        self.accepted_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "invitation_ref": self.invitation_ref,
            "case_ref": self.case_ref,
            "email": self.email,
            "expires_at": self.expires_at.isoformat(),
            "accepted_at": self.accepted_at.isoformat() if self.accepted_at else None,
            "created_at": self.created_at.isoformat(),
        }
