"""P209-M AI Security, Cryptographic Governance & Compliance aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class SecretsGovAiExplainableRoot(AggregateRoot):
    """AI security decisions must be explainable."""

    tenant_id: str
    decision_ref: str
    explainable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def record(
        cls,
        *,
        tenant_id: str,
        decision_ref: str,
        explainable: bool = True,
    ) -> SecretsGovAiExplainableRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.gov.ai_tenant_required")
        if not explainable:
            raise ValueError("secrets.gov.ai_security_decisions_not_explainable")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            decision_ref=decision_ref.strip(),
            explainable=True,
            status="explained",
        )
        root.pending_events.append("AiDecisionExplained")
        root.history.append({"event": "AiDecisionExplained"})
        return root

    def is_unexplainable(self) -> bool:
        return not self.explainable


@dataclass(eq=False, kw_only=True)
class SecretsGovPolicyManagedRoot(AggregateRoot):
    """Cryptographic policies must be managed."""

    tenant_id: str
    policy_ref: str
    managed: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def manage(
        cls,
        *,
        tenant_id: str,
        policy_ref: str,
        managed: bool = True,
    ) -> SecretsGovPolicyManagedRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.gov.policy_tenant_required")
        if not managed:
            raise ValueError("secrets.gov.cryptographic_policies_unmanaged")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            policy_ref=policy_ref.strip(),
            managed=True,
            status="managed",
        )
        root.pending_events.append("CryptoPolicyManaged")
        root.pending_events.append("PolicyCreated")
        root.history.append({"event": "CryptoPolicyManaged"})
        return root

    def is_unmanaged(self) -> bool:
        return not self.managed


@dataclass(eq=False, kw_only=True)
class SecretsGovEvidenceAutomatedRoot(AggregateRoot):
    """Compliance evidence must not be manual only."""

    tenant_id: str
    evidence_ref: str
    automated: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def automate(
        cls,
        *,
        tenant_id: str,
        evidence_ref: str,
        automated: bool = True,
    ) -> SecretsGovEvidenceAutomatedRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.gov.evidence_tenant_required")
        if not automated:
            raise ValueError("secrets.gov.compliance_evidence_manual_only")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            evidence_ref=evidence_ref.strip(),
            automated=True,
            status="automated",
        )
        root.pending_events.append("EvidenceAutomated")
        root.pending_events.append("ComplianceValidated")
        root.history.append({"event": "EvidenceAutomated"})
        return root

    def is_manual_only(self) -> bool:
        return not self.automated


@dataclass(eq=False, kw_only=True)
class SecretsGovRiskMeasurableRoot(AggregateRoot):
    """Risks must be measurable."""

    tenant_id: str
    risk_ref: str
    measurable: bool
    score: float
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def measure(
        cls,
        *,
        tenant_id: str,
        risk_ref: str,
        measurable: bool = True,
        score: float = 0.0,
    ) -> SecretsGovRiskMeasurableRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.gov.risk_tenant_required")
        if not measurable:
            raise ValueError("secrets.gov.risks_cannot_be_measured")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            risk_ref=risk_ref.strip(),
            measurable=True,
            score=score,
            status="measured",
        )
        root.pending_events.append("RiskMeasured")
        root.pending_events.append("RiskDetected")
        root.history.append({"event": "RiskMeasured"})
        return root

    def cannot_be_measured(self) -> bool:
        return not self.measurable


@dataclass(eq=False, kw_only=True)
class SecretsGovOwnershipDefinedRoot(AggregateRoot):
    """Governance ownership must be defined."""

    tenant_id: str
    asset_ref: str
    ownership_defined: bool
    owner_ref: str
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def define(
        cls,
        *,
        tenant_id: str,
        asset_ref: str,
        owner_ref: str,
        ownership_defined: bool = True,
    ) -> SecretsGovOwnershipDefinedRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.gov.own_tenant_required")
        if not ownership_defined or not owner_ref.strip():
            raise ValueError("secrets.gov.governance_ownership_undefined")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            asset_ref=asset_ref.strip(),
            ownership_defined=True,
            owner_ref=owner_ref.strip(),
            status="defined",
        )
        root.pending_events.append("OwnershipDefined")
        root.history.append({"event": "OwnershipDefined"})
        return root

    def is_undefined(self) -> bool:
        return not self.ownership_defined


@dataclass(eq=False, kw_only=True)
class SecretsGovAuditCompleteRoot(AggregateRoot):
    """Audit trails must be complete."""

    tenant_id: str
    trail_ref: str
    complete: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def complete_trail(
        cls,
        *,
        tenant_id: str,
        trail_ref: str,
        complete: bool = True,
    ) -> SecretsGovAuditCompleteRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.gov.audit_tenant_required")
        if not complete:
            raise ValueError("secrets.gov.audit_trails_incomplete")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            trail_ref=trail_ref.strip(),
            complete=True,
            status="complete",
        )
        root.pending_events.append("AuditTrailComplete")
        root.pending_events.append("AuditCompleted")
        root.history.append({"event": "AuditTrailComplete"})
        return root

    def is_incomplete(self) -> bool:
        return not self.complete


@dataclass(eq=False, kw_only=True)
class SecretsGovRemediationAutomatedRoot(AggregateRoot):
    """Remediation must be automatable."""

    tenant_id: str
    remediation_ref: str
    automatable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls,
        *,
        tenant_id: str,
        remediation_ref: str,
        automatable: bool = True,
    ) -> SecretsGovRemediationAutomatedRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.gov.rem_tenant_required")
        if not automatable:
            raise ValueError("secrets.gov.remediation_cannot_be_automated")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            remediation_ref=remediation_ref.strip(),
            automatable=True,
            status="enabled",
        )
        root.pending_events.append("RemediationAutomated")
        root.pending_events.append("RemediationExecuted")
        root.history.append({"event": "RemediationAutomated"})
        return root

    def cannot_be_automated(self) -> bool:
        return not self.automatable


@dataclass(eq=False, kw_only=True)
class SecretsGovHumanOversightRoot(AggregateRoot):
    """Responsible AI human oversight via Workflow."""

    tenant_id: str
    decision_ref: str
    oversight_required: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def require(
        cls,
        *,
        tenant_id: str,
        decision_ref: str,
        oversight_required: bool = True,
    ) -> SecretsGovHumanOversightRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.gov.oversight_tenant_required")
        if not oversight_required:
            raise ValueError("secrets.gov.ai_security_decisions_not_explainable")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            decision_ref=decision_ref.strip(),
            oversight_required=True,
            status="required",
        )
        root.pending_events.append("HumanOversightRequired")
        root.pending_events.append("PolicyApproved")
        root.history.append({"event": "HumanOversightRequired"})
        return root
