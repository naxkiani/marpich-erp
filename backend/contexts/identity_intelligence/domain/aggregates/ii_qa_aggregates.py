"""P207-O QA, Governance & Definition of Done aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId

TEST_LAYERS = frozenset({"unit", "integration", "system", "enterprise_acceptance"})
GOVERNANCE_DOMAINS = frozenset(
    {"architecture", "security", "data", "ai", "operational"}
)
DOD_CRITERIA = frozenset(
    {
        "secure",
        "scalable",
        "reliable",
        "governed",
        "explainable",
        "auditable",
        "production_ready",
    }
)


@dataclass(eq=False, kw_only=True)
class IdentityTestSuitePlanRoot(AggregateRoot):
    tenant_id: str
    suite_ref: str
    layer: str
    automated: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(
        cls,
        *,
        tenant_id: str,
        suite_ref: str,
        layer: str = "unit",
        automated: bool = True,
    ) -> IdentityTestSuitePlanRoot:
        if not tenant_id.strip():
            raise ValueError("ii.qa.tenant_required")
        lyr = layer.strip().lower()
        if lyr not in TEST_LAYERS:
            raise ValueError("ii.qa.layer_invalid")
        if not automated:
            raise ValueError("ii.qa.testing_manual_only")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            suite_ref=suite_ref.strip(),
            layer=lyr,
            automated=True,
            status="registered",
        )
        root.pending_events.append("TestCompleted")
        root.history.append({"event": "TestCompleted"})
        return root

    def is_manual_only(self) -> bool:
        return not self.automated


@dataclass(eq=False, kw_only=True)
class SecurityValidationCaseRoot(AggregateRoot):
    tenant_id: str
    case_ref: str
    zero_trust: bool
    application_security: bool
    infrastructure_security: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def assess(
        cls,
        *,
        tenant_id: str,
        case_ref: str,
        zero_trust: bool = True,
        application_security: bool = True,
        infrastructure_security: bool = True,
    ) -> SecurityValidationCaseRoot:
        if not tenant_id.strip():
            raise ValueError("ii.qa.sec_tenant_required")
        if not (zero_trust and application_security and infrastructure_security):
            raise ValueError("ii.qa.security_validation_incomplete")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            case_ref=case_ref.strip(),
            zero_trust=True,
            application_security=True,
            infrastructure_security=True,
            status="validated",
        )
        root.pending_events.append("SecurityValidated")
        root.history.append({"event": "SecurityValidated"})
        return root

    def is_incomplete(self) -> bool:
        return not (
            self.zero_trust
            and self.application_security
            and self.infrastructure_security
        )


@dataclass(eq=False, kw_only=True)
class AIValidationRecordRoot(AggregateRoot):
    tenant_id: str
    record_ref: str
    explainable: bool
    policy_compliant: bool
    drift_monitored: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def validate(
        cls,
        *,
        tenant_id: str,
        record_ref: str,
        explainable: bool = True,
        policy_compliant: bool = True,
        drift_monitored: bool = True,
    ) -> AIValidationRecordRoot:
        if not tenant_id.strip():
            raise ValueError("ii.qa.ai_tenant_required")
        if not (explainable and policy_compliant and drift_monitored):
            raise ValueError("ii.qa.ai_validation_absent")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            record_ref=record_ref.strip(),
            explainable=True,
            policy_compliant=True,
            drift_monitored=True,
            status="validated",
        )
        root.history.append({"event": "AIValidationCompleted"})
        return root

    def is_absent(self) -> bool:
        return not (self.explainable and self.policy_compliant)


@dataclass(eq=False, kw_only=True)
class ReleaseGovernanceApprovalRoot(AggregateRoot):
    tenant_id: str
    approval_ref: str
    domain: str
    owner_ref: str
    test_evidence: bool
    security_evidence: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def approve(
        cls,
        *,
        tenant_id: str,
        approval_ref: str,
        domain: str,
        owner_ref: str,
        test_evidence: bool = True,
        security_evidence: bool = True,
    ) -> ReleaseGovernanceApprovalRoot:
        if not tenant_id.strip():
            raise ValueError("ii.qa.gov_tenant_required")
        d = domain.strip().lower()
        if d not in GOVERNANCE_DOMAINS:
            raise ValueError("ii.qa.governance_undefined")
        if not owner_ref.strip():
            raise ValueError("ii.qa.governance_undefined")
        if not (test_evidence and security_evidence):
            raise ValueError("ii.qa.governance_undefined")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            approval_ref=approval_ref.strip(),
            domain=d,
            owner_ref=owner_ref.strip(),
            test_evidence=True,
            security_evidence=True,
            status="approved",
        )
        root.pending_events.append("GovernanceApproved")
        root.pending_events.append("ReleaseAuthorized")
        root.history.append({"event": "GovernanceApproved"})
        return root

    def is_undefined(self) -> bool:
        return self.domain not in GOVERNANCE_DOMAINS


@dataclass(eq=False, kw_only=True)
class ComplianceEvidencePackRoot(AggregateRoot):
    tenant_id: str
    pack_ref: str
    evidence_refs: tuple[str, ...]
    local_store: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def collect(
        cls,
        *,
        tenant_id: str,
        pack_ref: str,
        evidence_refs: tuple[str, ...] | None = None,
        local_store: bool = False,
    ) -> ComplianceEvidencePackRoot:
        if not tenant_id.strip():
            raise ValueError("ii.qa.comp_tenant_required")
        refs = tuple(evidence_refs) if evidence_refs is not None else ("ev-1", "ev-2")
        if not refs:
            raise ValueError("ii.qa.compliance_evidence_missing")
        if local_store:
            raise ValueError("ii.qa.local_compliance_store")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            pack_ref=pack_ref.strip(),
            evidence_refs=refs,
            local_store=False,
            status="collected",
        )
        root.history.append({"event": "ComplianceEvidenceCollected"})
        return root

    def is_missing(self) -> bool:
        return len(self.evidence_refs) == 0


@dataclass(eq=False, kw_only=True)
class ContinuousAssuranceBaselineRoot(AggregateRoot):
    tenant_id: str
    baseline_ref: str
    regression_detection: bool
    model_degradation_detection: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def establish(
        cls,
        *,
        tenant_id: str,
        baseline_ref: str,
        regression_detection: bool = True,
        model_degradation_detection: bool = True,
    ) -> ContinuousAssuranceBaselineRoot:
        if not tenant_id.strip():
            raise ValueError("ii.qa.baseline_tenant_required")
        if not (regression_detection and model_degradation_detection):
            raise ValueError("ii.qa.continuous_assurance_incomplete")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            baseline_ref=baseline_ref.strip(),
            regression_detection=True,
            model_degradation_detection=True,
            status="active",
        )
        root.history.append({"event": "ContinuousAssuranceEstablished"})
        return root


@dataclass(eq=False, kw_only=True)
class DefinitionOfDoneCertificationRoot(AggregateRoot):
    tenant_id: str
    cert_ref: str
    criteria_met: tuple[str, ...]
    p207_series_complete: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def certify(
        cls,
        *,
        tenant_id: str,
        cert_ref: str,
        criteria_met: tuple[str, ...] | None = None,
        p207_series_complete: bool = True,
    ) -> DefinitionOfDoneCertificationRoot:
        if not tenant_id.strip():
            raise ValueError("ii.qa.cert_tenant_required")
        criteria = tuple(criteria_met or tuple(DOD_CRITERIA))
        if not set(criteria).issuperset(DOD_CRITERIA):
            raise ValueError("ii.qa.definition_of_done_incomplete")
        if not p207_series_complete:
            raise ValueError("ii.qa.p207_series_incomplete")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            cert_ref=cert_ref.strip(),
            criteria_met=criteria,
            p207_series_complete=True,
            status="certified",
        )
        root.pending_events.append("DefinitionOfDoneCertified")
        root.history.append({"event": "DefinitionOfDoneCertified"})
        return root

    def is_certified(self) -> bool:
        return set(self.criteria_met).issuperset(DOD_CRITERIA)

    def is_incomplete(self) -> bool:
        return not self.is_certified()
