"""P207-M AI Security, Responsible AI & Governance aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId

AUTONOMY_LEVELS = frozenset(
    {
        "level_0_human_only",
        "level_1_ai_recommendation",
        "level_2_ai_executes_with_approval",
        "level_3_controlled_automation",
        "level_4_autonomous_operation",
    }
)

AI_THREATS = frozenset(
    {
        "prompt_injection",
        "data_leakage",
        "model_manipulation",
        "model_theft",
        "adversarial_input",
        "unauthorized_agent_actions",
    }
)


@dataclass(eq=False, kw_only=True)
class AIModelAssetRoot(AggregateRoot):
    tenant_id: str
    model_ref: str
    version: str
    owner_ref: str
    purpose: str
    risk_classification: str
    monitored: bool
    governed: bool
    owns_platform_sor: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(
        cls,
        *,
        tenant_id: str,
        model_ref: str,
        version: str = "1.0.0",
        owner_ref: str,
        purpose: str,
        risk_classification: str = "medium",
        monitored: bool = True,
        governed: bool = True,
        owns_platform_sor: bool = False,
    ) -> AIModelAssetRoot:
        if not tenant_id.strip():
            raise ValueError("ii.ai_gov.tenant_required")
        if not governed:
            raise ValueError("ii.ai_gov.ai_operates_without_governance")
        if not monitored:
            raise ValueError("ii.ai_gov.models_unmonitored")
        if owns_platform_sor:
            raise ValueError("ii.ai_gov.duplicates_platform_ai_governance_sor")
        if not owner_ref.strip() or not purpose.strip():
            raise ValueError("ii.ai_gov.model_asset_incomplete")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            model_ref=model_ref.strip(),
            version=version.strip(),
            owner_ref=owner_ref.strip(),
            purpose=purpose.strip(),
            risk_classification=risk_classification.strip(),
            monitored=True,
            governed=True,
            owns_platform_sor=False,
            status="registered",
        )
        root.pending_events.append("AIModelRegistered")
        root.history.append({"event": "AIModelRegistered"})
        return root

    def is_unmonitored(self) -> bool:
        return not self.monitored

    def is_ungoverned(self) -> bool:
        return not self.governed


@dataclass(eq=False, kw_only=True)
class AIAgentGovernanceRecordRoot(AggregateRoot):
    tenant_id: str
    agent_ref: str
    ai_identity_ref: str
    permission_scope: tuple[str, ...]
    approved: bool
    via_workflow: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def approve(
        cls,
        *,
        tenant_id: str,
        agent_ref: str,
        ai_identity_ref: str = "",
        permission_scope: tuple[str, ...] | None = None,
        approved: bool = True,
        via_workflow: bool = True,
    ) -> AIAgentGovernanceRecordRoot:
        if not tenant_id.strip():
            raise ValueError("ii.ai_gov.agent_tenant_required")
        if not ai_identity_ref.strip():
            raise ValueError("ii.ai_gov.ai_identities_undefined")
        scope = permission_scope or ("identity_intelligence.read",)
        if not scope:
            raise ValueError("ii.ai_gov.ai_identities_undefined")
        if not via_workflow:
            raise ValueError("ii.ai_gov.ai_operates_without_governance")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            agent_ref=agent_ref.strip(),
            ai_identity_ref=ai_identity_ref.strip(),
            permission_scope=tuple(scope),
            approved=approved,
            via_workflow=True,
            status="approved",
        )
        root.pending_events.append("AgentApproved")
        root.history.append({"event": "AgentApproved"})
        return root

    def identity_undefined(self) -> bool:
        return not self.ai_identity_ref.strip()


@dataclass(eq=False, kw_only=True)
class AIDecisionExplanationRoot(AggregateRoot):
    tenant_id: str
    decision_ref: str
    decision: str
    reason: str
    evidence: str
    confidence: float
    impact: str
    recommendation: str
    explainable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def explain(
        cls,
        *,
        tenant_id: str,
        decision_ref: str,
        decision: str,
        reason: str = "",
        evidence: str = "",
        confidence: float = 0.0,
        impact: str = "",
        recommendation: str = "",
        explainable: bool = True,
    ) -> AIDecisionExplanationRoot:
        if not tenant_id.strip():
            raise ValueError("ii.ai_gov.decision_tenant_required")
        if not explainable or not all(
            [
                decision.strip(),
                reason.strip(),
                evidence.strip(),
                impact.strip(),
                recommendation.strip(),
            ]
        ):
            raise ValueError("ii.ai_gov.decisions_unexplainable")
        if confidence <= 0 or confidence > 1:
            raise ValueError("ii.ai_gov.confidence_invalid")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            decision_ref=decision_ref.strip(),
            decision=decision.strip(),
            reason=reason.strip(),
            evidence=evidence.strip(),
            confidence=confidence,
            impact=impact.strip(),
            recommendation=recommendation.strip(),
            explainable=True,
            status="explained",
        )
        root.pending_events.append("DecisionExplained")
        root.history.append({"event": "DecisionExplained"})
        return root

    def is_unexplainable(self) -> bool:
        return not self.explainable or not self.reason.strip()


@dataclass(eq=False, kw_only=True)
class AIRiskAssessmentRoot(AggregateRoot):
    tenant_id: str
    assessment_ref: str
    subject_ref: str
    risk_types: tuple[str, ...]
    severity: str
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def evaluate(
        cls,
        *,
        tenant_id: str,
        assessment_ref: str,
        subject_ref: str,
        risk_types: tuple[str, ...] | None = None,
        severity: str = "high",
    ) -> AIRiskAssessmentRoot:
        if not tenant_id.strip():
            raise ValueError("ii.ai_gov.risk_tenant_required")
        risks = risk_types or (
            "model_risk",
            "data_risk",
            "security_risk",
            "operational_risk",
            "compliance_risk",
            "autonomy_risk",
        )
        if len(risks) < 3:
            raise ValueError("ii.ai_gov.risk_assessment_incomplete")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            assessment_ref=assessment_ref.strip(),
            subject_ref=subject_ref.strip(),
            risk_types=tuple(risks),
            severity=severity.strip(),
            status="evaluated",
        )
        root.pending_events.append("RiskDetected")
        root.history.append({"event": "RiskDetected"})
        return root


@dataclass(eq=False, kw_only=True)
class AIThreatProtectionCaseRoot(AggregateRoot):
    tenant_id: str
    case_ref: str
    threat_type: str
    blocked: bool
    input_validated: bool
    output_filtered: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def protect(
        cls,
        *,
        tenant_id: str,
        case_ref: str,
        threat_type: str = "prompt_injection",
        blocked: bool = True,
        input_validated: bool = True,
        output_filtered: bool = True,
    ) -> AIThreatProtectionCaseRoot:
        if not tenant_id.strip():
            raise ValueError("ii.ai_gov.threat_tenant_required")
        threat = threat_type.strip().lower()
        if threat not in AI_THREATS:
            raise ValueError("ii.ai_gov.threat_type_invalid")
        if not (input_validated and output_filtered):
            raise ValueError("ii.ai_gov.threat_protection_incomplete")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            case_ref=case_ref.strip(),
            threat_type=threat,
            blocked=blocked,
            input_validated=True,
            output_filtered=True,
            status="protected",
        )
        if blocked:
            root.pending_events.append("PolicyViolationDetected")
        root.history.append({"event": "ThreatProtected"})
        return root


@dataclass(eq=False, kw_only=True)
class AutonomousActionGovernanceRoot(AggregateRoot):
    tenant_id: str
    action_ref: str
    autonomy_level: str
    policy_validated: bool
    risk_assessed: bool
    audit_logged: bool
    controllable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(
        cls,
        *,
        tenant_id: str,
        action_ref: str,
        autonomy_level: str = "level_2_ai_executes_with_approval",
        policy_validated: bool = True,
        risk_assessed: bool = True,
        audit_logged: bool = True,
        controllable: bool = True,
    ) -> AutonomousActionGovernanceRoot:
        if not tenant_id.strip():
            raise ValueError("ii.ai_gov.action_tenant_required")
        level = autonomy_level.strip().lower()
        if level not in AUTONOMY_LEVELS:
            raise ValueError("ii.ai_gov.autonomy_level_invalid")
        if not controllable:
            raise ValueError("ii.ai_gov.autonomous_actions_uncontrolled")
        if not (policy_validated and risk_assessed and audit_logged):
            raise ValueError("ii.ai_gov.autonomous_actions_uncontrolled")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            action_ref=action_ref.strip(),
            autonomy_level=level,
            policy_validated=True,
            risk_assessed=True,
            audit_logged=True,
            controllable=True,
            status="registered",
        )
        root.pending_events.append("AIActionAudited")
        root.history.append({"event": "AIActionAudited"})
        return root

    def is_uncontrolled(self) -> bool:
        return (
            not self.controllable
            or not self.policy_validated
            or not self.risk_assessed
            or not self.audit_logged
        )


@dataclass(eq=False, kw_only=True)
class AIAuditComplianceRecordRoot(AggregateRoot):
    tenant_id: str
    record_ref: str
    audit_complete: bool
    evidence_refs: tuple[str, ...]
    human_override_logged: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def record(
        cls,
        *,
        tenant_id: str,
        record_ref: str,
        audit_complete: bool = True,
        evidence_refs: tuple[str, ...] | None = None,
        human_override_logged: bool = True,
    ) -> AIAuditComplianceRecordRoot:
        if not tenant_id.strip():
            raise ValueError("ii.ai_gov.audit_tenant_required")
        refs = tuple(evidence_refs) if evidence_refs is not None else ("ev-1",)
        if not audit_complete or not refs:
            raise ValueError("ii.ai_gov.audit_trails_incomplete")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            record_ref=record_ref.strip(),
            audit_complete=True,
            evidence_refs=refs,
            human_override_logged=human_override_logged,
            status="recorded",
        )
        root.pending_events.append("AIActionAudited")
        root.history.append({"event": "AIActionAudited"})
        return root

    def audit_incomplete(self) -> bool:
        return not self.audit_complete or len(self.evidence_refs) == 0
