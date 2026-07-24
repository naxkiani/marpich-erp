"""P207-H Behavioral Identity Analytics aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId

ANOMALY_TYPES = frozenset(
    {
        "impossible_travel",
        "unusual_login_time",
        "new_location",
        "unusual_application_access",
        "excessive_access_usage",
        "abnormal_administrative_actions",
        "sudden_pattern_change",
        "abnormal_activity_sequence",
    }
)

UEBA_ENTITY_KINDS = frozenset(
    {
        "user",
        "administrator",
        "service_account",
        "machine_identity",
        "application",
    }
)

LEARNING_METHODS = frozenset(
    {
        "machine_learning",
        "statistical_analysis",
        "pattern_recognition",
        "graph_learning",
    }
)


@dataclass(eq=False, kw_only=True)
class IdentityBehaviorProfileRoot(AggregateRoot):
    """Behavior profile — never rule-only; learning required."""

    tenant_id: str
    profile_ref: str
    subject_ref: str
    rule_only: bool
    learning_enabled: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        profile_ref: str,
        subject_ref: str,
        rule_only: bool = False,
        learning_enabled: bool = True,
    ) -> IdentityBehaviorProfileRoot:
        if not tenant_id.strip():
            raise ValueError("ii.behavior.tenant_required")
        if rule_only:
            raise ValueError("ii.behavior.behavioral_analysis_rule_only")
        if not learning_enabled:
            raise ValueError("ii.behavior.learning_capability_absent")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            profile_ref=profile_ref.strip(),
            subject_ref=subject_ref.strip(),
            rule_only=False,
            learning_enabled=True,
            status="active",
        )
        root.pending_events.append("BehaviorProfileCreated")
        root.history.append({"event": "BehaviorProfileCreated"})
        return root

    def analyze(self) -> None:
        self.status = "analyzed"
        self.pending_events.append("BehaviorAnalyzed")
        self.history.append({"event": "BehaviorAnalyzed"})

    def is_rule_only(self) -> bool:
        return self.rule_only

    def is_learning_absent(self) -> bool:
        return not self.learning_enabled


@dataclass(eq=False, kw_only=True)
class BehaviorBaselineRoot(AggregateRoot):
    tenant_id: str
    baseline_ref: str
    subject_ref: str
    scope: str
    learning_method: str
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def learn(
        cls,
        *,
        tenant_id: str,
        baseline_ref: str,
        subject_ref: str,
        scope: str = "individual_baseline",
        learning_method: str = "machine_learning",
    ) -> BehaviorBaselineRoot:
        if not tenant_id.strip():
            raise ValueError("ii.behavior.baseline_tenant_required")
        method = learning_method.strip().lower()
        if method not in LEARNING_METHODS:
            raise ValueError("ii.behavior.learning_capability_absent")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            baseline_ref=baseline_ref.strip(),
            subject_ref=subject_ref.strip(),
            scope=scope.strip(),
            learning_method=method,
            status="learned",
        )
        root.pending_events.append("BaselineLearned")
        root.history.append({"event": "BaselineLearned"})
        return root


@dataclass(eq=False, kw_only=True)
class AnomalyDetectionCaseRoot(AggregateRoot):
    tenant_id: str
    case_ref: str
    subject_ref: str
    anomaly_type: str
    explanation: str
    high_impact: bool
    hitl_approved: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def detect(
        cls,
        *,
        tenant_id: str,
        case_ref: str,
        subject_ref: str,
        anomaly_type: str,
        explanation: str = "",
        high_impact: bool = False,
        hitl_approved: bool = True,
    ) -> AnomalyDetectionCaseRoot:
        if not tenant_id.strip():
            raise ValueError("ii.behavior.anomaly_tenant_required")
        at = anomaly_type.strip().lower()
        if at not in ANOMALY_TYPES:
            raise ValueError("ii.behavior.anomaly_type_invalid")
        if not explanation.strip():
            raise ValueError("ii.behavior.anomaly_explanations_unavailable")
        if high_impact and not hitl_approved:
            raise ValueError("ii.behavior.skips_hitl_high_impact")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            case_ref=case_ref.strip(),
            subject_ref=subject_ref.strip(),
            anomaly_type=at,
            explanation=explanation.strip(),
            high_impact=high_impact,
            hitl_approved=hitl_approved if high_impact else True,
            status="detected",
        )
        root.pending_events.append("AnomalyDetected")
        root.history.append({"event": "AnomalyDetected"})
        return root

    def is_unexplained(self) -> bool:
        return not self.explanation.strip()

    def start_investigation(self) -> None:
        self.status = "investigating"
        self.pending_events.append("InvestigationStarted")
        self.history.append({"event": "InvestigationStarted"})


@dataclass(eq=False, kw_only=True)
class UebaEntityProfileRoot(AggregateRoot):
    tenant_id: str
    entity_ref: str
    entity_kind: str
    rule_only: bool
    learning_enabled: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def profile(
        cls,
        *,
        tenant_id: str,
        entity_ref: str,
        entity_kind: str = "user",
        rule_only: bool = False,
        learning_enabled: bool = True,
    ) -> UebaEntityProfileRoot:
        if not tenant_id.strip():
            raise ValueError("ii.behavior.ueba_tenant_required")
        kind = entity_kind.strip().lower()
        if kind not in UEBA_ENTITY_KINDS:
            raise ValueError("ii.behavior.ueba_entity_invalid")
        if rule_only:
            raise ValueError("ii.behavior.behavioral_analysis_rule_only")
        if not learning_enabled:
            raise ValueError("ii.behavior.learning_capability_absent")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            entity_ref=entity_ref.strip(),
            entity_kind=kind,
            rule_only=False,
            learning_enabled=True,
            status="profiled",
        )
        root.history.append({"event": "UebaEntityProfiled"})
        return root


@dataclass(eq=False, kw_only=True)
class BehaviorRiskSignalRoot(AggregateRoot):
    tenant_id: str
    signal_ref: str
    subject_ref: str
    risk_level: str
    explanation: str
    via_p207g: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def emit(
        cls,
        *,
        tenant_id: str,
        signal_ref: str,
        subject_ref: str,
        risk_level: str = "medium",
        explanation: str = "",
        via_p207g: bool = True,
    ) -> BehaviorRiskSignalRoot:
        if not tenant_id.strip():
            raise ValueError("ii.behavior.risk_tenant_required")
        if not via_p207g:
            raise ValueError("ii.behavior.risk_intelligence_integration_absent")
        if not explanation.strip():
            raise ValueError("ii.behavior.anomaly_explanations_unavailable")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            signal_ref=signal_ref.strip(),
            subject_ref=subject_ref.strip(),
            risk_level=risk_level.strip(),
            explanation=explanation.strip(),
            via_p207g=True,
            status="emitted",
        )
        root.pending_events.append("RiskUpdated")
        root.history.append({"event": "RiskUpdated"})
        return root

    def is_risk_integration_absent(self) -> bool:
        return not self.via_p207g


@dataclass(eq=False, kw_only=True)
class BehaviorTrustSignalRoot(AggregateRoot):
    tenant_id: str
    trust_ref: str
    subject_ref: str
    score: float
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def update(
        cls,
        *,
        tenant_id: str,
        trust_ref: str,
        subject_ref: str,
        score: float = 0.7,
    ) -> BehaviorTrustSignalRoot:
        if not tenant_id.strip():
            raise ValueError("ii.behavior.trust_tenant_required")
        if score < 0 or score > 1:
            raise ValueError("ii.behavior.trust_score_invalid")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            trust_ref=trust_ref.strip(),
            subject_ref=subject_ref.strip(),
            score=score,
            status="updated",
        )
        root.pending_events.append("TrustChanged")
        root.history.append({"event": "TrustChanged"})
        return root


@dataclass(eq=False, kw_only=True)
class BehaviorPrivacyPolicyRoot(AggregateRoot):
    tenant_id: str
    policy_ref: str
    privacy_controls: bool
    ai_governed: bool
    data_minimization: bool
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
        privacy_controls: bool = True,
        ai_governed: bool = True,
        data_minimization: bool = True,
    ) -> BehaviorPrivacyPolicyRoot:
        if not tenant_id.strip():
            raise ValueError("ii.behavior.privacy_tenant_required")
        if not privacy_controls or not data_minimization:
            raise ValueError("ii.behavior.privacy_controls_missing")
        if not ai_governed:
            raise ValueError("ii.behavior.ai_models_cannot_be_governed")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            policy_ref=policy_ref.strip(),
            privacy_controls=True,
            ai_governed=True,
            data_minimization=True,
            status="active",
        )
        root.history.append({"event": "BehaviorPrivacyDefined"})
        return root

    def is_privacy_missing(self) -> bool:
        return not self.privacy_controls or not self.data_minimization

    def is_ai_ungoverned(self) -> bool:
        return not self.ai_governed
