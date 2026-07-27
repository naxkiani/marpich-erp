"""P212-N Deploy aggregates — quality-gate invariants."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


def _tid(tenant_id: str, code: str) -> str:
    if not tenant_id.strip():
        raise ValueError(code)
    return tenant_id.strip()


@dataclass(eq=False, kw_only=True)
class DgDeployCloudNativeRoot(AggregateRoot):
    tenant_id: str
    cloud_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(
        cls, *, tenant_id: str, cloud_ref: str, present: bool = True
    ) -> "DgDeployCloudNativeRoot":
        tid = _tid(tenant_id, "data_governance.deploy.tenant_0_required")
        if not present:
            raise ValueError(
                "data_governance.deploy.cloud_native_deployment_architecture_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            cloud_ref=cloud_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("DeploymentCreatedEvent")
        root.history.append({"event": "DgDeployCloudNativeRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgDeployKubernetesRoot(AggregateRoot):
    tenant_id: str
    k8s_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, k8s_ref: str, present: bool = True
    ) -> "DgDeployKubernetesRoot":
        tid = _tid(tenant_id, "data_governance.deploy.tenant_1_required")
        if not present:
            raise ValueError(
                "data_governance.deploy.kubernetes_platform_architecture_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            k8s_ref=k8s_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("DeploymentCompletedEvent")
        root.history.append({"event": "DgDeployKubernetesRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgDeployDevSecOpsRoot(AggregateRoot):
    tenant_id: str
    pipeline_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, pipeline_ref: str, present: bool = True
    ) -> "DgDeployDevSecOpsRoot":
        tid = _tid(tenant_id, "data_governance.deploy.tenant_2_required")
        if not present:
            raise ValueError(
                "data_governance.deploy.devsecops_platform_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            pipeline_ref=pipeline_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("SecurityValidationPassedEvent")
        root.history.append({"event": "DgDeployDevSecOpsRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgDeployGitOpsRoot(AggregateRoot):
    tenant_id: str
    gitops_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, gitops_ref: str, present: bool = True
    ) -> "DgDeployGitOpsRoot":
        tid = _tid(tenant_id, "data_governance.deploy.tenant_3_required")
        if not present:
            raise ValueError(
                "data_governance.deploy.gitops_architecture_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            gitops_ref=gitops_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("DeploymentStartedEvent")
        root.history.append({"event": "DgDeployGitOpsRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgDeployIacRoot(AggregateRoot):
    tenant_id: str
    iac_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, iac_ref: str, present: bool = True
    ) -> "DgDeployIacRoot":
        tid = _tid(tenant_id, "data_governance.deploy.tenant_4_required")
        if not present:
            raise ValueError(
                "data_governance.deploy.infrastructure_as_code_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            iac_ref=iac_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("DeploymentCreatedEvent")
        root.history.append({"event": "DgDeployIacRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgDeployServiceMeshRoot(AggregateRoot):
    tenant_id: str
    mesh_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, mesh_ref: str, present: bool = True
    ) -> "DgDeployServiceMeshRoot":
        tid = _tid(tenant_id, "data_governance.deploy.tenant_5_required")
        if not present:
            raise ValueError(
                "data_governance.deploy.service_mesh_architecture_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            mesh_ref=mesh_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("DeploymentCompletedEvent")
        root.history.append({"event": "DgDeployServiceMeshRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgDeployScalabilityRoot(AggregateRoot):
    tenant_id: str
    scale_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def confirm(
        cls, *, tenant_id: str, scale_ref: str, present: bool = True
    ) -> "DgDeployScalabilityRoot":
        tid = _tid(tenant_id, "data_governance.deploy.tenant_6_required")
        if not present:
            raise ValueError(
                "data_governance.deploy.scalability_architecture_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            scale_ref=scale_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("ScalingTriggeredEvent")
        root.history.append({"event": "DgDeployScalabilityRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgDeployHaRoot(AggregateRoot):
    tenant_id: str
    ha_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def confirm(
        cls, *, tenant_id: str, ha_ref: str, present: bool = True
    ) -> "DgDeployHaRoot":
        tid = _tid(tenant_id, "data_governance.deploy.tenant_7_required")
        if not present:
            raise ValueError(
                "data_governance.deploy.high_availability_architecture_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            ha_ref=ha_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("RecoveryCompletedEvent")
        root.history.append({"event": "DgDeployHaRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgDeployObservabilityRoot(AggregateRoot):
    tenant_id: str
    obs_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, obs_ref: str, present: bool = True
    ) -> "DgDeployObservabilityRoot":
        tid = _tid(tenant_id, "data_governance.deploy.tenant_8_required")
        if not present:
            raise ValueError(
                "data_governance.deploy.observability_platform_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            obs_ref=obs_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("IncidentDetectedEvent")
        root.history.append({"event": "DgDeployObservabilityRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgDeployAiopsRoot(AggregateRoot):
    tenant_id: str
    aiops_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, aiops_ref: str, present: bool = True
    ) -> "DgDeployAiopsRoot":
        tid = _tid(tenant_id, "data_governance.deploy.tenant_9_required")
        if not present:
            raise ValueError(
                "data_governance.deploy.aiops_operations_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            aiops_ref=aiops_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("ScalingExecutedEvent")
        root.history.append({"event": "DgDeployAiopsRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgDeploySecurityRoot(AggregateRoot):
    tenant_id: str
    security_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def integrate(
        cls, *, tenant_id: str, security_ref: str, present: bool = True
    ) -> "DgDeploySecurityRoot":
        tid = _tid(tenant_id, "data_governance.deploy.tenant_10_required")
        if not present:
            raise ValueError(
                "data_governance.deploy.security_integration_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            security_ref=security_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("SecurityValidationPassedEvent")
        root.history.append({"event": "DgDeploySecurityRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgDeployMultiRegionRoot(AggregateRoot):
    tenant_id: str
    region_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def confirm(
        cls, *, tenant_id: str, region_ref: str, present: bool = True
    ) -> "DgDeployMultiRegionRoot":
        tid = _tid(tenant_id, "data_governance.deploy.tenant_11_required")
        if not present:
            raise ValueError(
                "data_governance.deploy.multi_region_architecture_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            region_ref=region_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("DeploymentCompletedEvent")
        root.history.append({"event": "DgDeployMultiRegionRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgDeployCqrsOpsRoot(AggregateRoot):
    tenant_id: str
    cqrs_ops_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def integrate(
        cls, *, tenant_id: str, cqrs_ops_ref: str, present: bool = True
    ) -> "DgDeployCqrsOpsRoot":
        tid = _tid(tenant_id, "data_governance.deploy.tenant_12_required")
        if not present:
            raise ValueError(
                "data_governance.deploy.cqrs_operational_integration_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            cqrs_ops_ref=cqrs_ops_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("DeploymentStartedEvent")
        root.history.append({"event": "DgDeployCqrsOpsRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgDeployReliabilityRoot(AggregateRoot):
    tenant_id: str
    reliability_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def confirm(
        cls, *, tenant_id: str, reliability_ref: str, present: bool = True
    ) -> "DgDeployReliabilityRoot":
        tid = _tid(tenant_id, "data_governance.deploy.tenant_13_required")
        if not present:
            raise ValueError(
                "data_governance.deploy.enterprise_reliability_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            reliability_ref=reliability_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("RecoveryCompletedEvent")
        root.history.append({"event": "DgDeployReliabilityRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present
