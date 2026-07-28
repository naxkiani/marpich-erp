"""P213-O aggregates — quality-gate invariants."""
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
class BiDeployProfileRoot(AggregateRoot):
    tenant_id: str
    profile_ref: str
    complete: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(cls, *, tenant_id: str, profile_ref: str, complete: bool = True):
        tid = _tid(tenant_id, "analytics.deploy.tenant_required")
        if not complete:
            raise ValueError(
                "analytics.deploy.bi_deploy_architecture_is_incomplete"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            profile_ref=profile_ref.strip(),
            complete=True,
            status="published",
        )
        root.pending_events.append("BiDeploymentCompletedEvent")
        return root

    def is_incomplete(self) -> bool:
        return not self.complete


@dataclass(eq=False, kw_only=True)
class BiKubernetesRuntimeRoot(AggregateRoot):
    tenant_id: str
    cluster_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, cluster_ref: str, present: bool = True):
        tid = _tid(tenant_id, "analytics.deploy.k8s_tenant_required")
        if not present:
            raise ValueError(
                "analytics.deploy.kubernetes_runtime_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            cluster_ref=cluster_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("BiDeploymentCompletedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BiGitOpsPlatformRoot(AggregateRoot):
    tenant_id: str
    gitops_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, gitops_ref: str, present: bool = True):
        tid = _tid(tenant_id, "analytics.deploy.gitops_tenant_required")
        if not present:
            raise ValueError("analytics.deploy.gitops_platform_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            gitops_ref=gitops_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("BiGitOpsReconciledEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BiDevSecOpsRoot(AggregateRoot):
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
    ):
        tid = _tid(tenant_id, "analytics.deploy.sec_tenant_required")
        if not present:
            raise ValueError(
                "analytics.deploy.devsecops_pipeline_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            pipeline_ref=pipeline_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("BiSecurityGatePassedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BiObservabilityRoot(AggregateRoot):
    tenant_id: str
    obs_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, obs_ref: str, present: bool = True):
        tid = _tid(tenant_id, "analytics.deploy.obs_tenant_required")
        if not present:
            raise ValueError(
                "analytics.deploy.observability_platform_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            obs_ref=obs_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("BiIncidentDetectedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BiDefinitionOfDoneRoot(AggregateRoot):
    tenant_id: str
    dod_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, dod_ref: str, present: bool = True):
        tid = _tid(tenant_id, "analytics.deploy.dod_tenant_required")
        if not present:
            raise ValueError(
                "analytics.deploy.definition_of_done_is_incomplete"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            dod_ref=dod_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("BiDeploymentCompletedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present
