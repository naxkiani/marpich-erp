"""P211-P QA/governance/DoD aggregates — quality-gate invariants."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class DsAutomatedTestingRoot(AggregateRoot):
    tenant_id: str
    plan_ref: str
    automated: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def execute(
        cls, *, tenant_id: str, plan_ref: str, automated: bool = True
    ) -> DsAutomatedTestingRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.qa.tenant_required")
        if not automated:
            raise ValueError("data_security.qa.testing_is_manual_only")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            plan_ref=plan_ref.strip(),
            automated=True,
            status="executed",
        )
        root.pending_events.append("TestStarted")
        root.pending_events.append("TestCompleted")
        root.pending_events.append("ManualOnlyTestingRejected")
        root.history.append({"event": "TestingAutomated"})
        return root

    def is_manual_only(self) -> bool:
        return not self.automated


@dataclass(eq=False, kw_only=True)
class DsAvailableComplianceEvidenceRoot(AggregateRoot):
    tenant_id: str
    evidence_ref: str
    available: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def collect(
        cls, *, tenant_id: str, evidence_ref: str, available: bool = True
    ) -> DsAvailableComplianceEvidenceRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.qa.evidence_tenant_required")
        if not available:
            raise ValueError(
                "data_security.qa.compliance_evidence_is_unavailable"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            evidence_ref=evidence_ref.strip(),
            available=True,
            status="available",
        )
        root.pending_events.append("ComplianceApproved")
        root.pending_events.append("UnavailableComplianceEvidenceRejected")
        root.history.append({"event": "ComplianceEvidenceAvailable"})
        return root

    def is_unavailable(self) -> bool:
        return not self.available


@dataclass(eq=False, kw_only=True)
class DsPresentSecurityValidationRoot(AggregateRoot):
    tenant_id: str
    validation_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def validate(
        cls, *, tenant_id: str, validation_ref: str, present: bool = True
    ) -> DsPresentSecurityValidationRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.qa.security_tenant_required")
        if not present:
            raise ValueError(
                "data_security.qa.security_validation_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            validation_ref=validation_ref.strip(),
            present=True,
            status="validated",
        )
        root.pending_events.append("ControlValidated")
        root.pending_events.append("MissingSecurityValidationRejected")
        root.history.append({"event": "SecurityValidationPresent"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DsClearGovernanceOwnershipRoot(AggregateRoot):
    tenant_id: str
    control_ref: str
    clear: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def assign(
        cls, *, tenant_id: str, control_ref: str, clear: bool = True
    ) -> DsClearGovernanceOwnershipRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.qa.gov_tenant_required")
        if not clear:
            raise ValueError(
                "data_security.qa.governance_ownership_is_unclear"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            control_ref=control_ref.strip(),
            clear=True,
            status="owned",
        )
        root.pending_events.append("ControlValidated")
        root.pending_events.append("UnclearGovernanceOwnershipRejected")
        root.history.append({"event": "GovernanceOwnershipClear"})
        return root

    def is_unclear(self) -> bool:
        return not self.clear


@dataclass(eq=False, kw_only=True)
class DsTrackableRisksRoot(AggregateRoot):
    tenant_id: str
    risk_ref: str
    trackable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def track(
        cls, *, tenant_id: str, risk_ref: str, trackable: bool = True
    ) -> DsTrackableRisksRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.qa.risk_tenant_required")
        if not trackable:
            raise ValueError("data_security.qa.risks_cannot_be_tracked")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            risk_ref=risk_ref.strip(),
            trackable=True,
            status="tracked",
        )
        root.pending_events.append("FindingCreated")
        root.pending_events.append("RiskAccepted")
        root.pending_events.append("UntrackableRisksRejected")
        root.history.append({"event": "RisksTrackable"})
        return root

    def cannot_be_tracked(self) -> bool:
        return not self.trackable


@dataclass(eq=False, kw_only=True)
class DsDefinedProductionReadinessRoot(AggregateRoot):
    tenant_id: str
    readiness_ref: str
    defined: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def certify(
        cls, *, tenant_id: str, readiness_ref: str, defined: bool = True
    ) -> DsDefinedProductionReadinessRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.qa.readiness_tenant_required")
        if not defined:
            raise ValueError(
                "data_security.qa.production_readiness_is_undefined"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            readiness_ref=readiness_ref.strip(),
            defined=True,
            status="certified",
        )
        root.pending_events.append("ReleaseApproved")
        root.pending_events.append("UndefinedProductionReadinessRejected")
        root.history.append({"event": "ProductionReadinessDefined"})
        return root

    def is_undefined(self) -> bool:
        return not self.defined


@dataclass(eq=False, kw_only=True)
class DsFindingCreatedRoot(AggregateRoot):
    tenant_id: str
    finding_ref: str
    created: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def open(
        cls, *, tenant_id: str, finding_ref: str, created: bool = True
    ) -> DsFindingCreatedRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.qa.finding_tenant_required")
        if not created:
            raise ValueError("data_security.qa.finding_not_created")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            finding_ref=finding_ref.strip(),
            created=True,
            status="open",
        )
        root.pending_events.append("FindingCreated")
        root.history.append({"event": "FindingCreated"})
        return root


@dataclass(eq=False, kw_only=True)
class DsReleaseApprovedRoot(AggregateRoot):
    tenant_id: str
    release_ref: str
    approved: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def approve(
        cls, *, tenant_id: str, release_ref: str, approved: bool = True
    ) -> DsReleaseApprovedRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.qa.release_tenant_required")
        if not approved:
            raise ValueError("data_security.qa.release_not_approved")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            release_ref=release_ref.strip(),
            approved=True,
            status="approved",
        )
        root.pending_events.append("ReleaseApproved")
        root.history.append({"event": "ReleaseApproved"})
        return root
