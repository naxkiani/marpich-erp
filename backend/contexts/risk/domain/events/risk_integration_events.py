"""Enterprise Risk Platform integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent


@dataclass(frozen=True, kw_only=True)
class RiskItemRegisteredIntegration(IntegrationEvent):
    risk_ref: str
    category: str
    risk_score: int
    severity: str

    @property
    def event_name(self) -> str:
        return "risk.item.registered"

    @property
    def source_context(self) -> str:
        return "risk"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "risk_ref": self.risk_ref,
            "category": self.category,
            "risk_score": self.risk_score,
            "severity": self.severity,
        }


@dataclass(frozen=True, kw_only=True)
class RiskItemEscalatedIntegration(IntegrationEvent):
    risk_ref: str
    category: str
    risk_score: int

    @property
    def event_name(self) -> str:
        return "risk.item.escalated"

    @property
    def source_context(self) -> str:
        return "risk"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "risk_ref": self.risk_ref,
            "category": self.category,
            "risk_score": self.risk_score,
        }


@dataclass(frozen=True, kw_only=True)
class RiskPredictionGeneratedIntegration(IntegrationEvent):
    prediction_ref: str
    category: str
    predicted_score: float
    trend: str

    @property
    def event_name(self) -> str:
        return "risk.prediction.generated"

    @property
    def source_context(self) -> str:
        return "risk"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "prediction_ref": self.prediction_ref,
            "category": self.category,
            "predicted_score": self.predicted_score,
            "trend": self.trend,
        }


@dataclass(frozen=True, kw_only=True)
class RiskMatrixUpdatedIntegration(IntegrationEvent):
    matrix_ref: str
    total_mapped: int

    @property
    def event_name(self) -> str:
        return "risk.matrix.updated"

    @property
    def source_context(self) -> str:
        return "risk"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"matrix_ref": self.matrix_ref, "total_mapped": self.total_mapped}
