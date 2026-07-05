"""Banking Security Platform integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent


@dataclass(frozen=True, kw_only=True)
class BankingSecurityApprovalSubmittedIntegration(IntegrationEvent):
    request_id: str
    request_ref: str
    action_type: str
    maker_id: str

    @property
    def event_name(self) -> str:
        return "banking.security.approval.submitted"

    @property
    def source_context(self) -> str:
        return "banking"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "request_id": self.request_id,
            "request_ref": self.request_ref,
            "action_type": self.action_type,
            "maker_id": self.maker_id,
        }


@dataclass(frozen=True, kw_only=True)
class BankingSecurityApprovalCompletedIntegration(IntegrationEvent):
    request_id: str
    request_ref: str
    status: str
    approvers: list[str]

    @property
    def event_name(self) -> str:
        return "banking.security.approval.completed"

    @property
    def source_context(self) -> str:
        return "banking"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "request_id": self.request_id,
            "request_ref": self.request_ref,
            "status": self.status,
            "approvers": self.approvers,
        }


@dataclass(frozen=True, kw_only=True)
class BankingSecurityFreezeActivatedIntegration(IntegrationEvent):
    freeze_id: str
    freeze_ref: str
    scope: str
    activated_by: str

    @property
    def event_name(self) -> str:
        return "banking.security.freeze.activated"

    @property
    def source_context(self) -> str:
        return "banking"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "freeze_id": self.freeze_id,
            "freeze_ref": self.freeze_ref,
            "scope": self.scope,
            "activated_by": self.activated_by,
        }


@dataclass(frozen=True, kw_only=True)
class BankingSecurityAlertRaisedIntegration(IntegrationEvent):
    alert_id: str
    alert_ref: str
    action_type: str
    risk_score: float

    @property
    def event_name(self) -> str:
        return "banking.security.alert.raised"

    @property
    def source_context(self) -> str:
        return "banking"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "alert_id": self.alert_id,
            "alert_ref": self.alert_ref,
            "action_type": self.action_type,
            "risk_score": self.risk_score,
        }


@dataclass(frozen=True, kw_only=True)
class BankingSecurityAuditRecordedIntegration(IntegrationEvent):
    audit_id: str
    action: str
    actor_id: str
    tamper_hash: str

    @property
    def event_name(self) -> str:
        return "banking.security.audit.recorded"

    @property
    def source_context(self) -> str:
        return "banking"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "audit_id": self.audit_id,
            "action": self.action,
            "actor_id": self.actor_id,
            "tamper_hash": self.tamper_hash,
        }
