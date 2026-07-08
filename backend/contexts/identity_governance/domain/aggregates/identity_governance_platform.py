"""Enterprise Identity Governance Platform aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class IdentityGovernanceCapability(StrEnum):
    USER_LIFECYCLE = "user_lifecycle"
    ROLE_LIFECYCLE = "role_lifecycle"
    ACCESS_REQUEST = "access_request"
    ACCESS_REVIEW = "access_review"
    PRIVILEGE_REVIEW = "privilege_review"
    SEGREGATION_OF_DUTIES = "segregation_of_duties"
    TEMPORARY_ACCESS = "temporary_access"
    EMERGENCY_ACCESS = "emergency_access"
    CERTIFICATION = "certification"
    APPROVAL = "approval"
    AUDIT = "audit"
    IDENTITY_DASHBOARD = "identity_dashboard"


class RequestStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


class ReviewStatus(StrEnum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class CertificationStatus(StrEnum):
    PENDING = "pending"
    CERTIFIED = "certified"
    REVOKED = "revoked"


class AccessGrantStatus(StrEnum):
    ACTIVE = "active"
    EXPIRED = "expired"
    REVOKED = "revoked"


@dataclass(eq=False, kw_only=True)
class IdentityGovernanceProfile(AggregateRoot):
    tenant_id: str
    profile_ref: str
    access_review_frequency_days: int = 90
    certification_required: bool = True
    sod_enforcement: bool = True
    temporary_access_max_hours: int = 72
    emergency_access_max_hours: int = 4
    metadata: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(cls, *, tenant_id: str, profile_ref: str, metadata: dict | None = None) -> IdentityGovernanceProfile:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            profile_ref=profile_ref,
            metadata=metadata or {},
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "profile_ref": self.profile_ref,
            "tenant_id": self.tenant_id,
            "access_review_frequency_days": self.access_review_frequency_days,
            "certification_required": self.certification_required,
            "sod_enforcement": self.sod_enforcement,
            "temporary_access_max_hours": self.temporary_access_max_hours,
            "emergency_access_max_hours": self.emergency_access_max_hours,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class AccessRequest(AggregateRoot):
    tenant_id: str
    request_ref: str
    requester_id: str
    target_user_id: str
    requested_roles: list[str]
    justification: str
    status: str
    approver_id: str = ""
    sod_checked: bool = False
    sod_valid: bool = True
    metadata: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def submit(
        cls,
        *,
        tenant_id: str,
        request_ref: str,
        requester_id: str,
        target_user_id: str,
        requested_roles: list[str],
        justification: str,
        sod_valid: bool = True,
        metadata: dict | None = None,
    ) -> AccessRequest:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            request_ref=request_ref,
            requester_id=requester_id,
            target_user_id=target_user_id,
            requested_roles=requested_roles,
            justification=justification,
            status=RequestStatus.PENDING.value,
            sod_checked=True,
            sod_valid=sod_valid,
            metadata=metadata or {},
        )

    def approve(self, approver_id: str) -> None:
        self.status = RequestStatus.APPROVED.value
        self.approver_id = approver_id
        self.updated_at = datetime.now(UTC)

    def reject(self, approver_id: str) -> None:
        self.status = RequestStatus.REJECTED.value
        self.approver_id = approver_id
        self.updated_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "request_ref": self.request_ref,
            "tenant_id": self.tenant_id,
            "requester_id": self.requester_id,
            "target_user_id": self.target_user_id,
            "requested_roles": self.requested_roles,
            "justification": self.justification,
            "status": self.status,
            "approver_id": self.approver_id,
            "sod_checked": self.sod_checked,
            "sod_valid": self.sod_valid,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class AccessReview(AggregateRoot):
    tenant_id: str
    review_ref: str
    title: str
    reviewer_id: str
    scope_user_ids: list[str] = field(default_factory=list)
    status: str
    findings: list[dict] = field(default_factory=list)
    completed_at: str | None = None
    metadata: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def schedule(
        cls,
        *,
        tenant_id: str,
        review_ref: str,
        title: str,
        reviewer_id: str,
        scope_user_ids: list[str],
        metadata: dict | None = None,
    ) -> AccessReview:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            review_ref=review_ref,
            title=title,
            reviewer_id=reviewer_id,
            scope_user_ids=scope_user_ids,
            status=ReviewStatus.SCHEDULED.value,
            metadata=metadata or {},
        )

    def start(self) -> None:
        self.status = ReviewStatus.IN_PROGRESS.value

    def complete(self, findings: list[dict]) -> None:
        self.status = ReviewStatus.COMPLETED.value
        self.findings = findings
        self.completed_at = datetime.now(UTC).isoformat()

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "review_ref": self.review_ref,
            "tenant_id": self.tenant_id,
            "title": self.title,
            "reviewer_id": self.reviewer_id,
            "scope_user_ids": self.scope_user_ids,
            "status": self.status,
            "findings": self.findings,
            "completed_at": self.completed_at,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class PrivilegeCertification(AggregateRoot):
    tenant_id: str
    certification_ref: str
    user_id: str
    role_ids: list[str]
    certifier_id: str
    status: str
    notes: str = ""
    certified_at: str | None = None
    metadata: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def initiate(
        cls,
        *,
        tenant_id: str,
        certification_ref: str,
        user_id: str,
        role_ids: list[str],
        certifier_id: str = "",
        metadata: dict | None = None,
    ) -> PrivilegeCertification:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            certification_ref=certification_ref,
            user_id=user_id,
            role_ids=role_ids,
            certifier_id=certifier_id,
            status=CertificationStatus.PENDING.value,
            metadata=metadata or {},
        )

    def certify(self, certifier_id: str, notes: str = "") -> None:
        self.status = CertificationStatus.CERTIFIED.value
        self.certifier_id = certifier_id
        self.notes = notes
        self.certified_at = datetime.now(UTC).isoformat()

    def revoke(self, certifier_id: str, notes: str = "") -> None:
        self.status = CertificationStatus.REVOKED.value
        self.certifier_id = certifier_id
        self.notes = notes

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "certification_ref": self.certification_ref,
            "tenant_id": self.tenant_id,
            "user_id": self.user_id,
            "role_ids": self.role_ids,
            "certifier_id": self.certifier_id,
            "status": self.status,
            "notes": self.notes,
            "certified_at": self.certified_at,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class TemporaryAccessGrant(AggregateRoot):
    tenant_id: str
    grant_ref: str
    user_id: str
    roles: list[str]
    granted_by: str
    expires_at: str
    status: str
    justification: str = ""
    metadata: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def grant(
        cls,
        *,
        tenant_id: str,
        grant_ref: str,
        user_id: str,
        roles: list[str],
        granted_by: str,
        expires_at: str,
        justification: str = "",
        metadata: dict | None = None,
    ) -> TemporaryAccessGrant:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            grant_ref=grant_ref,
            user_id=user_id,
            roles=roles,
            granted_by=granted_by,
            expires_at=expires_at,
            status=AccessGrantStatus.ACTIVE.value,
            justification=justification,
            metadata=metadata or {},
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "grant_ref": self.grant_ref,
            "tenant_id": self.tenant_id,
            "user_id": self.user_id,
            "roles": self.roles,
            "granted_by": self.granted_by,
            "expires_at": self.expires_at,
            "status": self.status,
            "justification": self.justification,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class EmergencyAccessGrant(AggregateRoot):
    tenant_id: str
    grant_ref: str
    user_id: str
    roles: list[str]
    granted_by: str
    expires_at: str
    status: str
    incident_ref: str = ""
    justification: str = ""
    metadata: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def grant(
        cls,
        *,
        tenant_id: str,
        grant_ref: str,
        user_id: str,
        roles: list[str],
        granted_by: str,
        expires_at: str,
        incident_ref: str = "",
        justification: str = "",
        metadata: dict | None = None,
    ) -> EmergencyAccessGrant:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            grant_ref=grant_ref,
            user_id=user_id,
            roles=roles,
            granted_by=granted_by,
            expires_at=expires_at,
            status=AccessGrantStatus.ACTIVE.value,
            incident_ref=incident_ref,
            justification=justification,
            metadata=metadata or {},
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "grant_ref": self.grant_ref,
            "tenant_id": self.tenant_id,
            "user_id": self.user_id,
            "roles": self.roles,
            "granted_by": self.granted_by,
            "expires_at": self.expires_at,
            "status": self.status,
            "incident_ref": self.incident_ref,
            "justification": self.justification,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class GovernanceAuditEntry(AggregateRoot):
    tenant_id: str
    entry_ref: str
    action: str
    actor_id: str
    resource_type: str
    resource_ref: str
    details: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def record(
        cls,
        *,
        tenant_id: str,
        entry_ref: str,
        action: str,
        actor_id: str,
        resource_type: str,
        resource_ref: str,
        details: dict | None = None,
    ) -> GovernanceAuditEntry:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            entry_ref=entry_ref,
            action=action,
            actor_id=actor_id,
            resource_type=resource_type,
            resource_ref=resource_ref,
            details=details or {},
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "entry_ref": self.entry_ref,
            "tenant_id": self.tenant_id,
            "action": self.action,
            "actor_id": self.actor_id,
            "resource_type": self.resource_type,
            "resource_ref": self.resource_ref,
            "details": self.details,
            "created_at": self.created_at.isoformat(),
        }
