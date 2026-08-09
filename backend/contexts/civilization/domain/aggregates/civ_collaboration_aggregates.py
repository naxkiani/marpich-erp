"""P219-P aggregates — civilization collaboration intelligence core invariants."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import UTC, datetime
from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


def _tid(tenant_id: str, code: str) -> str:
    if not tenant_id.strip():
        raise ValueError(code)
    return tenant_id.strip()


def _mk(root_cls, tenant_id: str, ref_name: str, ref_value: str, err: str, event: str):
    tid = _tid(tenant_id, err + ".tenant")
    obj = root_cls(
        id=UniqueId.generate(), tenant_id=tid,
        **{ref_name: ref_value.strip()}, present=True, status="enabled",
    )
    obj.pending_events.append(event)
    return obj


@dataclass(eq=False, kw_only=True)
class CivilizationCollaborationIntelligencePlatformRoot(AggregateRoot):
    tenant_id: str; collaboration_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, collaboration_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.collaboration.civilization_collaboration_intelligence_platform_is_missing")
        return _mk(
            cls, tenant_id, "collaboration_ref", collaboration_ref,
            "civilization.collaboration.civilization_collaboration_intelligence_platform_is_missing",
            "CollaborationInitiatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class GlobalCollaborationNetworkRoot(AggregateRoot):
    tenant_id: str; network_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, network_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.collaboration.global_collaboration_network_is_missing")
        return _mk(
            cls, tenant_id, "network_ref", network_ref,
            "civilization.collaboration.global_collaboration_network_is_missing",
            "PartnerMatchedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class CollectiveProblemSolvingPlatformRoot(AggregateRoot):
    tenant_id: str; collective_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, collective_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.collaboration.collective_problem_solving_platform_is_missing")
        return _mk(
            cls, tenant_id, "collective_ref", collective_ref,
            "civilization.collaboration.collective_problem_solving_platform_is_missing",
            "ConsensusReachedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class CivilizationCoordinationPlatformRoot(AggregateRoot):
    tenant_id: str; coordination_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, coordination_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.collaboration.civilization_coordination_platform_is_missing")
        return _mk(
            cls, tenant_id, "coordination_ref", coordination_ref,
            "civilization.collaboration.civilization_coordination_platform_is_missing",
            "CoordinationOptimizedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class CollaborationDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.collaboration.collaboration_digital_twin_is_missing")
        return _mk(
            cls, tenant_id, "twin_ref", twin_ref,
            "civilization.collaboration.collaboration_digital_twin_is_missing",
            "ExecutionSynchronizedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class CollaborationKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.collaboration.collaboration_knowledge_graph_is_missing")
        return _mk(
            cls, tenant_id, "kg_ref", kg_ref,
            "civilization.collaboration.collaboration_knowledge_graph_is_missing",
            "KnowledgeSharedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class MeosCivilizationCollaborationIntelligenceCoreRoot(AggregateRoot):
    tenant_id: str; core_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, core_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.collaboration.meos_civilization_collaboration_intelligence_core_is_missing")
        return _mk(
            cls, tenant_id, "core_ref", core_ref,
            "civilization.collaboration.meos_civilization_collaboration_intelligence_core_is_missing",
            "SolutionApprovedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class CollaborationEventArchitectureRoot(AggregateRoot):
    tenant_id: str; events_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, events_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.collaboration.collaboration_event_architecture_is_missing")
        return _mk(
            cls, tenant_id, "events_ref", events_ref,
            "civilization.collaboration.collaboration_event_architecture_is_missing",
            "LearningDistributedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present
