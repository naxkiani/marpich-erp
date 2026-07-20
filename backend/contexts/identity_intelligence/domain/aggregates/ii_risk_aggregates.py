"""P207-G Predictive Identity Risk Intelligence aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId

RISK_TIERS = frozenset({"low", "medium", "high", "critical"})
RESPONSE_ACTIONS = frozenset(
    {"monitor", "recommend", "require_approval", "automated_protection"}
)


@dataclass(eq=False, kw_only=True)
class IdentityRiskProfileRoot(AggregateRoot):
    """Risk profile — never static-only; explanation required."""

    tenant_id: str
    profile_ref: str
    subject_ref: str
    current_score: float
    predicted_score: float
    explanation: str
    static_only: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def calculate(
        cls,
        *,
        tenant_id: str,
        profile_ref: str,
        subject_ref: str,
        current_score: float = 0.4,
        predicted_score: float = 0.5,
        explanation: str = "",
        static_only: bool = False,
    ) -> IdentityRiskProfileRoot:
        if not tenant_id.strip():
            raise ValueError("ii.risk.tenant_required")
        if static_only:
            raise ValueError("ii.risk.risk_static_only")
        if not explanation.strip():
            raise ValueError("ii.risk.risk_explanation_unavailable")
        if not (0 <= current_score <= 1) or not (0 <= predicted_score <= 1):
            raise ValueError("ii.risk.score_invalid")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            profile_ref=profile_ref.strip(),
            subject_ref=subject_ref.strip(),
            current_score=current_score,
            predicted_score=predicted_score,
            explanation=explanation.strip(),
            static_only=False,
            status="calculated",
        )
        root.pending_events.append("RiskCalculated")
        if predicted_score > current_score:
            root.pending_events.append("RiskIncreased")
        root.history.append({"event": "RiskCalculated"})
        return root

    def is_static_only(self) -> bool:
        return self.static_only

    def is_explanation_unavailable(self) -> bool:
        return not self.explanation.strip()


@dataclass(eq=False, kw_only=True)
class RiskSignalFusionBatchRoot(AggregateRoot):
    tenant_id: str
    batch_ref: str
    signal_categories: tuple[str, ...]
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def fuse(
        cls,
        *,
        tenant_id: str,
        batch_ref: str,
        signal_categories: tuple[str, ...] | None = None,
    ) -> RiskSignalFusionBatchRoot:
        if not tenant_id.strip():
            raise ValueError("ii.risk.fusion_tenant_required")
        cats = signal_categories or (
            "identity_signals",
            "access_signals",
            "privilege_signals",
            "behavior_signals",
            "security_signals",
        )
        if not cats:
            raise ValueError("ii.risk.signals_empty")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            batch_ref=batch_ref.strip(),
            signal_categories=tuple(cats),
            status="fused",
        )
        root.pending_events.append("SignalsFused")
        root.history.append({"event": "SignalsFused"})
        return root


@dataclass(eq=False, kw_only=True)
class RiskPredictionCaseRoot(AggregateRoot):
    tenant_id: str
    case_ref: str
    subject_ref: str
    target: str
    forecast: str
    confidence: float
    prediction_present: bool
    via_ai_platform: bool
    auditable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def predict(
        cls,
        *,
        tenant_id: str,
        case_ref: str,
        subject_ref: str,
        target: str = "future_identity_risk",
        forecast: str = "",
        confidence: float = 0.75,
        prediction_present: bool = True,
        via_ai_platform: bool = True,
        auditable: bool = True,
    ) -> RiskPredictionCaseRoot:
        if not tenant_id.strip():
            raise ValueError("ii.risk.pred_tenant_required")
        if not prediction_present or not forecast.strip():
            raise ValueError("ii.risk.prediction_capability_absent")
        if not via_ai_platform:
            raise ValueError("ii.risk.embeds_llm_sdk")
        if not auditable:
            raise ValueError("ii.risk.ai_decisions_not_auditable")
        if confidence < 0 or confidence > 1:
            raise ValueError("ii.risk.confidence_invalid")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            case_ref=case_ref.strip(),
            subject_ref=subject_ref.strip(),
            target=target.strip(),
            forecast=forecast.strip(),
            confidence=confidence,
            prediction_present=True,
            via_ai_platform=True,
            auditable=True,
            status="predicted",
        )
        root.pending_events.append("RiskPredicted")
        root.history.append({"event": "RiskPredicted"})
        return root

    def is_prediction_absent(self) -> bool:
        return not self.prediction_present or not self.forecast.strip()

    def is_unauditable(self) -> bool:
        return not self.auditable


@dataclass(eq=False, kw_only=True)
class ContinuousTrustScoreRoot(AggregateRoot):
    tenant_id: str
    trust_ref: str
    subject_ref: str
    score: float
    defined: bool
    inputs: tuple[str, ...]
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def evaluate(
        cls,
        *,
        tenant_id: str,
        trust_ref: str,
        subject_ref: str,
        score: float = 0.7,
        defined: bool = True,
        inputs: tuple[str, ...] | None = None,
    ) -> ContinuousTrustScoreRoot:
        if not tenant_id.strip():
            raise ValueError("ii.risk.trust_tenant_required")
        if not defined:
            raise ValueError("ii.risk.trust_calculation_undefined")
        inp = inputs or (
            "identity_context",
            "behavior",
            "risk",
            "environment",
            "security_signals",
        )
        if not inp:
            raise ValueError("ii.risk.trust_calculation_undefined")
        if score < 0 or score > 1:
            raise ValueError("ii.risk.trust_score_invalid")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            trust_ref=trust_ref.strip(),
            subject_ref=subject_ref.strip(),
            score=score,
            defined=True,
            inputs=tuple(inp),
            status="evaluated",
        )
        root.pending_events.append("TrustUpdated")
        root.history.append({"event": "TrustUpdated"})
        return root

    def is_undefined(self) -> bool:
        return not self.defined or len(self.inputs) == 0


@dataclass(eq=False, kw_only=True)
class BehaviorRiskFindingRoot(AggregateRoot):
    tenant_id: str
    finding_ref: str
    subject_ref: str
    pattern: str
    threat_detected: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def analyze(
        cls,
        *,
        tenant_id: str,
        finding_ref: str,
        subject_ref: str,
        pattern: str = "suspicious_behavior",
        threat_detected: bool = False,
    ) -> BehaviorRiskFindingRoot:
        if not tenant_id.strip() or not subject_ref.strip():
            raise ValueError("ii.risk.behavior_required")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            finding_ref=finding_ref.strip(),
            subject_ref=subject_ref.strip(),
            pattern=pattern.strip(),
            threat_detected=threat_detected,
            status="analyzed",
        )
        if threat_detected:
            root.pending_events.append("ThreatDetected")
        root.history.append({"event": "BehaviorAnalyzed"})
        return root


@dataclass(eq=False, kw_only=True)
class RiskMitigationRecommendationRoot(AggregateRoot):
    tenant_id: str
    mitigation_ref: str
    subject_ref: str
    tier: str
    action: str
    governed: bool
    hitl_approved: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def recommend(
        cls,
        *,
        tenant_id: str,
        mitigation_ref: str,
        subject_ref: str,
        tier: str = "medium",
        action: str = "recommend",
        governed: bool = True,
        hitl_approved: bool = True,
    ) -> RiskMitigationRecommendationRoot:
        if not tenant_id.strip():
            raise ValueError("ii.risk.mit_tenant_required")
        t = tier.strip().lower()
        a = action.strip().lower()
        if t not in RISK_TIERS:
            raise ValueError("ii.risk.tier_invalid")
        if a not in RESPONSE_ACTIONS:
            raise ValueError("ii.risk.action_invalid")
        if not governed:
            raise ValueError("ii.risk.automated_response_lacks_governance")
        if t in {"high", "critical"} and not hitl_approved:
            raise ValueError("ii.risk.skips_hitl_high_critical")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            mitigation_ref=mitigation_ref.strip(),
            subject_ref=subject_ref.strip(),
            tier=t,
            action=a,
            governed=True,
            hitl_approved=hitl_approved if t in {"high", "critical"} else True,
            status="recommended",
        )
        root.pending_events.append("MitigationRecommended")
        root.history.append({"event": "MitigationRecommended"})
        return root

    def is_ungoverned(self) -> bool:
        return not self.governed


@dataclass(eq=False, kw_only=True)
class RiskGovernancePolicyRoot(AggregateRoot):
    tenant_id: str
    policy_ref: str
    explanation_required: bool
    trust_defined: bool
    response_governed: bool
    ai_auditable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def define(
        cls,
        *,
        tenant_id: str,
        policy_ref: str,
        explanation_required: bool = True,
        trust_defined: bool = True,
        response_governed: bool = True,
        ai_auditable: bool = True,
    ) -> RiskGovernancePolicyRoot:
        if not tenant_id.strip():
            raise ValueError("ii.risk.gov_tenant_required")
        if not explanation_required:
            raise ValueError("ii.risk.risk_explanation_unavailable")
        if not trust_defined:
            raise ValueError("ii.risk.trust_calculation_undefined")
        if not response_governed:
            raise ValueError("ii.risk.automated_response_lacks_governance")
        if not ai_auditable:
            raise ValueError("ii.risk.ai_decisions_not_auditable")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            policy_ref=policy_ref.strip(),
            explanation_required=True,
            trust_defined=True,
            response_governed=True,
            ai_auditable=True,
            status="active",
        )
        root.history.append({"event": "RiskGovernanceDefined"})
        return root
