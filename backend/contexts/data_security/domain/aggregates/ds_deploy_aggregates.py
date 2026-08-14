"""P211-O Deploy/DevSecOps aggregates — quality-gate invariants."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class DsAutomatedDeploymentRoot(AggregateRoot):
    tenant_id: str
    release_ref: str
    automated: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def promote(
        cls, *, tenant_id: str, release_ref: str, automated: bool = True
    ) -> DsAutomatedDeploymentRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.deploy.tenant_required")
        if not automated:
            raise ValueError("data_security.deploy.deployment_is_manual")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            release_ref=release_ref.strip(),
            automated=True,
            status="promoted",
        )
        root.pending_events.append("EnvironmentPromoted")
        root.pending_events.append("ReleaseApproved")
        root.pending_events.append("ManualDeploymentRejected")
        root.history.append({"event": "DeploymentAutomated"})
        return root

    def is_manual(self) -> bool:
        return not self.automated


@dataclass(eq=False, kw_only=True)
class DsSecurityScanningRoot(AggregateRoot):
    tenant_id: str
    scan_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enforce(
        cls, *, tenant_id: str, scan_ref: str, present: bool = True
    ) -> DsSecurityScanningRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.deploy.scan_tenant_required")
        if not present:
            raise ValueError(
                "data_security.deploy.security_scanning_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            scan_ref=scan_ref.strip(),
            present=True,
            status="scanned",
        )
        root.pending_events.append("RuntimePolicyEnforced")
        root.pending_events.append("MissingSecurityScanningRejected")
        root.history.append({"event": "SecurityScanningPresent"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DsScalableInfrastructureRoot(AggregateRoot):
    tenant_id: str
    workload_ref: str
    scalable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def scale(
        cls, *, tenant_id: str, workload_ref: str, scalable: bool = True
    ) -> DsScalableInfrastructureRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.deploy.scale_tenant_required")
        if not scalable:
            raise ValueError(
                "data_security.deploy.infrastructure_cannot_scale"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            workload_ref=workload_ref.strip(),
            scalable=True,
            status="scaled",
        )
        root.pending_events.append("WorkloadScaled")
        root.pending_events.append("UnscalableInfrastructureRejected")
        root.history.append({"event": "InfrastructureScalable"})
        return root

    def cannot_scale(self) -> bool:
        return not self.scalable


@dataclass(eq=False, kw_only=True)
class DsCompleteMonitoringRoot(AggregateRoot):
    tenant_id: str
    monitor_ref: str
    complete: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, monitor_ref: str, complete: bool = True
    ) -> DsCompleteMonitoringRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.deploy.monitor_tenant_required")
        if not complete:
            raise ValueError(
                "data_security.deploy.monitoring_is_incomplete"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            monitor_ref=monitor_ref.strip(),
            complete=True,
            status="complete",
        )
        root.pending_events.append("AnomalyDetected")
        root.pending_events.append("IncompleteMonitoringRejected")
        root.history.append({"event": "MonitoringComplete"})
        return root

    def is_incomplete(self) -> bool:
        return not self.complete


@dataclass(eq=False, kw_only=True)
class DsDefinedDisasterRecoveryRoot(AggregateRoot):
    tenant_id: str
    dr_ref: str
    defined: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def define(
        cls, *, tenant_id: str, dr_ref: str, defined: bool = True
    ) -> DsDefinedDisasterRecoveryRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.deploy.dr_tenant_required")
        if not defined:
            raise ValueError(
                "data_security.deploy.disaster_recovery_is_undefined"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            dr_ref=dr_ref.strip(),
            defined=True,
            status="defined",
        )
        root.pending_events.append("DrDrillCompleted")
        root.pending_events.append("FailoverTriggered")
        root.pending_events.append("UndefinedDisasterRecoveryRejected")
        root.history.append({"event": "DisasterRecoveryDefined"})
        return root

    def is_undefined(self) -> bool:
        return not self.defined


@dataclass(eq=False, kw_only=True)
class DsPresentRuntimeSecurityRoot(AggregateRoot):
    tenant_id: str
    policy_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enforce(
        cls, *, tenant_id: str, policy_ref: str, present: bool = True
    ) -> DsPresentRuntimeSecurityRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.deploy.runtime_tenant_required")
        if not present:
            raise ValueError(
                "data_security.deploy.runtime_security_is_absent"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            policy_ref=policy_ref.strip(),
            present=True,
            status="enforced",
        )
        root.pending_events.append("RuntimePolicyEnforced")
        root.pending_events.append("AbsentRuntimeSecurityRejected")
        root.history.append({"event": "RuntimeSecurityPresent"})
        return root

    def is_absent(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DsComplianceEvidenceRoot(AggregateRoot):
    tenant_id: str
    evidence_ref: str
    collected: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def collect(
        cls, *, tenant_id: str, evidence_ref: str, collected: bool = True
    ) -> DsComplianceEvidenceRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.deploy.evidence_tenant_required")
        if not collected:
            raise ValueError("data_security.deploy.evidence_not_collected")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            evidence_ref=evidence_ref.strip(),
            collected=True,
            status="collected",
        )
        root.pending_events.append("ComplianceEvidenceCollected")
        root.history.append({"event": "ComplianceEvidenceCollected"})
        return root


@dataclass(eq=False, kw_only=True)
class DsAnomalyDetectedRoot(AggregateRoot):
    tenant_id: str
    anomaly_ref: str
    detected: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def detect(
        cls, *, tenant_id: str, anomaly_ref: str, detected: bool = True
    ) -> DsAnomalyDetectedRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.deploy.anomaly_tenant_required")
        if not detected:
            raise ValueError("data_security.deploy.anomaly_not_detected")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            anomaly_ref=anomaly_ref.strip(),
            detected=True,
            status="detected",
        )
        root.pending_events.append("AnomalyDetected")
        root.history.append({"event": "AnomalyDetected"})
        return root
