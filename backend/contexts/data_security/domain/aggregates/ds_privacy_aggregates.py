"""P211-I Privacy intelligence aggregates — quality-gate invariants."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class DsDiscoverablePersonalDataRoot(AggregateRoot):
    tenant_id: str
    asset_ref: str
    discoverable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def discover(
        cls, *, tenant_id: str, asset_ref: str, discoverable: bool = True
    ) -> DsDiscoverablePersonalDataRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.privacy.tenant_required")
        if not discoverable:
            raise ValueError(
                "data_security.privacy.personal_data_cannot_be_discovered"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            asset_ref=asset_ref.strip(),
            discoverable=True,
            status="discovered",
        )
        root.pending_events.append("PersonalDataDetected")
        root.pending_events.append("UndiscoverablePersonalDataRejected")
        root.history.append({"event": "PersonalDataDiscovered"})
        return root

    def is_undiscoverable(self) -> bool:
        return not self.discoverable


@dataclass(eq=False, kw_only=True)
class DsTrackableConsentRoot(AggregateRoot):
    tenant_id: str
    consent_ref: str
    trackable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def track(
        cls, *, tenant_id: str, consent_ref: str, trackable: bool = True
    ) -> DsTrackableConsentRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.privacy.consent_tenant_required")
        if not trackable:
            raise ValueError("data_security.privacy.consent_cannot_be_tracked")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            consent_ref=consent_ref.strip(),
            trackable=True,
            status="tracked",
        )
        root.pending_events.append("ConsentGranted")
        root.pending_events.append("UntrackableConsentRejected")
        root.history.append({"event": "ConsentTracked"})
        return root

    def is_untrackable(self) -> bool:
        return not self.trackable


@dataclass(eq=False, kw_only=True)
class DsMeasurablePrivacyRiskRoot(AggregateRoot):
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
        score: float = 0.35,
    ) -> DsMeasurablePrivacyRiskRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.privacy.risk_tenant_required")
        if not measurable:
            raise ValueError(
                "data_security.privacy.privacy_risks_cannot_be_measured"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            risk_ref=risk_ref.strip(),
            measurable=True,
            score=score,
            status="measured",
        )
        root.pending_events.append("PrivacyRiskIdentified")
        root.pending_events.append("UnmeasurablePrivacyRiskRejected")
        root.history.append({"event": "PrivacyRiskMeasured"})
        return root

    def is_unmeasurable(self) -> bool:
        return not self.measurable


@dataclass(eq=False, kw_only=True)
class DsVisibleProcessingRoot(AggregateRoot):
    tenant_id: str
    activity_ref: str
    visible: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(
        cls, *, tenant_id: str, activity_ref: str, visible: bool = True
    ) -> DsVisibleProcessingRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.privacy.proc_tenant_required")
        if not visible:
            raise ValueError(
                "data_security.privacy.data_processing_is_invisible"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            activity_ref=activity_ref.strip(),
            visible=True,
            status="registered",
        )
        root.pending_events.append("ProcessingActivityRegistered")
        root.pending_events.append("InvisibleProcessingRejected")
        root.history.append({"event": "ProcessingVisible"})
        return root

    def is_invisible(self) -> bool:
        return not self.visible


@dataclass(eq=False, kw_only=True)
class DsMappedObligationsRoot(AggregateRoot):
    tenant_id: str
    obligation_ref: str
    mapped: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def map(
        cls, *, tenant_id: str, obligation_ref: str, mapped: bool = True
    ) -> DsMappedObligationsRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.privacy.obl_tenant_required")
        if not mapped:
            raise ValueError(
                "data_security.privacy.regulatory_obligations_are_unmapped"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            obligation_ref=obligation_ref.strip(),
            mapped=True,
            status="mapped",
        )
        root.pending_events.append("ObligationMapped")
        root.pending_events.append("ComplianceEvidenceGenerated")
        root.pending_events.append("UnmappedObligationsRejected")
        root.history.append({"event": "ObligationMapped"})
        return root

    def is_unmapped(self) -> bool:
        return not self.mapped


@dataclass(eq=False, kw_only=True)
class DsManagedAiPrivacyRoot(AggregateRoot):
    tenant_id: str
    ai_ref: str
    managed: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def govern(
        cls, *, tenant_id: str, ai_ref: str, managed: bool = True
    ) -> DsManagedAiPrivacyRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.privacy.ai_tenant_required")
        if not managed:
            raise ValueError(
                "data_security.privacy.ai_privacy_risks_are_unmanaged"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            ai_ref=ai_ref.strip(),
            managed=True,
            status="managed",
        )
        root.pending_events.append("PrivacyRiskIdentified")
        root.pending_events.append("UnmanagedAiPrivacyRejected")
        root.history.append({"event": "AiPrivacyManaged"})
        return root

    def is_unmanaged(self) -> bool:
        return not self.managed


@dataclass(eq=False, kw_only=True)
class DsConsentWithdrawnRoot(AggregateRoot):
    tenant_id: str
    consent_ref: str
    withdrawn: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def withdraw(
        cls, *, tenant_id: str, consent_ref: str, withdrawn: bool = True
    ) -> DsConsentWithdrawnRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.privacy.wd_tenant_required")
        if not withdrawn:
            raise ValueError("data_security.privacy.consent_not_withdrawn")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            consent_ref=consent_ref.strip(),
            withdrawn=True,
            status="withdrawn",
        )
        root.pending_events.append("ConsentWithdrawn")
        root.history.append({"event": "ConsentWithdrawn"})
        return root


@dataclass(eq=False, kw_only=True)
class DsAssessmentCompletedRoot(AggregateRoot):
    tenant_id: str
    assessment_ref: str
    completed: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def complete(
        cls, *, tenant_id: str, assessment_ref: str, completed: bool = True
    ) -> DsAssessmentCompletedRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.privacy.assess_tenant_required")
        if not completed:
            raise ValueError("data_security.privacy.assessment_not_completed")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            assessment_ref=assessment_ref.strip(),
            completed=True,
            status="completed",
        )
        root.pending_events.append("AssessmentCompleted")
        root.history.append({"event": "AssessmentCompleted"})
        return root
