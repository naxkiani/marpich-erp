"""Enterprise KYC Platform aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class DocumentType(StrEnum):
    PASSPORT = "passport"
    NATIONAL_ID = "national_id"
    BUSINESS_REGISTRATION = "business_registration"
    TAX_NUMBER = "tax_number"
    ADDRESS_PROOF = "address_proof"
    OTHER = "other"


class VerificationStatus(StrEnum):
    PENDING = "pending"
    IN_REVIEW = "in_review"
    VERIFIED = "verified"
    REJECTED = "rejected"
    EXPIRED = "expired"


class DueDiligenceLevel(StrEnum):
    STANDARD = "standard"
    ENHANCED = "enhanced"


class RiskClass(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class PepStatus(StrEnum):
    NOT_SCREENED = "not_screened"
    CLEAR = "clear"
    POTENTIAL_MATCH = "potential_match"
    CONFIRMED = "confirmed"


class SanctionsStatus(StrEnum):
    NOT_SCREENED = "not_screened"
    CLEAR = "clear"
    POTENTIAL_MATCH = "potential_match"
    BLOCKED = "blocked"


class KycCaseStatus(StrEnum):
    DRAFT = "draft"
    PENDING_DOCUMENTS = "pending_documents"
    IN_REVIEW = "in_review"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


class ReviewStatus(StrEnum):
    SCHEDULED = "scheduled"
    DUE = "due"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    OVERDUE = "overdue"


class WorkflowApprovalStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class BiometricHookStatus(StrEnum):
    NOT_REQUESTED = "not_requested"
    PENDING = "pending"
    VERIFIED = "verified"
    FAILED = "failed"


KYC_CASE_TRANSITIONS: dict[str, list[str]] = {
    KycCaseStatus.DRAFT.value: [KycCaseStatus.PENDING_DOCUMENTS.value, KycCaseStatus.IN_REVIEW.value],
    KycCaseStatus.PENDING_DOCUMENTS.value: [KycCaseStatus.IN_REVIEW.value],
    KycCaseStatus.IN_REVIEW.value: [
        KycCaseStatus.PENDING_APPROVAL.value,
        KycCaseStatus.APPROVED.value,
        KycCaseStatus.REJECTED.value,
    ],
    KycCaseStatus.PENDING_APPROVAL.value: [KycCaseStatus.APPROVED.value, KycCaseStatus.REJECTED.value],
    KycCaseStatus.APPROVED.value: [KycCaseStatus.EXPIRED.value],
    KycCaseStatus.REJECTED.value: [KycCaseStatus.DRAFT.value],
    KycCaseStatus.EXPIRED.value: [KycCaseStatus.IN_REVIEW.value],
}


@dataclass(eq=False, kw_only=True)
class KycCase(AggregateRoot):
    tenant_id: str
    customer_id: str
    case_ref: str
    status: str = KycCaseStatus.DRAFT.value
    due_diligence_level: str = DueDiligenceLevel.STANDARD.value
    risk_class: str = RiskClass.LOW.value
    pep_status: str = PepStatus.NOT_SCREENED.value
    sanctions_status: str = SanctionsStatus.NOT_SCREENED.value
    identity_verified: bool = False
    address_verified: bool = False
    requires_edd: bool = False
    policy_decisions: dict = field(default_factory=dict)
    organization_id: str | None = None
    branch_id: str | None = None
    assigned_to: str | None = None
    approved_at: datetime | None = None
    approved_by: str | None = None
    expires_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        customer_id: str,
        case_ref: str,
        due_diligence_level: str = DueDiligenceLevel.STANDARD.value,
        organization_id: str | None = None,
        branch_id: str | None = None,
    ) -> KycCase:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            customer_id=customer_id,
            case_ref=case_ref.strip().upper(),
            due_diligence_level=due_diligence_level,
            organization_id=organization_id,
            branch_id=branch_id,
        )

    def transition(self, new_status: str) -> None:
        KycCaseStatus(new_status)
        allowed = KYC_CASE_TRANSITIONS.get(self.status, [])
        if new_status not in allowed:
            raise ValueError("invalid_case_transition")
        self.status = new_status
        self.updated_at = datetime.now(UTC)

    def apply_risk_classification(self, *, risk_class: str, requires_edd: bool) -> None:
        RiskClass(risk_class)
        self.risk_class = risk_class
        self.requires_edd = requires_edd
        if requires_edd:
            self.due_diligence_level = DueDiligenceLevel.ENHANCED.value
        self.updated_at = datetime.now(UTC)

    def apply_pep_screening(self, status: str) -> None:
        PepStatus(status)
        self.pep_status = status
        if status in {PepStatus.POTENTIAL_MATCH.value, PepStatus.CONFIRMED.value}:
            self.requires_edd = True
            self.due_diligence_level = DueDiligenceLevel.ENHANCED.value
        self.updated_at = datetime.now(UTC)

    def apply_sanctions_screening(self, status: str) -> None:
        SanctionsStatus(status)
        self.sanctions_status = status
        self.updated_at = datetime.now(UTC)

    def mark_identity_verified(self) -> None:
        self.identity_verified = True
        self.updated_at = datetime.now(UTC)

    def mark_address_verified(self) -> None:
        self.address_verified = True
        self.updated_at = datetime.now(UTC)

    def submit_for_approval(self) -> None:
        if self.status != KycCaseStatus.IN_REVIEW.value:
            raise ValueError("not_in_review")
        self.status = KycCaseStatus.PENDING_APPROVAL.value
        self.updated_at = datetime.now(UTC)

    def approve(self, *, approved_by: str, review_interval_days: int = 365) -> None:
        if self.status != KycCaseStatus.PENDING_APPROVAL.value:
            raise ValueError("not_pending_approval")
        if self.sanctions_status == SanctionsStatus.BLOCKED.value:
            raise ValueError("sanctions_blocked")
        self.status = KycCaseStatus.APPROVED.value
        self.approved_at = datetime.now(UTC)
        self.approved_by = approved_by
        self.expires_at = datetime.now(UTC) + timedelta(days=review_interval_days)
        self.updated_at = datetime.now(UTC)

    def reject(self, *, reason: str = "") -> None:
        if self.status != KycCaseStatus.PENDING_APPROVAL.value:
            raise ValueError("not_pending_approval")
        self.status = KycCaseStatus.REJECTED.value
        self.updated_at = datetime.now(UTC)

    def record_policy_decision(self, policy_key: str, decision: dict) -> None:
        self.policy_decisions[policy_key] = decision
        self.updated_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "customer_id": self.customer_id,
            "case_ref": self.case_ref,
            "status": self.status,
            "due_diligence_level": self.due_diligence_level,
            "risk_class": self.risk_class,
            "pep_status": self.pep_status,
            "sanctions_status": self.sanctions_status,
            "identity_verified": self.identity_verified,
            "address_verified": self.address_verified,
            "requires_edd": self.requires_edd,
            "policy_decisions": self.policy_decisions,
            "organization_id": self.organization_id,
            "branch_id": self.branch_id,
            "assigned_to": self.assigned_to,
            "approved_at": self.approved_at.isoformat() if self.approved_at else None,
            "approved_by": self.approved_by,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class KycDocument(AggregateRoot):
    tenant_id: str
    case_id: str
    customer_id: str
    document_type: str
    document_ref: str
    issuing_country: str = ""
    expiry_date: str | None = None
    verification_status: str = VerificationStatus.PENDING.value
    verified_at: datetime | None = None
    verified_by: str | None = None
    rejection_reason: str = ""
    metadata: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        case_id: str,
        customer_id: str,
        document_type: str,
        document_ref: str,
        issuing_country: str = "",
        expiry_date: str | None = None,
        metadata: dict | None = None,
    ) -> KycDocument:
        DocumentType(document_type)
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            case_id=case_id,
            customer_id=customer_id,
            document_type=document_type,
            document_ref=document_ref.strip(),
            issuing_country=issuing_country.strip().upper(),
            expiry_date=expiry_date,
            metadata=metadata or {},
        )

    def verify(self, *, verified_by: str) -> None:
        self.verification_status = VerificationStatus.VERIFIED.value
        self.verified_at = datetime.now(UTC)
        self.verified_by = verified_by

    def reject(self, *, reason: str) -> None:
        self.verification_status = VerificationStatus.REJECTED.value
        self.rejection_reason = reason

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "case_id": self.case_id,
            "customer_id": self.customer_id,
            "document_type": self.document_type,
            "document_ref": self.document_ref,
            "issuing_country": self.issuing_country,
            "expiry_date": self.expiry_date,
            "verification_status": self.verification_status,
            "verified_at": self.verified_at.isoformat() if self.verified_at else None,
            "verified_by": self.verified_by,
            "rejection_reason": self.rejection_reason,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class KycAddressVerification(AggregateRoot):
    tenant_id: str
    case_id: str
    customer_id: str
    address_line: str
    city: str
    country: str
    postal_code: str = ""
    verification_status: str = VerificationStatus.PENDING.value
    verified_at: datetime | None = None
    verified_by: str | None = None
    proof_document_id: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        case_id: str,
        customer_id: str,
        address_line: str,
        city: str,
        country: str,
        postal_code: str = "",
        proof_document_id: str | None = None,
    ) -> KycAddressVerification:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            case_id=case_id,
            customer_id=customer_id,
            address_line=address_line.strip(),
            city=city.strip(),
            country=country.strip().upper(),
            postal_code=postal_code.strip(),
            proof_document_id=proof_document_id,
        )

    def verify(self, *, verified_by: str) -> None:
        self.verification_status = VerificationStatus.VERIFIED.value
        self.verified_at = datetime.now(UTC)
        self.verified_by = verified_by

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "case_id": self.case_id,
            "customer_id": self.customer_id,
            "address_line": self.address_line,
            "city": self.city,
            "country": self.country,
            "postal_code": self.postal_code,
            "verification_status": self.verification_status,
            "verified_at": self.verified_at.isoformat() if self.verified_at else None,
            "verified_by": self.verified_by,
            "proof_document_id": self.proof_document_id,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class KycScreeningResult(AggregateRoot):
    tenant_id: str
    case_id: str
    customer_id: str
    screening_type: str
    provider_ref: str = ""
    status: str
    match_score: float = 0.0
    match_details: dict = field(default_factory=dict)
    screened_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    screened_by: str | None = None

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        case_id: str,
        customer_id: str,
        screening_type: str,
        status: str,
        provider_ref: str = "",
        match_score: float = 0.0,
        match_details: dict | None = None,
        screened_by: str | None = None,
    ) -> KycScreeningResult:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            case_id=case_id,
            customer_id=customer_id,
            screening_type=screening_type,
            status=status,
            provider_ref=provider_ref,
            match_score=round(match_score, 4),
            match_details=match_details or {},
            screened_by=screened_by,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "case_id": self.case_id,
            "customer_id": self.customer_id,
            "screening_type": self.screening_type,
            "provider_ref": self.provider_ref,
            "status": self.status,
            "match_score": self.match_score,
            "match_details": self.match_details,
            "screened_at": self.screened_at.isoformat(),
            "screened_by": self.screened_by,
        }


@dataclass(eq=False, kw_only=True)
class KycPeriodicReview(AggregateRoot):
    tenant_id: str
    case_id: str
    customer_id: str
    review_ref: str
    status: str = ReviewStatus.SCHEDULED.value
    due_date: datetime
    completed_at: datetime | None = None
    completed_by: str | None = None
    outcome: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        case_id: str,
        customer_id: str,
        review_ref: str,
        due_date: datetime,
    ) -> KycPeriodicReview:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            case_id=case_id,
            customer_id=customer_id,
            review_ref=review_ref.strip().upper(),
            due_date=due_date,
        )

    def start(self) -> None:
        self.status = ReviewStatus.IN_PROGRESS.value

    def complete(self, *, completed_by: str, outcome: str) -> None:
        self.status = ReviewStatus.COMPLETED.value
        self.completed_at = datetime.now(UTC)
        self.completed_by = completed_by
        self.outcome = outcome

    def mark_overdue(self) -> None:
        if self.status in {ReviewStatus.SCHEDULED.value, ReviewStatus.DUE.value}:
            self.status = ReviewStatus.OVERDUE.value

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "case_id": self.case_id,
            "customer_id": self.customer_id,
            "review_ref": self.review_ref,
            "status": self.status,
            "due_date": self.due_date.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "completed_by": self.completed_by,
            "outcome": self.outcome,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class KycWorkflowRequest(AggregateRoot):
    tenant_id: str
    case_id: str
    customer_id: str
    request_type: str
    status: str = WorkflowApprovalStatus.PENDING.value
    required_levels: int = 1
    approved_levels: int = 0
    approver_id: str | None = None
    rejection_reason: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    resolved_at: datetime | None = None

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        case_id: str,
        customer_id: str,
        request_type: str,
        required_levels: int = 1,
    ) -> KycWorkflowRequest:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            case_id=case_id,
            customer_id=customer_id,
            request_type=request_type,
            required_levels=required_levels,
        )

    def approve(self, *, approver_id: str) -> None:
        if self.status != WorkflowApprovalStatus.PENDING.value:
            raise ValueError("not_pending")
        self.approved_levels += 1
        self.approver_id = approver_id
        if self.approved_levels >= self.required_levels:
            self.status = WorkflowApprovalStatus.APPROVED.value
            self.resolved_at = datetime.now(UTC)

    def reject(self, *, approver_id: str, reason: str = "") -> None:
        if self.status != WorkflowApprovalStatus.PENDING.value:
            raise ValueError("not_pending")
        self.status = WorkflowApprovalStatus.REJECTED.value
        self.approver_id = approver_id
        self.rejection_reason = reason
        self.resolved_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "case_id": self.case_id,
            "customer_id": self.customer_id,
            "request_type": self.request_type,
            "status": self.status,
            "required_levels": self.required_levels,
            "approved_levels": self.approved_levels,
            "approver_id": self.approver_id,
            "rejection_reason": self.rejection_reason,
            "created_at": self.created_at.isoformat(),
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
        }


@dataclass(eq=False, kw_only=True)
class KycBiometricHook(AggregateRoot):
    tenant_id: str
    case_id: str
    customer_id: str
    provider: str
    hook_ref: str
    status: str = BiometricHookStatus.NOT_REQUESTED.value
    callback_url: str = ""
    result_payload: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    completed_at: datetime | None = None

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        case_id: str,
        customer_id: str,
        provider: str,
        hook_ref: str,
        callback_url: str = "",
    ) -> KycBiometricHook:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            case_id=case_id,
            customer_id=customer_id,
            provider=provider.strip(),
            hook_ref=hook_ref.strip(),
            callback_url=callback_url,
            status=BiometricHookStatus.PENDING.value,
        )

    def complete(self, *, status: str, result_payload: dict) -> None:
        BiometricHookStatus(status)
        self.status = status
        self.result_payload = result_payload
        self.completed_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "case_id": self.case_id,
            "customer_id": self.customer_id,
            "provider": self.provider,
            "hook_ref": self.hook_ref,
            "status": self.status,
            "callback_url": self.callback_url,
            "result_payload": self.result_payload,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }


@dataclass(eq=False, kw_only=True)
class KycAuditEntry(AggregateRoot):
    tenant_id: str
    case_id: str
    action: str
    actor_id: str | None
    detail: str
    sensitivity: str = "high"
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        case_id: str,
        action: str,
        actor_id: str | None = None,
        detail: str = "",
        sensitivity: str = "high",
    ) -> KycAuditEntry:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            case_id=case_id,
            action=action,
            actor_id=actor_id,
            detail=detail,
            sensitivity=sensitivity,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "case_id": self.case_id,
            "action": self.action,
            "actor_id": self.actor_id,
            "detail": self.detail,
            "sensitivity": self.sensitivity,
            "occurred_at": self.occurred_at.isoformat(),
        }
