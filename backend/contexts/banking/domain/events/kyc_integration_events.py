"""Enterprise KYC integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent


@dataclass(frozen=True, kw_only=True)
class KycCaseOpenedIntegration(IntegrationEvent):
    case_id: str
    customer_id: str
    case_ref: str
    due_diligence_level: str

    @property
    def event_name(self) -> str:
        return "banking.kyc.case.opened"

    @property
    def source_context(self) -> str:
        return "banking"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "case_id": self.case_id,
            "customer_id": self.customer_id,
            "case_ref": self.case_ref,
            "due_diligence_level": self.due_diligence_level,
        }


@dataclass(frozen=True, kw_only=True)
class KycCaseApprovedIntegration(IntegrationEvent):
    case_id: str
    customer_id: str
    risk_class: str
    due_diligence_level: str
    approved_by: str

    @property
    def event_name(self) -> str:
        return "banking.kyc.case.approved"

    @property
    def source_context(self) -> str:
        return "banking"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "case_id": self.case_id,
            "customer_id": self.customer_id,
            "risk_class": self.risk_class,
            "due_diligence_level": self.due_diligence_level,
            "approved_by": self.approved_by,
        }


@dataclass(frozen=True, kw_only=True)
class KycPepFlagRaisedIntegration(IntegrationEvent):
    case_id: str
    customer_id: str
    pep_status: str
    match_score: float

    @property
    def event_name(self) -> str:
        return "banking.kyc.pep.flagged"

    @property
    def source_context(self) -> str:
        return "banking"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "case_id": self.case_id,
            "customer_id": self.customer_id,
            "pep_status": self.pep_status,
            "match_score": self.match_score,
        }


@dataclass(frozen=True, kw_only=True)
class KycSanctionsHitIntegration(IntegrationEvent):
    case_id: str
    customer_id: str
    sanctions_status: str
    match_score: float

    @property
    def event_name(self) -> str:
        return "banking.kyc.sanctions.hit"

    @property
    def source_context(self) -> str:
        return "banking"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "case_id": self.case_id,
            "customer_id": self.customer_id,
            "sanctions_status": self.sanctions_status,
            "match_score": self.match_score,
        }


@dataclass(frozen=True, kw_only=True)
class KycPeriodicReviewDueIntegration(IntegrationEvent):
    case_id: str
    customer_id: str
    review_id: str
    due_date: str

    @property
    def event_name(self) -> str:
        return "banking.kyc.review.due"

    @property
    def source_context(self) -> str:
        return "banking"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "case_id": self.case_id,
            "customer_id": self.customer_id,
            "review_id": self.review_id,
            "due_date": self.due_date,
        }


@dataclass(frozen=True, kw_only=True)
class KycBiometricHookRequestedIntegration(IntegrationEvent):
    case_id: str
    customer_id: str
    hook_id: str
    provider: str
    callback_url: str

    @property
    def event_name(self) -> str:
        return "banking.kyc.biometric.requested"

    @property
    def source_context(self) -> str:
        return "banking"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "case_id": self.case_id,
            "customer_id": self.customer_id,
            "hook_id": self.hook_id,
            "provider": self.provider,
            "callback_url": self.callback_url,
        }
