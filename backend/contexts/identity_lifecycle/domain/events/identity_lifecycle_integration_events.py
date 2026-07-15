"""Identity lifecycle integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent


@dataclass(frozen=True, kw_only=True)
class LifecycleCaseOpenedIntegration(IntegrationEvent):
    case_ref: str
    identity_ref: str
    email: str

    @property
    def event_name(self) -> str:
        return "identity_lifecycle.case.opened"

    @property
    def source_context(self) -> str:
        return "identity_lifecycle"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"case_ref": self.case_ref, "identity_ref": self.identity_ref, "email": self.email}


@dataclass(frozen=True, kw_only=True)
class LifecycleStateChangedIntegration(IntegrationEvent):
    case_ref: str
    action: str
    from_state: str
    to_state: str

    @property
    def event_name(self) -> str:
        return "identity_lifecycle.state.changed"

    @property
    def source_context(self) -> str:
        return "identity_lifecycle"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "case_ref": self.case_ref,
            "action": self.action,
            "from_state": self.from_state,
            "to_state": self.to_state,
        }


@dataclass(frozen=True, kw_only=True)
class LifecycleVerificationCompletedIntegration(IntegrationEvent):
    case_ref: str
    verification_type: str
    status: str

    @property
    def event_name(self) -> str:
        return "identity_lifecycle.verification.completed"

    @property
    def source_context(self) -> str:
        return "identity_lifecycle"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "case_ref": self.case_ref,
            "verification_type": self.verification_type,
            "status": self.status,
        }


@dataclass(frozen=True, kw_only=True)
class LifecycleConsentRecordedIntegration(IntegrationEvent):
    case_ref: str
    purpose: str
    granted: bool

    @property
    def event_name(self) -> str:
        return "identity_lifecycle.consent.recorded"

    @property
    def source_context(self) -> str:
        return "identity_lifecycle"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"case_ref": self.case_ref, "purpose": self.purpose, "granted": self.granted}


@dataclass(frozen=True, kw_only=True)
class LifecycleIdentityDeletedIntegration(IntegrationEvent):
    case_ref: str
    deletion_type: str

    @property
    def event_name(self) -> str:
        return "identity_lifecycle.identity.deleted"

    @property
    def source_context(self) -> str:
        return "identity_lifecycle"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"case_ref": self.case_ref, "deletion_type": self.deletion_type}


@dataclass(frozen=True, kw_only=True)
class LifecycleRegistrationRequestedIntegration(IntegrationEvent):
    registration_ref: str
    identity_type: str
    email: str

    @property
    def event_name(self) -> str:
        return "identity_lifecycle.registration.requested"

    @property
    def source_context(self) -> str:
        return "identity_lifecycle"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "registration_ref": self.registration_ref,
            "identity_type": self.identity_type,
            "email": self.email,
        }


@dataclass(frozen=True, kw_only=True)
class LifecycleRegistrationValidatedIntegration(IntegrationEvent):
    registration_ref: str

    @property
    def event_name(self) -> str:
        return "identity_lifecycle.registration.validated"

    @property
    def source_context(self) -> str:
        return "identity_lifecycle"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"registration_ref": self.registration_ref}


@dataclass(frozen=True, kw_only=True)
class LifecycleRegistrationDuplicateDetectedIntegration(IntegrationEvent):
    registration_ref: str
    match_count: int

    @property
    def event_name(self) -> str:
        return "identity_lifecycle.registration.duplicate_detected"

    @property
    def source_context(self) -> str:
        return "identity_lifecycle"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "registration_ref": self.registration_ref,
            "match_count": self.match_count,
        }


@dataclass(frozen=True, kw_only=True)
class LifecycleRegistrationApprovedIntegration(IntegrationEvent):
    registration_ref: str
    case_ref: str
    approved_by: str

    @property
    def event_name(self) -> str:
        return "identity_lifecycle.registration.approved"

    @property
    def source_context(self) -> str:
        return "identity_lifecycle"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "registration_ref": self.registration_ref,
            "case_ref": self.case_ref,
            "approved_by": self.approved_by,
        }


@dataclass(frozen=True, kw_only=True)
class LifecycleRegistrationRejectedIntegration(IntegrationEvent):
    registration_ref: str
    reason: str

    @property
    def event_name(self) -> str:
        return "identity_lifecycle.registration.rejected"

    @property
    def source_context(self) -> str:
        return "identity_lifecycle"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "registration_ref": self.registration_ref,
            "reason": self.reason,
        }


@dataclass(frozen=True, kw_only=True)
class LifecycleIdentityCreatedIntegration(IntegrationEvent):
    registration_ref: str
    case_ref: str
    identity_type: str

    @property
    def event_name(self) -> str:
        return "identity_lifecycle.identity.created"

    @property
    def source_context(self) -> str:
        return "identity_lifecycle"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "registration_ref": self.registration_ref,
            "case_ref": self.case_ref,
            "identity_type": self.identity_type,
        }


@dataclass(frozen=True, kw_only=True)
class LifecycleProfileInitializedIntegration(IntegrationEvent):
    registration_ref: str

    @property
    def event_name(self) -> str:
        return "identity_lifecycle.profile.initialized"

    @property
    def source_context(self) -> str:
        return "identity_lifecycle"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"registration_ref": self.registration_ref}


@dataclass(frozen=True, kw_only=True)
class LifecycleOnboardingStartedIntegration(IntegrationEvent):
    registration_ref: str

    @property
    def event_name(self) -> str:
        return "identity_lifecycle.onboarding.started"

    @property
    def source_context(self) -> str:
        return "identity_lifecycle"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"registration_ref": self.registration_ref}


@dataclass(frozen=True, kw_only=True)
class LifecycleProvisioningRequestedIntegration(IntegrationEvent):
    registration_ref: str
    case_ref: str
    identity_type: str

    @property
    def event_name(self) -> str:
        return "identity_lifecycle.provisioning.requested"

    @property
    def source_context(self) -> str:
        return "identity_lifecycle"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "registration_ref": self.registration_ref,
            "case_ref": self.case_ref,
            "identity_type": self.identity_type,
        }


@dataclass(frozen=True, kw_only=True)
class LifecycleWelcomeGeneratedIntegration(IntegrationEvent):
    registration_ref: str

    @property
    def event_name(self) -> str:
        return "identity_lifecycle.welcome.generated"

    @property
    def source_context(self) -> str:
        return "identity_lifecycle"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"registration_ref": self.registration_ref}


@dataclass(frozen=True, kw_only=True)
class LifecycleActivationRequestedIntegration(IntegrationEvent):
    registration_ref: str
    case_ref: str

    @property
    def event_name(self) -> str:
        return "identity_lifecycle.activation.requested"

    @property
    def source_context(self) -> str:
        return "identity_lifecycle"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "registration_ref": self.registration_ref,
            "case_ref": self.case_ref,
        }
