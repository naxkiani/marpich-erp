"""P207-N DevSecOps, Kubernetes & Observability aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId

K8S_NAMESPACES = frozenset(
    {
        "identity-intelligence",
        "ai-platform",
        "knowledge-platform",
        "risk-platform",
        "governance-platform",
        "observability-platform",
        "security-platform",
    }
)

OBSERVABILITY_PILLARS = frozenset({"metrics", "logs", "traces"})


@dataclass(eq=False, kw_only=True)
class KubernetesClusterBlueprintRoot(AggregateRoot):
    tenant_id: str
    cluster_ref: str
    namespaces: tuple[str, ...]
    defined: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def provision(
        cls,
        *,
        tenant_id: str,
        cluster_ref: str,
        namespaces: tuple[str, ...] | None = None,
        defined: bool = True,
    ) -> KubernetesClusterBlueprintRoot:
        if not tenant_id.strip():
            raise ValueError("ii.ops.tenant_required")
        ns = tuple(namespaces or tuple(K8S_NAMESPACES))
        if not defined or not K8S_NAMESPACES.issubset(set(ns)):
            raise ValueError("ii.ops.kubernetes_architecture_undefined")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            cluster_ref=cluster_ref.strip(),
            namespaces=ns,
            defined=True,
            status="provisioned",
        )
        root.pending_events.append("ClusterProvisioned")
        root.history.append({"event": "ClusterProvisioned"})
        return root

    def is_undefined(self) -> bool:
        return not self.defined


@dataclass(eq=False, kw_only=True)
class DevSecOpsPipelineRunRoot(AggregateRoot):
    tenant_id: str
    run_ref: str
    automated: bool
    security_integrated: bool
    image_scanned: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def run(
        cls,
        *,
        tenant_id: str,
        run_ref: str,
        automated: bool = True,
        security_integrated: bool = True,
        image_scanned: bool = True,
    ) -> DevSecOpsPipelineRunRoot:
        if not tenant_id.strip():
            raise ValueError("ii.ops.pipeline_tenant_required")
        if not automated:
            raise ValueError("ii.ops.deployment_manual")
        if not security_integrated:
            raise ValueError("ii.ops.security_separated_from_devops")
        if not image_scanned:
            raise ValueError("ii.ops.security_separated_from_devops")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            run_ref=run_ref.strip(),
            automated=True,
            security_integrated=True,
            image_scanned=True,
            status="completed",
        )
        root.pending_events.append("PipelineCompleted")
        root.pending_events.append("ServiceDeployed")
        root.history.append({"event": "PipelineCompleted"})
        return root

    def is_manual(self) -> bool:
        return not self.automated

    def security_separated(self) -> bool:
        return not self.security_integrated


@dataclass(eq=False, kw_only=True)
class GitOpsDeploymentSyncRoot(AggregateRoot):
    tenant_id: str
    sync_ref: str
    gitops_enabled: bool
    continuous_sync: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def sync(
        cls,
        *,
        tenant_id: str,
        sync_ref: str,
        gitops_enabled: bool = True,
        continuous_sync: bool = True,
    ) -> GitOpsDeploymentSyncRoot:
        if not tenant_id.strip():
            raise ValueError("ii.ops.sync_tenant_required")
        if not gitops_enabled or not continuous_sync:
            raise ValueError("ii.ops.deployment_manual")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            sync_ref=sync_ref.strip(),
            gitops_enabled=True,
            continuous_sync=True,
            status="synced",
        )
        root.history.append({"event": "GitOpsSynced"})
        return root


@dataclass(eq=False, kw_only=True)
class ScalabilityPolicyRoot(AggregateRoot):
    tenant_id: str
    policy_ref: str
    horizontal_scaling: bool
    intelligent_scaling: bool
    strategy_defined: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def define(
        cls,
        *,
        tenant_id: str,
        policy_ref: str,
        horizontal_scaling: bool = True,
        intelligent_scaling: bool = True,
        strategy_defined: bool = True,
    ) -> ScalabilityPolicyRoot:
        if not tenant_id.strip():
            raise ValueError("ii.ops.scale_tenant_required")
        if not strategy_defined or not (horizontal_scaling and intelligent_scaling):
            raise ValueError("ii.ops.scaling_strategy_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            policy_ref=policy_ref.strip(),
            horizontal_scaling=True,
            intelligent_scaling=True,
            strategy_defined=True,
            status="active",
        )
        root.pending_events.append("WorkloadScaled")
        root.history.append({"event": "WorkloadScaled"})
        return root

    def strategy_missing(self) -> bool:
        return not self.strategy_defined


@dataclass(eq=False, kw_only=True)
class HighAvailabilityPlanRoot(AggregateRoot):
    tenant_id: str
    plan_ref: str
    multi_zone: bool
    availability_target: str
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def establish(
        cls,
        *,
        tenant_id: str,
        plan_ref: str,
        multi_zone: bool = True,
        availability_target: str = "99.99%",
    ) -> HighAvailabilityPlanRoot:
        if not tenant_id.strip():
            raise ValueError("ii.ops.ha_tenant_required")
        if not multi_zone or availability_target != "99.99%":
            raise ValueError("ii.ops.ha_plan_incomplete")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            plan_ref=plan_ref.strip(),
            multi_zone=True,
            availability_target="99.99%",
            status="active",
        )
        root.history.append({"event": "HAPlanEstablished"})
        return root


@dataclass(eq=False, kw_only=True)
class DisasterRecoveryTestRoot(AggregateRoot):
    tenant_id: str
    test_ref: str
    tested: bool
    rpo_met: bool
    rto_met: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def execute(
        cls,
        *,
        tenant_id: str,
        test_ref: str,
        tested: bool = True,
        rpo_met: bool = True,
        rto_met: bool = True,
    ) -> DisasterRecoveryTestRoot:
        if not tenant_id.strip():
            raise ValueError("ii.ops.dr_tenant_required")
        if not tested or not (rpo_met and rto_met):
            raise ValueError("ii.ops.disaster_recovery_not_tested")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            test_ref=test_ref.strip(),
            tested=True,
            rpo_met=True,
            rto_met=True,
            status="passed",
        )
        root.pending_events.append("FailoverTestPassed")
        root.history.append({"event": "FailoverTestPassed"})
        return root

    def not_tested(self) -> bool:
        return not self.tested


@dataclass(eq=False, kw_only=True)
class ObservabilityBaselineRoot(AggregateRoot):
    tenant_id: str
    baseline_ref: str
    pillars: tuple[str, ...]
    complete: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def collect(
        cls,
        *,
        tenant_id: str,
        baseline_ref: str,
        pillars: tuple[str, ...] | None = None,
        complete: bool = True,
    ) -> ObservabilityBaselineRoot:
        if not tenant_id.strip():
            raise ValueError("ii.ops.obs_tenant_required")
        pl = tuple(pillars or tuple(OBSERVABILITY_PILLARS))
        if not complete or not OBSERVABILITY_PILLARS.issubset(set(pl)):
            raise ValueError("ii.ops.observability_incomplete")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            baseline_ref=baseline_ref.strip(),
            pillars=pl,
            complete=True,
            status="collected",
        )
        root.pending_events.append("ObservabilityBaselineCollected")
        root.history.append({"event": "ObservabilityBaselineCollected"})
        return root

    def is_incomplete(self) -> bool:
        return not self.complete
