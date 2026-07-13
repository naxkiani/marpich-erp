"""Identity risk integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent


@dataclass(frozen=True, kw_only=True)
class RiskScoreComputedIntegration(IntegrationEvent):
    score_ref: str
    signal_ref: str
    score: int
    risk_level: str
    user_id: str | None

    @property
    def event_name(self) -> str:
        return "identity_risk.score.computed"

    @property
    def source_context(self) -> str:
        return "identity_risk"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "score_ref": self.score_ref,
            "signal_ref": self.signal_ref,
            "score": self.score,
            "risk_level": self.risk_level,
            "user_id": self.user_id,
        }


@dataclass(frozen=True, kw_only=True)
class AnomalyDetectedIntegration(IntegrationEvent):
    alert_ref: str
    score_ref: str
    severity: str
    title: str

    @property
    def event_name(self) -> str:
        return "identity_risk.anomaly.detected"

    @property
    def source_context(self) -> str:
        return "identity_risk"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "alert_ref": self.alert_ref,
            "score_ref": self.score_ref,
            "severity": self.severity,
            "title": self.title,
        }


@dataclass(frozen=True, kw_only=True)
class StepUpRecommendedIntegration(IntegrationEvent):
    score_ref: str
    user_id: str | None
    score: int

    @property
    def event_name(self) -> str:
        return "identity_risk.step_up.recommended"

    @property
    def source_context(self) -> str:
        return "identity_risk"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"score_ref": self.score_ref, "user_id": self.user_id, "score": self.score}
