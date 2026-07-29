"""P211-F DSPM aggregates — quality-gate invariants."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class DsKnownAssetsRoot(AggregateRoot):
    tenant_id: str
    estate_ref: str
    known: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def discover(
        cls, *, tenant_id: str, estate_ref: str, known: bool = True
    ) -> DsKnownAssetsRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.dspm.tenant_required")
        if not known:
            raise ValueError("data_security.dspm.data_assets_are_unknown")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            estate_ref=estate_ref.strip(),
            known=True,
            status="known",
        )
        root.pending_events.append("DataAssetDiscovered")
        root.pending_events.append("UnknownAssetsRejected")
        root.history.append({"event": "AssetsKnown"})
        return root

    def is_unknown(self) -> bool:
        return not self.known


@dataclass(eq=False, kw_only=True)
class DsMeasurablePostureRoot(AggregateRoot):
    tenant_id: str
    posture_ref: str
    measurable: bool
    score: float
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def assess(
        cls,
        *,
        tenant_id: str,
        posture_ref: str,
        measurable: bool = True,
        score: float = 0.85,
    ) -> DsMeasurablePostureRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.dspm.posture_tenant_required")
        if not measurable:
            raise ValueError(
                "data_security.dspm.security_posture_cannot_be_measured"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            posture_ref=posture_ref.strip(),
            measurable=True,
            score=score,
            status="measured",
        )
        root.pending_events.append("RiskCalculated")
        root.pending_events.append("PostureScoreUpdated")
        root.pending_events.append("UnmeasurablePostureRejected")
        root.history.append({"event": "PostureMeasured"})
        return root

    def is_unmeasurable(self) -> bool:
        return not self.measurable


@dataclass(eq=False, kw_only=True)
class DsVisibleExposureRoot(AggregateRoot):
    tenant_id: str
    exposure_ref: str
    visible: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def detect(
        cls, *, tenant_id: str, exposure_ref: str, visible: bool = True
    ) -> DsVisibleExposureRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.dspm.exp_tenant_required")
        if not visible:
            raise ValueError(
                "data_security.dspm.exposure_risks_are_invisible"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            exposure_ref=exposure_ref.strip(),
            visible=True,
            status="visible",
        )
        root.pending_events.append("ExposureFound")
        root.pending_events.append("InvisibleExposureRejected")
        root.history.append({"event": "ExposureVisible"})
        return root

    def is_invisible(self) -> bool:
        return not self.visible


@dataclass(eq=False, kw_only=True)
class DsOwnedFindingRoot(AggregateRoot):
    tenant_id: str
    finding_ref: str
    owned: bool
    owner_ref: str
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        finding_ref: str,
        owner_ref: str = "owner-1",
        owned: bool = True,
    ) -> DsOwnedFindingRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.dspm.find_tenant_required")
        if not owned or not owner_ref.strip():
            raise ValueError(
                "data_security.dspm.findings_have_no_ownership"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            finding_ref=finding_ref.strip(),
            owned=True,
            owner_ref=owner_ref.strip(),
            status="owned",
        )
        root.pending_events.append("ExposureFound")
        root.pending_events.append("UnownedFindingsRejected")
        root.history.append({"event": "FindingOwned"})
        return root

    def is_unowned(self) -> bool:
        return not self.owned


@dataclass(eq=False, kw_only=True)
class DsAutonomousRemediationRoot(AggregateRoot):
    tenant_id: str
    action_ref: str
    autonomous_path: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def generate(
        cls,
        *,
        tenant_id: str,
        action_ref: str,
        autonomous_path: bool = True,
    ) -> DsAutonomousRemediationRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.dspm.rem_tenant_required")
        if not autonomous_path:
            raise ValueError(
                "data_security.dspm.remediation_is_manual_only"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            action_ref=action_ref.strip(),
            autonomous_path=True,
            status="generated",
        )
        root.pending_events.append("RemediationCreated")
        root.pending_events.append("ManualOnlyRemediationRejected")
        root.history.append({"event": "RemediationAutonomous"})
        return root

    def is_manual_only(self) -> bool:
        return not self.autonomous_path


@dataclass(eq=False, kw_only=True)
class DsContinuousAssessmentRoot(AggregateRoot):
    tenant_id: str
    assessment_ref: str
    available: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def run(
        cls,
        *,
        tenant_id: str,
        assessment_ref: str,
        available: bool = True,
    ) -> DsContinuousAssessmentRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.dspm.cont_tenant_required")
        if not available:
            raise ValueError(
                "data_security.dspm.continuous_assessment_is_unavailable"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            assessment_ref=assessment_ref.strip(),
            available=True,
            status="running",
        )
        root.pending_events.append("ContinuousAssessmentCompleted")
        root.pending_events.append("UnavailableAssessmentRejected")
        root.history.append({"event": "AssessmentContinuous"})
        return root

    def is_unavailable(self) -> bool:
        return not self.available


@dataclass(eq=False, kw_only=True)
class DsControlAppliedRoot(AggregateRoot):
    tenant_id: str
    control_ref: str
    applied: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def apply(
        cls, *, tenant_id: str, control_ref: str, applied: bool = True
    ) -> DsControlAppliedRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.dspm.ctrl_tenant_required")
        if not applied:
            raise ValueError("data_security.dspm.control_not_applied")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            control_ref=control_ref.strip(),
            applied=True,
            status="applied",
        )
        root.pending_events.append("ControlApplied")
        root.history.append({"event": "ControlApplied"})
        return root


@dataclass(eq=False, kw_only=True)
class DsSensitiveDetectedRoot(AggregateRoot):
    tenant_id: str
    detection_ref: str
    detected: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def detect(
        cls, *, tenant_id: str, detection_ref: str, detected: bool = True
    ) -> DsSensitiveDetectedRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.dspm.sens_tenant_required")
        if not detected:
            raise ValueError("data_security.dspm.sensitive_not_detected")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            detection_ref=detection_ref.strip(),
            detected=True,
            status="detected",
        )
        root.pending_events.append("SensitiveDataDetected")
        root.history.append({"event": "SensitiveDetected"})
        return root
