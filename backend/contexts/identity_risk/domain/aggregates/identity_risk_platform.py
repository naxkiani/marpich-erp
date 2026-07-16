"""Identity risk platform aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class IdentityRiskCapability(StrEnum):
    RISK_SIGNAL_CATALOG = "risk_signal_catalog"
    AUTHENTICATION_RISK_SCORING = "authentication_risk_scoring"
    DIRECTORY_SYNC_RISK_SCORING = "directory_sync_risk_scoring"
    FEDERATION_RISK_SCORING = "federation_risk_scoring"
    ANOMALY_DETECTION = "anomaly_detection"
    RISK_SCORE_REGISTRY = "risk_score_registry"
    STEP_UP_RECOMMENDATION = "step_up_recommendation"
    POLICY_DRIVEN_RISK = "policy_driven_risk"
    IDENTITY_RISK_DASHBOARD = "identity_risk_dashboard"
    IDENTITY_RISK_API = "identity_risk_api"


class RiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SignalSource(StrEnum):
    AUTHENTICATION = "authentication"
    DIRECTORY = "directory"
    SCIM = "scim"
    MANUAL = "manual"


@dataclass(eq=False, kw_only=True)
class RiskProfile(AggregateRoot):
    tenant_id: str
    profile_ref: str
    scoring_enabled: bool = True
    score_threshold: int = 50
    step_up_threshold: int = 75
    bulk_create_threshold: int = 10
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(cls, *, tenant_id: str, profile_ref: str) -> RiskProfile:
        return cls(id=UniqueId.generate(), tenant_id=tenant_id, profile_ref=profile_ref)

    def to_dict(self) -> dict:
        return {
            "profile_ref": self.profile_ref,
            "tenant_id": self.tenant_id,
            "scoring_enabled": self.scoring_enabled,
            "score_threshold": self.score_threshold,
            "step_up_threshold": self.step_up_threshold,
            "bulk_create_threshold": self.bulk_create_threshold,
        }


@dataclass(eq=False, kw_only=True)
class RiskSignal(AggregateRoot):
    tenant_id: str
    signal_ref: str
    source: str
    event_name: str
    user_id: str | None
    factors: list[dict] = field(default_factory=list)
    raw_payload: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def capture(
        cls,
        *,
        tenant_id: str,
        signal_ref: str,
        source: str,
        event_name: str,
        user_id: str | None,
        factors: list[dict],
        raw_payload: dict,
    ) -> RiskSignal:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            signal_ref=signal_ref,
            source=source,
            event_name=event_name,
            user_id=user_id,
            factors=factors,
            raw_payload=raw_payload,
        )

    def to_dict(self) -> dict:
        return {
            "signal_ref": self.signal_ref,
            "tenant_id": self.tenant_id,
            "source": self.source,
            "event_name": self.event_name,
            "user_id": self.user_id,
            "factors": self.factors,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class RiskScore(AggregateRoot):
    tenant_id: str
    score_ref: str
    signal_ref: str
    score: int
    risk_level: str
    explanation: str
    factors: list[dict] = field(default_factory=list)
    step_up_recommended: bool = False
    user_id: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def compute(
        cls,
        *,
        tenant_id: str,
        score_ref: str,
        signal_ref: str,
        score: int,
        risk_level: str,
        explanation: str,
        factors: list[dict],
        step_up_recommended: bool,
        user_id: str | None,
    ) -> RiskScore:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            score_ref=score_ref,
            signal_ref=signal_ref,
            score=score,
            risk_level=risk_level,
            explanation=explanation,
            factors=factors,
            step_up_recommended=step_up_recommended,
            user_id=user_id,
        )

    def to_dict(self) -> dict:
        return {
            "score_ref": self.score_ref,
            "tenant_id": self.tenant_id,
            "signal_ref": self.signal_ref,
            "score": self.score,
            "risk_level": self.risk_level,
            "explanation": self.explanation,
            "factors": self.factors,
            "step_up_recommended": self.step_up_recommended,
            "user_id": self.user_id,
            "explainable": True,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class AnomalyAlert(AggregateRoot):
    tenant_id: str
    alert_ref: str
    score_ref: str
    title: str
    severity: str
    description: str
    acknowledged: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def raise_alert(
        cls,
        *,
        tenant_id: str,
        alert_ref: str,
        score_ref: str,
        title: str,
        severity: str,
        description: str,
    ) -> AnomalyAlert:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            alert_ref=alert_ref,
            score_ref=score_ref,
            title=title,
            severity=severity,
            description=description,
        )

    def to_dict(self) -> dict:
        return {
            "alert_ref": self.alert_ref,
            "tenant_id": self.tenant_id,
            "score_ref": self.score_ref,
            "title": self.title,
            "severity": self.severity,
            "description": self.description,
            "acknowledged": self.acknowledged,
            "created_at": self.created_at.isoformat(),
        }
