"""P209-N Deployment, DevSecOps, K8s & Observability aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class SecretsDeployAutomatedRoot(AggregateRoot):
    """Deployment must not be manual."""

    tenant_id: str
    deploy_ref: str
    automated: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls,
        *,
        tenant_id: str,
        deploy_ref: str,
        automated: bool = True,
    ) -> SecretsDeployAutomatedRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.deploy.auto_tenant_required")
        if not automated:
            raise ValueError("secrets.deploy.deployment_is_manual")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            deploy_ref=deploy_ref.strip(),
            automated=True,
            status="enabled",
        )
        root.pending_events.append("DeployAutomated")
        root.pending_events.append("DeploymentStarted")
        root.history.append({"event": "DeployAutomated"})
        return root

    def is_manual(self) -> bool:
        return not self.automated


@dataclass(eq=False, kw_only=True)
class SecretsDeployK8sSecurityRoot(AggregateRoot):
    """Kubernetes security must be complete."""

    tenant_id: str
    cluster_ref: str
    complete: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def verify(
        cls,
        *,
        tenant_id: str,
        cluster_ref: str,
        complete: bool = True,
    ) -> SecretsDeployK8sSecurityRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.deploy.k8s_tenant_required")
        if not complete:
            raise ValueError("secrets.deploy.kubernetes_security_incomplete")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            cluster_ref=cluster_ref.strip(),
            complete=True,
            status="verified",
        )
        root.pending_events.append("K8sSecurityComplete")
        root.history.append({"event": "K8sSecurityComplete"})
        return root

    def is_incomplete(self) -> bool:
        return not self.complete


@dataclass(eq=False, kw_only=True)
class SecretsDeployObservabilityRoot(AggregateRoot):
    """Observability must not be missing."""

    tenant_id: str
    service_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls,
        *,
        tenant_id: str,
        service_ref: str,
        present: bool = True,
    ) -> SecretsDeployObservabilityRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.deploy.obs_tenant_required")
        if not present:
            raise ValueError("secrets.deploy.observability_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            service_ref=service_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("ObservabilityPresent")
        root.history.append({"event": "ObservabilityPresent"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class SecretsDeployCicdSecurityRoot(AggregateRoot):
    """CI/CD must include security validation."""

    tenant_id: str
    pipeline_ref: str
    secured: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def validate(
        cls,
        *,
        tenant_id: str,
        pipeline_ref: str,
        secured: bool = True,
    ) -> SecretsDeployCicdSecurityRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.deploy.cicd_tenant_required")
        if not secured:
            raise ValueError("secrets.deploy.cicd_lacks_security_validation")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            pipeline_ref=pipeline_ref.strip(),
            secured=True,
            status="validated",
        )
        root.pending_events.append("CicdSecurityValidated")
        root.history.append({"event": "CicdSecurityValidated"})
        return root

    def lacks_security(self) -> bool:
        return not self.secured


@dataclass(eq=False, kw_only=True)
class SecretsDeployScalingDefinedRoot(AggregateRoot):
    """Scaling strategy must be defined."""

    tenant_id: str
    strategy_ref: str
    defined: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def define(
        cls,
        *,
        tenant_id: str,
        strategy_ref: str,
        defined: bool = True,
    ) -> SecretsDeployScalingDefinedRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.deploy.scale_tenant_required")
        if not defined:
            raise ValueError("secrets.deploy.scaling_strategy_undefined")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            strategy_ref=strategy_ref.strip(),
            defined=True,
            status="defined",
        )
        root.pending_events.append("ScalingDefined")
        root.pending_events.append("ServiceScaled")
        root.history.append({"event": "ScalingDefined"})
        return root

    def is_undefined(self) -> bool:
        return not self.defined


@dataclass(eq=False, kw_only=True)
class SecretsDeployDrAvailableRoot(AggregateRoot):
    """Disaster recovery must be available."""

    tenant_id: str
    plan_ref: str
    available: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls,
        *,
        tenant_id: str,
        plan_ref: str,
        available: bool = True,
    ) -> SecretsDeployDrAvailableRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.deploy.dr_tenant_required")
        if not available:
            raise ValueError("secrets.deploy.disaster_recovery_unavailable")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            plan_ref=plan_ref.strip(),
            available=True,
            status="available",
        )
        root.pending_events.append("DrAvailable")
        root.pending_events.append("RecoveryStarted")
        root.history.append({"event": "DrAvailable"})
        return root

    def is_unavailable(self) -> bool:
        return not self.available


@dataclass(eq=False, kw_only=True)
class SecretsDeployIacManagedRoot(AggregateRoot):
    """Infrastructure changes must be managed."""

    tenant_id: str
    change_ref: str
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
        change_ref: str,
        managed: bool = True,
    ) -> SecretsDeployIacManagedRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.deploy.iac_tenant_required")
        if not managed:
            raise ValueError("secrets.deploy.infrastructure_changes_unmanaged")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            change_ref=change_ref.strip(),
            managed=True,
            status="managed",
        )
        root.pending_events.append("IacManaged")
        root.history.append({"event": "IacManaged"})
        return root

    def is_unmanaged(self) -> bool:
        return not self.managed


@dataclass(eq=False, kw_only=True)
class SecretsDeployZeroTrustOpsRoot(AggregateRoot):
    """Zero Trust operations for cryptographic deploy fabric."""

    tenant_id: str
    env_ref: str
    enforced: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enforce(
        cls,
        *,
        tenant_id: str,
        env_ref: str,
        enforced: bool = True,
    ) -> SecretsDeployZeroTrustOpsRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.deploy.zt_tenant_required")
        if not enforced:
            raise ValueError("secrets.deploy.kubernetes_security_incomplete")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            env_ref=env_ref.strip(),
            enforced=True,
            status="enforced",
        )
        root.pending_events.append("ZeroTrustOpsEnforced")
        root.pending_events.append("DeploymentCompleted")
        root.history.append({"event": "ZeroTrustOpsEnforced"})
        return root
