"""P211-N CQRS/events/ops aggregates — quality-gate invariants."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class DsLooselyCoupledServicesRoot(AggregateRoot):
    tenant_id: str
    fabric_ref: str
    loosely_coupled: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def establish(
        cls, *, tenant_id: str, fabric_ref: str, loosely_coupled: bool = True
    ) -> DsLooselyCoupledServicesRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.ops.tenant_required")
        if not loosely_coupled:
            raise ValueError(
                "data_security.ops.services_are_tightly_coupled"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            fabric_ref=fabric_ref.strip(),
            loosely_coupled=True,
            status="decoupled",
        )
        root.pending_events.append("DataAssetRegistered")
        root.pending_events.append("TightCouplingRejected")
        root.history.append({"event": "ServicesLooselyCoupled"})
        return root

    def is_tightly_coupled(self) -> bool:
        return not self.loosely_coupled


@dataclass(eq=False, kw_only=True)
class DsImmutableEventsRoot(AggregateRoot):
    tenant_id: str
    event_ref: str
    immutable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def append(
        cls, *, tenant_id: str, event_ref: str, immutable: bool = True
    ) -> DsImmutableEventsRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.ops.event_tenant_required")
        if not immutable:
            raise ValueError("data_security.ops.events_are_not_immutable")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            event_ref=event_ref.strip(),
            immutable=True,
            status="appended",
        )
        root.pending_events.append("RiskPredicted")
        root.pending_events.append("MutableEventRejected")
        root.history.append({"event": "EventImmutable"})
        return root

    def is_mutable(self) -> bool:
        return not self.immutable


@dataclass(eq=False, kw_only=True)
class DsManagedApisRoot(AggregateRoot):
    tenant_id: str
    api_ref: str
    managed: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(
        cls, *, tenant_id: str, api_ref: str, managed: bool = True
    ) -> DsManagedApisRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.ops.api_tenant_required")
        if not managed:
            raise ValueError("data_security.ops.apis_are_unmanaged")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            api_ref=api_ref.strip(),
            managed=True,
            status="managed",
        )
        root.pending_events.append("ProtectionPolicyChanged")
        root.pending_events.append("UnmanagedApiRejected")
        root.history.append({"event": "ApiManaged"})
        return root

    def is_unmanaged(self) -> bool:
        return not self.managed


@dataclass(eq=False, kw_only=True)
class DsTraceableSecurityDecisionsRoot(AggregateRoot):
    tenant_id: str
    decision_ref: str
    traceable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def record(
        cls, *, tenant_id: str, decision_ref: str, traceable: bool = True
    ) -> DsTraceableSecurityDecisionsRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.ops.decision_tenant_required")
        if not traceable:
            raise ValueError(
                "data_security.ops.security_decisions_cannot_be_traced"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            decision_ref=decision_ref.strip(),
            traceable=True,
            status="traced",
        )
        root.pending_events.append("AccessGranted")
        root.pending_events.append("UntraceableDecisionRejected")
        root.history.append({"event": "DecisionTraceable"})
        return root

    def is_untraceable(self) -> bool:
        return not self.traceable


@dataclass(eq=False, kw_only=True)
class DsScalablePlatformRoot(AggregateRoot):
    tenant_id: str
    platform_ref: str
    scalable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, platform_ref: str, scalable: bool = True
    ) -> DsScalablePlatformRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.ops.scale_tenant_required")
        if not scalable:
            raise ValueError("data_security.ops.scaling_is_impossible")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            platform_ref=platform_ref.strip(),
            scalable=True,
            status="scalable",
        )
        root.pending_events.append("TwinSynchronized")
        root.pending_events.append("ImpossibleScalingRejected")
        root.history.append({"event": "PlatformScalable"})
        return root

    def is_impossible(self) -> bool:
        return not self.scalable


@dataclass(eq=False, kw_only=True)
class DsCompleteAuditHistoryRoot(AggregateRoot):
    tenant_id: str
    audit_ref: str
    complete: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def seal(
        cls, *, tenant_id: str, audit_ref: str, complete: bool = True
    ) -> DsCompleteAuditHistoryRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.ops.audit_tenant_required")
        if not complete:
            raise ValueError(
                "data_security.ops.audit_history_is_incomplete"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            audit_ref=audit_ref.strip(),
            complete=True,
            status="complete",
        )
        root.pending_events.append("IncidentCreated")
        root.pending_events.append("IncompleteAuditRejected")
        root.history.append({"event": "AuditHistoryComplete"})
        return root

    def is_incomplete(self) -> bool:
        return not self.complete


@dataclass(eq=False, kw_only=True)
class DsEventPublishedRoot(AggregateRoot):
    tenant_id: str
    stream_ref: str
    published: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(
        cls, *, tenant_id: str, stream_ref: str, published: bool = True
    ) -> DsEventPublishedRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.ops.stream_tenant_required")
        if not published:
            raise ValueError("data_security.ops.event_not_published")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            stream_ref=stream_ref.strip(),
            published=True,
            status="published",
        )
        root.pending_events.append("DataClassified")
        root.pending_events.append("AutonomousActionExecuted")
        root.history.append({"event": "EventPublished"})
        return root


@dataclass(eq=False, kw_only=True)
class DsSimulationExecutedRoot(AggregateRoot):
    tenant_id: str
    simulation_ref: str
    executed: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def execute(
        cls, *, tenant_id: str, simulation_ref: str, executed: bool = True
    ) -> DsSimulationExecutedRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.ops.sim_tenant_required")
        if not executed:
            raise ValueError("data_security.ops.simulation_not_executed")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            simulation_ref=simulation_ref.strip(),
            executed=True,
            status="executed",
        )
        root.pending_events.append("SimulationExecuted")
        root.pending_events.append("RiskForecastGenerated")
        root.history.append({"event": "SimulationExecuted"})
        return root
