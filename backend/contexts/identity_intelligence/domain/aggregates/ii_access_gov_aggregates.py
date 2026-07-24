"""P207-J AI Driven Governance & Access Optimization aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId

ENTITLEMENT_CLASSES = frozenset({"critical", "sensitive", "standard"})
CERTIFICATION_ACTIONS = frozenset({"approve", "remove", "modify", "escalate"})


@dataclass(eq=False, kw_only=True)
class AccessGovernanceCaseRoot(AggregateRoot):
    """Continuous governance — never periodic-only."""

    tenant_id: str
    case_ref: str
    subject_ref: str
    periodic_only: bool
    continuous: bool
    business_context: str
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def analyze(
        cls,
        *,
        tenant_id: str,
        case_ref: str,
        subject_ref: str,
        periodic_only: bool = False,
        continuous: bool = True,
        business_context: str = "",
    ) -> AccessGovernanceCaseRoot:
        if not tenant_id.strip():
            raise ValueError("ii.access_gov.tenant_required")
        if periodic_only or not continuous:
            raise ValueError("ii.access_gov.governance_periodic_only")
        if not business_context.strip():
            raise ValueError("ii.access_gov.optimization_ignores_business_context")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            case_ref=case_ref.strip(),
            subject_ref=subject_ref.strip(),
            periodic_only=False,
            continuous=True,
            business_context=business_context.strip(),
            status="analyzed",
        )
        root.pending_events.append("AccessAnalyzed")
        root.history.append({"event": "AccessAnalyzed"})
        return root

    def is_periodic_only(self) -> bool:
        return self.periodic_only or not self.continuous


@dataclass(eq=False, kw_only=True)
class EntitlementIntelligenceRecordRoot(AggregateRoot):
    tenant_id: str
    record_ref: str
    subject_ref: str
    entitlement_class: str
    risk_kind: str
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def discover(
        cls,
        *,
        tenant_id: str,
        record_ref: str,
        subject_ref: str,
        entitlement_class: str = "sensitive",
        risk_kind: str = "excessive_access",
    ) -> EntitlementIntelligenceRecordRoot:
        if not tenant_id.strip():
            raise ValueError("ii.access_gov.ent_tenant_required")
        ec = entitlement_class.strip().lower()
        if ec not in ENTITLEMENT_CLASSES:
            raise ValueError("ii.access_gov.entitlement_class_invalid")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            record_ref=record_ref.strip(),
            subject_ref=subject_ref.strip(),
            entitlement_class=ec,
            risk_kind=risk_kind.strip(),
            status="discovered",
        )
        if risk_kind in {"excessive_access", "toxic_combination"}:
            root.pending_events.append("RiskDetected")
        root.history.append({"event": "EntitlementDiscovered"})
        return root


@dataclass(eq=False, kw_only=True)
class AccessOptimizationRecommendationRoot(AggregateRoot):
    tenant_id: str
    recommendation_ref: str
    subject_ref: str
    action: str
    explanation: str
    business_context: str
    via_p207g: bool
    human_governance: bool
    hitl_approved: bool
    high_impact: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def recommend(
        cls,
        *,
        tenant_id: str,
        recommendation_ref: str,
        subject_ref: str,
        action: str = "remove",
        explanation: str = "",
        business_context: str = "",
        via_p207g: bool = True,
        human_governance: bool = True,
        hitl_approved: bool = True,
        high_impact: bool = False,
    ) -> AccessOptimizationRecommendationRoot:
        if not tenant_id.strip():
            raise ValueError("ii.access_gov.rec_tenant_required")
        if not explanation.strip():
            raise ValueError("ii.access_gov.ai_recommendations_unexplained")
        if not business_context.strip():
            raise ValueError("ii.access_gov.optimization_ignores_business_context")
        if not via_p207g:
            raise ValueError("ii.access_gov.risk_intelligence_disconnected")
        if not human_governance:
            raise ValueError("ii.access_gov.human_governance_absent")
        if high_impact and not hitl_approved:
            raise ValueError("ii.access_gov.skips_hitl_high_impact")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            recommendation_ref=recommendation_ref.strip(),
            subject_ref=subject_ref.strip(),
            action=action.strip(),
            explanation=explanation.strip(),
            business_context=business_context.strip(),
            via_p207g=True,
            human_governance=True,
            hitl_approved=hitl_approved if high_impact else True,
            high_impact=high_impact,
            status="recommended",
        )
        root.pending_events.append("OptimizationRecommended")
        if high_impact:
            root.pending_events.append("ApprovalRequested")
        root.history.append({"event": "OptimizationRecommended"})
        return root

    def is_unexplained(self) -> bool:
        return not self.explanation.strip()

    def is_risk_disconnected(self) -> bool:
        return not self.via_p207g

    def execute(self) -> None:
        self.status = "optimized"
        self.pending_events.append("AccessOptimized")
        self.pending_events.append("GovernanceUpdated")
        self.history.append({"event": "AccessOptimized"})


@dataclass(eq=False, kw_only=True)
class CertificationInsightRoot(AggregateRoot):
    tenant_id: str
    insight_ref: str
    subject_ref: str
    recommended_action: str
    explanation: str
    continuous: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def generate(
        cls,
        *,
        tenant_id: str,
        insight_ref: str,
        subject_ref: str,
        recommended_action: str = "remove",
        explanation: str = "",
        continuous: bool = True,
    ) -> CertificationInsightRoot:
        if not tenant_id.strip():
            raise ValueError("ii.access_gov.insight_tenant_required")
        action = recommended_action.strip().lower()
        if action not in CERTIFICATION_ACTIONS:
            raise ValueError("ii.access_gov.cert_action_invalid")
        if not explanation.strip():
            raise ValueError("ii.access_gov.ai_recommendations_unexplained")
        if not continuous:
            raise ValueError("ii.access_gov.governance_periodic_only")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            insight_ref=insight_ref.strip(),
            subject_ref=subject_ref.strip(),
            recommended_action=action,
            explanation=explanation.strip(),
            continuous=True,
            status="generated",
        )
        root.history.append({"event": "CertificationInsightGenerated"})
        return root


@dataclass(eq=False, kw_only=True)
class RoleOptimizationProposalRoot(AggregateRoot):
    tenant_id: str
    proposal_ref: str
    role_ref: str
    duplicates_iga_sor: bool
    via_p202: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def propose(
        cls,
        *,
        tenant_id: str,
        proposal_ref: str,
        role_ref: str,
        duplicates_iga_sor: bool = False,
        via_p202: bool = True,
    ) -> RoleOptimizationProposalRoot:
        if not tenant_id.strip():
            raise ValueError("ii.access_gov.role_tenant_required")
        if duplicates_iga_sor:
            raise ValueError("ii.access_gov.duplicates_p202_iga_sor")
        if not via_p202:
            raise ValueError("ii.access_gov.iga_peer_required")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            proposal_ref=proposal_ref.strip(),
            role_ref=role_ref.strip(),
            duplicates_iga_sor=False,
            via_p202=True,
            status="proposed",
        )
        root.history.append({"event": "RoleOptimizationProposed"})
        return root


@dataclass(eq=False, kw_only=True)
class PolicyIntelligenceFindingRoot(AggregateRoot):
    tenant_id: str
    finding_ref: str
    policy_key: str
    conflict_detected: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def evaluate(
        cls,
        *,
        tenant_id: str,
        finding_ref: str,
        policy_key: str,
        conflict_detected: bool = False,
    ) -> PolicyIntelligenceFindingRoot:
        if not tenant_id.strip() or not policy_key.strip():
            raise ValueError("ii.access_gov.policy_required")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            finding_ref=finding_ref.strip(),
            policy_key=policy_key.strip(),
            conflict_detected=conflict_detected,
            status="evaluated",
        )
        root.history.append({"event": "PolicyEvaluated"})
        return root


@dataclass(eq=False, kw_only=True)
class GovernanceComplianceEvidenceRoot(AggregateRoot):
    tenant_id: str
    evidence_ref: str
    case_ref: str
    available: bool
    audit_trail: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def generate(
        cls,
        *,
        tenant_id: str,
        evidence_ref: str,
        case_ref: str,
        available: bool = True,
        audit_trail: bool = True,
    ) -> GovernanceComplianceEvidenceRoot:
        if not tenant_id.strip():
            raise ValueError("ii.access_gov.evidence_tenant_required")
        if not available or not audit_trail:
            raise ValueError("ii.access_gov.compliance_evidence_unavailable")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            evidence_ref=evidence_ref.strip(),
            case_ref=case_ref.strip(),
            available=True,
            audit_trail=True,
            status="generated",
        )
        root.pending_events.append("ComplianceEvidenceGenerated")
        root.history.append({"event": "ComplianceEvidenceGenerated"})
        return root

    def is_unavailable(self) -> bool:
        return not self.available or not self.audit_trail
