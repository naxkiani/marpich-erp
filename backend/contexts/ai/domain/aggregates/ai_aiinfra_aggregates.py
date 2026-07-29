"""P214-N aggregates — quality-gate invariants."""
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
class AiinfraPlatformRoot(AggregateRoot):
    tenant_id: str
    platform_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, platform_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aiinfra.tenant_required")
        if not present:
            raise ValueError("ai.aiinfra.enterprise_ai_cloud_platform_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            platform_ref=platform_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("InfrastructureCreatedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class ComputeFabricRoot(AggregateRoot):
    tenant_id: str
    compute_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, compute_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aiinfra.compute_tenant_required")
        if not present:
            raise ValueError("ai.aiinfra.intelligent_compute_fabric_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            compute_ref=compute_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("ComputeAllocatedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class GPUInfrastructureRoot(AggregateRoot):
    tenant_id: str
    gpu_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, gpu_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aiinfra.gpu_tenant_required")
        if not present:
            raise ValueError("ai.aiinfra.gpu_infrastructure_platform_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            gpu_ref=gpu_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("GPUProvisionedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class AIRuntimeRoot(AggregateRoot):
    tenant_id: str
    runtime_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, runtime_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aiinfra.runtime_tenant_required")
        if not present:
            raise ValueError("ai.aiinfra.ai_runtime_platform_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            runtime_ref=runtime_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("WorkloadDeployedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class KubernetesAIRoot(AggregateRoot):
    tenant_id: str
    k8s_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, k8s_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aiinfra.k8s_tenant_required")
        if not present:
            raise ValueError("ai.aiinfra.kubernetes_ai_platform_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            k8s_ref=k8s_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("WorkloadDeployedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class InfraAutomationRoot(AggregateRoot):
    tenant_id: str
    automation_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, automation_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aiinfra.auto_tenant_required")
        if not present:
            raise ValueError("ai.aiinfra.infrastructure_automation_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            automation_ref=automation_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("InfrastructureCreatedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class ResourceIntelligenceRoot(AggregateRoot):
    tenant_id: str
    resource_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, resource_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aiinfra.res_tenant_required")
        if not present:
            raise ValueError("ai.aiinfra.resource_intelligence_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            resource_ref=resource_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("OptimizationCompletedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class InfraDigitalTwinRoot(AggregateRoot):
    tenant_id: str
    twin_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aiinfra.twin_tenant_required")
        if not present:
            raise ValueError("ai.aiinfra.infrastructure_digital_twin_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            twin_ref=twin_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("OptimizationCompletedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present
