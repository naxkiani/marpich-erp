"""P211-L AI security aggregates — quality-gate invariants."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class DsExplainableAiDecisionRoot(AggregateRoot):
    tenant_id: str
    decision_ref: str
    explainable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def decide(
        cls, *, tenant_id: str, decision_ref: str, explainable: bool = True
    ) -> DsExplainableAiDecisionRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.ai.tenant_required")
        if not explainable:
            raise ValueError(
                "data_security.ai.ai_decisions_are_not_explainable"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            decision_ref=decision_ref.strip(),
            explainable=True,
            status="explained",
        )
        root.pending_events.append("RecommendationGenerated")
        root.pending_events.append("UnexplainableAiRejected")
        root.history.append({"event": "AiExplainable"})
        return root

    def is_unexplainable(self) -> bool:
        return not self.explainable


@dataclass(eq=False, kw_only=True)
class DsControlledAutonomyRoot(AggregateRoot):
    tenant_id: str
    action_ref: str
    controlled: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def execute(
        cls, *, tenant_id: str, action_ref: str, controlled: bool = True
    ) -> DsControlledAutonomyRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.ai.aut_tenant_required")
        if not controlled:
            raise ValueError(
                "data_security.ai.autonomous_actions_are_uncontrolled"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            action_ref=action_ref.strip(),
            controlled=True,
            status="controlled",
        )
        root.pending_events.append("ProtectionExecuted")
        root.pending_events.append("UncontrolledAutonomyRejected")
        root.history.append({"event": "AutonomyControlled"})
        return root

    def is_uncontrolled(self) -> bool:
        return not self.controlled


@dataclass(eq=False, kw_only=True)
class DsPredictableRiskRoot(AggregateRoot):
    tenant_id: str
    prediction_ref: str
    predictable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def predict(
        cls, *, tenant_id: str, prediction_ref: str, predictable: bool = True
    ) -> DsPredictableRiskRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.ai.risk_tenant_required")
        if not predictable:
            raise ValueError(
                "data_security.ai.data_risks_cannot_be_predicted"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            prediction_ref=prediction_ref.strip(),
            predictable=True,
            status="predicted",
        )
        root.pending_events.append("RiskPredicted")
        root.pending_events.append("UnpredictableRiskRejected")
        root.history.append({"event": "RiskPredictable"})
        return root

    def is_unpredictable(self) -> bool:
        return not self.predictable


@dataclass(eq=False, kw_only=True)
class DsLearningLoopRoot(AggregateRoot):
    tenant_id: str
    loop_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def complete(
        cls, *, tenant_id: str, loop_ref: str, present: bool = True
    ) -> DsLearningLoopRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.ai.learn_tenant_required")
        if not present:
            raise ValueError("data_security.ai.learning_loop_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            loop_ref=loop_ref.strip(),
            present=True,
            status="active",
        )
        root.pending_events.append("LearningCompleted")
        root.pending_events.append("ModelUpdated")
        root.pending_events.append("MissingLearningLoopRejected")
        root.history.append({"event": "LearningLoopPresent"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DsAiGovernanceRoot(AggregateRoot):
    tenant_id: str
    governance_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def establish(
        cls, *, tenant_id: str, governance_ref: str, present: bool = True
    ) -> DsAiGovernanceRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.ai.gov_tenant_required")
        if not present:
            raise ValueError(
                "data_security.ai.ai_security_governance_is_absent"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            governance_ref=governance_ref.strip(),
            present=True,
            status="present",
        )
        root.pending_events.append("PolicyOptimized")
        root.pending_events.append("AbsentAiGovernanceRejected")
        root.history.append({"event": "AiGovernancePresent"})
        return root

    def is_absent(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DsHumanOversightRoot(AggregateRoot):
    tenant_id: str
    oversight_ref: str
    possible: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def approve(
        cls, *, tenant_id: str, oversight_ref: str, possible: bool = True
    ) -> DsHumanOversightRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.ai.oversight_tenant_required")
        if not possible:
            raise ValueError(
                "data_security.ai.human_oversight_is_impossible"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            oversight_ref=oversight_ref.strip(),
            possible=True,
            status="oversight_ready",
        )
        root.pending_events.append("ProtectionExecuted")
        root.pending_events.append("ImpossibleHumanOversightRejected")
        root.history.append({"event": "HumanOversightPossible"})
        return root

    def is_impossible(self) -> bool:
        return not self.possible


@dataclass(eq=False, kw_only=True)
class DsThreatDetectedRoot(AggregateRoot):
    tenant_id: str
    threat_ref: str
    detected: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def detect(
        cls, *, tenant_id: str, threat_ref: str, detected: bool = True
    ) -> DsThreatDetectedRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.ai.threat_tenant_required")
        if not detected:
            raise ValueError("data_security.ai.threat_not_detected")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            threat_ref=threat_ref.strip(),
            detected=True,
            status="detected",
        )
        root.pending_events.append("ThreatDetected")
        root.history.append({"event": "ThreatDetected"})
        return root


@dataclass(eq=False, kw_only=True)
class DsPolicyOptimizedRoot(AggregateRoot):
    tenant_id: str
    policy_ref: str
    optimized: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def optimize(
        cls, *, tenant_id: str, policy_ref: str, optimized: bool = True
    ) -> DsPolicyOptimizedRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.ai.pol_tenant_required")
        if not optimized:
            raise ValueError("data_security.ai.policy_not_optimized")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            policy_ref=policy_ref.strip(),
            optimized=True,
            status="optimized",
        )
        root.pending_events.append("PolicyOptimized")
        root.history.append({"event": "PolicyOptimized"})
        return root
