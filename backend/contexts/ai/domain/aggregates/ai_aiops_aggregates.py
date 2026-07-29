"""P214-J aggregates — quality-gate invariants."""
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
class AiopsPlatformRoot(AggregateRoot):
    tenant_id: str
    platform_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, platform_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aiops.tenant_required")
        if not present:
            raise ValueError("ai.aiops.enterprise_aiops_platform_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            platform_ref=platform_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("AIServiceCreatedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class ObservabilityRoot(AggregateRoot):
    tenant_id: str
    observability_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, observability_ref: str, present: bool = True
    ):
        tid = _tid(tenant_id, "ai.aiops.obs_tenant_required")
        if not present:
            raise ValueError("ai.aiops.ai_observability_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            observability_ref=observability_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("MetricCollectedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class IncidentIntelligenceRoot(AggregateRoot):
    tenant_id: str
    incident_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, incident_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aiops.incident_tenant_required")
        if not present:
            raise ValueError("ai.aiops.incident_intelligence_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            incident_ref=incident_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("IncidentDetectedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class AutonomousRemediationRoot(AggregateRoot):
    tenant_id: str
    remediation_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, remediation_ref: str, present: bool = True
    ):
        tid = _tid(tenant_id, "ai.aiops.remediation_tenant_required")
        if not present:
            raise ValueError("ai.aiops.autonomous_remediation_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            remediation_ref=remediation_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("RemediationExecutedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class PerformanceIntelligenceRoot(AggregateRoot):
    tenant_id: str
    performance_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, performance_ref: str, present: bool = True
    ):
        tid = _tid(tenant_id, "ai.aiops.perf_tenant_required")
        if not present:
            raise ValueError("ai.aiops.performance_intelligence_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            performance_ref=performance_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("OptimizationCompletedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class OpsDigitalTwinRoot(AggregateRoot):
    tenant_id: str
    twin_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aiops.twin_tenant_required")
        if not present:
            raise ValueError("ai.aiops.operational_digital_twin_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            twin_ref=twin_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("AIServiceRecoveredEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present
