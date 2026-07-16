"""Identity registration & onboarding aggregates (P201-A)."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class IdentityType(StrEnum):
    EMPLOYEE = "employee"
    CUSTOMER = "customer"
    CITIZEN = "citizen"
    STUDENT = "student"
    TEACHER = "teacher"
    VENDOR = "vendor"
    SUPPLIER = "supplier"
    PARTNER = "partner"
    CONTRACTOR = "contractor"
    GUEST = "guest"
    ORGANIZATION = "organization"
    DEPARTMENT = "department"
    API_CLIENT = "api_client"
    MACHINE = "machine"
    DEVICE = "device"
    SERVICE_ACCOUNT = "service_account"
    KUBERNETES_WORKLOAD = "kubernetes_workload"
    AI_AGENT = "ai_agent"
    DIGITAL_TWIN = "digital_twin"


SUPPORTED_IDENTITY_TYPES: frozenset[str] = frozenset(t.value for t in IdentityType)


class RegistrationChannel(StrEnum):
    WEB_PORTAL = "web_portal"
    MOBILE_APP = "mobile_app"
    REST_API = "rest_api"
    GRAPHQL_API = "graphql_api"
    SCIM = "scim"
    LDAP = "ldap"
    ACTIVE_DIRECTORY = "active_directory"
    HR_SYSTEM = "hr_system"
    ERP_SYSTEM = "erp_system"
    CRM_SYSTEM = "crm_system"
    PARTNER_SYSTEM = "partner_system"
    BULK_IMPORT = "bulk_import"
    CSV_IMPORT = "csv_import"
    EVENT_DRIVEN = "event_driven"


class RegistrationStatus(StrEnum):
    REQUESTED = "requested"
    PENDING_VALIDATION = "pending_validation"
    VALIDATED = "validated"
    DUPLICATE_REVIEW = "duplicate_review"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    PROFILE_INITIALIZED = "profile_initialized"
    ONBOARDING = "onboarding"
    PROVISIONING_REQUESTED = "provisioning_requested"
    ACTIVATION_REQUESTED = "activation_requested"


class ApprovalMode(StrEnum):
    AUTOMATIC = "automatic"
    MANUAL = "manual"
    MULTI_LEVEL = "multi_level"
    DEPARTMENT = "department"
    HR = "hr"
    SECURITY = "security"
    RISK_BASED = "risk_based"
    AI_ASSISTED = "ai_assisted"


@dataclass(eq=False, kw_only=True)
class IdentityRegistration(AggregateRoot):
    tenant_id: str
    registration_ref: str
    identity_type: str
    channel: str
    email: str
    display_name: str
    status: str = RegistrationStatus.REQUESTED.value
    source: str = "api"
    method: str = "self_registration"
    national_id: str = ""
    employee_number: str = ""
    phone: str = ""
    organization_ref: str = ""
    case_ref: str | None = None
    risk_score: float = 0.0
    trust_level: str = "unknown"
    validation_errors: list[str] = field(default_factory=list)
    duplicate_matches: list[dict] = field(default_factory=list)
    profile: dict = field(default_factory=dict)
    onboarding: dict = field(default_factory=dict)
    approval_mode: str = ApprovalMode.AUTOMATIC.value
    approved_by: str | None = None
    rejected_reason: str = ""
    zt_context: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def request(
        cls,
        *,
        tenant_id: str,
        registration_ref: str,
        identity_type: str,
        channel: str,
        email: str,
        display_name: str,
        source: str = "api",
        method: str = "self_registration",
        national_id: str = "",
        employee_number: str = "",
        phone: str = "",
        organization_ref: str = "",
        approval_mode: str = ApprovalMode.AUTOMATIC.value,
        zt_context: dict | None = None,
        metadata: dict | None = None,
    ) -> IdentityRegistration:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            registration_ref=registration_ref,
            identity_type=identity_type,
            channel=channel,
            email=email.lower().strip(),
            display_name=display_name.strip(),
            source=source,
            method=method,
            national_id=national_id,
            employee_number=employee_number,
            phone=phone,
            organization_ref=organization_ref,
            approval_mode=approval_mode,
            zt_context=dict(zt_context or {}),
            metadata=dict(metadata or {}),
            status=RegistrationStatus.REQUESTED.value,
        )

    def touch(self, status: str | None = None) -> None:
        if status:
            self.status = status
        self.updated_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "registration_ref": self.registration_ref,
            "tenant_id": self.tenant_id,
            "identity_type": self.identity_type,
            "channel": self.channel,
            "email": self.email,
            "display_name": self.display_name,
            "status": self.status,
            "source": self.source,
            "method": self.method,
            "national_id": self.national_id,
            "employee_number": self.employee_number,
            "phone": self.phone,
            "organization_ref": self.organization_ref,
            "case_ref": self.case_ref,
            "risk_score": self.risk_score,
            "trust_level": self.trust_level,
            "validation_errors": list(self.validation_errors),
            "duplicate_matches": list(self.duplicate_matches),
            "profile": dict(self.profile),
            "onboarding": dict(self.onboarding),
            "approval_mode": self.approval_mode,
            "approved_by": self.approved_by,
            "rejected_reason": self.rejected_reason,
            "zt_context": dict(self.zt_context),
            "metadata": dict(self.metadata),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
