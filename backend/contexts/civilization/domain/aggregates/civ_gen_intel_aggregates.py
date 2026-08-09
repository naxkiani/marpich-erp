"""P219-V aggregates — civilization general intelligence coordination invariants."""
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
class CivilizationGeneralIntelligenceCoordinationPlatformRoot(AggregateRoot):
    tenant_id: str; cgi_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, cgi_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.gen_intel.civilization_general_intelligence_coordination_platform_is_missing")
        return _mk(
            cls, tenant_id, "cgi_ref", cgi_ref,
            "civilization.gen_intel.civilization_general_intelligence_coordination_platform_is_missing",
            "CoordinationUpdatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class KnowledgeFusionPlatformRoot(AggregateRoot):
    tenant_id: str; fusion_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, fusion_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.gen_intel.knowledge_fusion_platform_is_missing")
        return _mk(
            cls, tenant_id, "fusion_ref", fusion_ref,
            "civilization.gen_intel.knowledge_fusion_platform_is_missing",
            "KnowledgeIntegratedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class MultiAgentCoordinationPlatformRoot(AggregateRoot):
    tenant_id: str; agent_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, agent_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.gen_intel.multi_agent_coordination_platform_is_missing")
        return _mk(
            cls, tenant_id, "agent_ref", agent_ref,
            "civilization.gen_intel.multi_agent_coordination_platform_is_missing",
            "AgentAssignedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class CrossDomainIntelligencePlatformRoot(AggregateRoot):
    tenant_id: str; cross_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, cross_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.gen_intel.cross_domain_intelligence_platform_is_missing")
        return _mk(
            cls, tenant_id, "cross_ref", cross_ref,
            "civilization.gen_intel.cross_domain_intelligence_platform_is_missing",
            "KnowledgeSynchronizedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DecisionSupportPlatformRoot(AggregateRoot):
    tenant_id: str; decision_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, decision_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.gen_intel.decision_support_platform_is_missing")
        return _mk(
            cls, tenant_id, "decision_ref", decision_ref,
            "civilization.gen_intel.decision_support_platform_is_missing",
            "RecommendationGeneratedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class CoordinationDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.gen_intel.coordination_digital_twin_is_missing")
        return _mk(
            cls, tenant_id, "twin_ref", twin_ref,
            "civilization.gen_intel.coordination_digital_twin_is_missing",
            "ReasoningCompletedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class MeosCivilizationGeneralIntelligenceCoordinationCoreRoot(AggregateRoot):
    tenant_id: str; core_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, core_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.gen_intel.meos_civilization_general_intelligence_coordination_core_is_missing")
        return _mk(
            cls, tenant_id, "core_ref", core_ref,
            "civilization.gen_intel.meos_civilization_general_intelligence_coordination_core_is_missing",
            "DecisionSupportedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class IntelligenceKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.gen_intel.intelligence_knowledge_graph_is_missing")
        return _mk(
            cls, tenant_id, "kg_ref", kg_ref,
            "civilization.gen_intel.intelligence_knowledge_graph_is_missing",
            "KnowledgeGraphUpdatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class IntelligenceCoordinationEventArchitectureRoot(AggregateRoot):
    tenant_id: str; events_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, events_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.gen_intel.intelligence_coordination_event_architecture_is_missing")
        return _mk(
            cls, tenant_id, "events_ref", events_ref,
            "civilization.gen_intel.intelligence_coordination_event_architecture_is_missing",
            "ConfidenceCalculatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present

