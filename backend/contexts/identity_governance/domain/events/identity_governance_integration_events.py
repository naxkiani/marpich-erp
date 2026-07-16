"""Enterprise Identity Governance Platform integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent


@dataclass(frozen=True, kw_only=True)
class AccessRequestSubmittedIntegration(IntegrationEvent):
    request_ref: str
    target_user_id: str
    requested_roles: list[str]

    @property
    def event_name(self) -> str:
        return "identity_governance.access_request.submitted"

    @property
    def source_context(self) -> str:
        return "identity_governance"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "request_ref": self.request_ref,
            "target_user_id": self.target_user_id,
            "requested_roles": self.requested_roles,
        }


@dataclass(frozen=True, kw_only=True)
class AccessRequestApprovedIntegration(IntegrationEvent):
    request_ref: str
    approver_id: str

    @property
    def event_name(self) -> str:
        return "identity_governance.access_request.approved"

    @property
    def source_context(self) -> str:
        return "identity_governance"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"request_ref": self.request_ref, "approver_id": self.approver_id}


@dataclass(frozen=True, kw_only=True)
class AccessReviewCompletedIntegration(IntegrationEvent):
    review_ref: str
    findings_count: int

    @property
    def event_name(self) -> str:
        return "identity_governance.access_review.completed"

    @property
    def source_context(self) -> str:
        return "identity_governance"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"review_ref": self.review_ref, "findings_count": self.findings_count}


@dataclass(frozen=True, kw_only=True)
class SodViolationDetectedIntegration(IntegrationEvent):
    request_ref: str
    conflicts: list[dict]

    @property
    def event_name(self) -> str:
        return "identity_governance.sod.violation_detected"

    @property
    def source_context(self) -> str:
        return "identity_governance"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"request_ref": self.request_ref, "conflicts": self.conflicts}


@dataclass(frozen=True, kw_only=True)
class EmergencyAccessGrantedIntegration(IntegrationEvent):
    grant_ref: str
    user_id: str
    incident_ref: str

    @property
    def event_name(self) -> str:
        return "identity_governance.emergency_access.granted"

    @property
    def source_context(self) -> str:
        return "identity_governance"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "grant_ref": self.grant_ref,
            "user_id": self.user_id,
            "incident_ref": self.incident_ref,
        }
