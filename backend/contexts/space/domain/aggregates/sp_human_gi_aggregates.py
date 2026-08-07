"""P218-V aggregates — human general intelligence invariants."""
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
        id=UniqueId.generate(), tenant_id=tid, **{ref_name: ref_value.strip()},
        present=True, status="enabled",
    )
    obj.pending_events.append(event)
    return obj


@dataclass(eq=False, kw_only=True)
class HumanGiCoreRoot(AggregateRoot):
    tenant_id: str; core_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, core_ref: str, present: bool = True):
        if not present: raise ValueError("space.human_gi.human_gi_architecture_is_missing")
        return _mk(cls, tenant_id, "core_ref", core_ref, "space.human_gi.human_gi_architecture_is_missing", "IntelligenceScenarioUpdatedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class CognitiveCivilizationRoot(AggregateRoot):
    tenant_id: str; civilization_intel_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, civilization_intel_ref: str, present: bool = True):
        if not present: raise ValueError("space.human_gi.advanced_cognitive_civilization_is_missing")
        return _mk(cls, tenant_id, "civilization_intel_ref", civilization_intel_ref, "space.human_gi.advanced_cognitive_civilization_is_missing", "CivilizationProblemSolvedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class CollectiveIntelligenceRoot(AggregateRoot):
    tenant_id: str; collective_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, collective_ref: str, present: bool = True):
        if not present: raise ValueError("space.human_gi.collective_intelligence_is_missing")
        return _mk(cls, tenant_id, "collective_ref", collective_ref, "space.human_gi.collective_intelligence_is_missing", "CollectiveNetworkCreatedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class ReasoningArchitectureRoot(AggregateRoot):
    tenant_id: str; reasoning_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, reasoning_ref: str, present: bool = True):
        if not present: raise ValueError("space.human_gi.reasoning_architecture_is_missing")
        return _mk(cls, tenant_id, "reasoning_ref", reasoning_ref, "space.human_gi.reasoning_architecture_is_missing", "ReasoningCapabilityImprovedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class HumanGiKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present: raise ValueError("space.human_gi.knowledge_graph_is_missing")
        return _mk(cls, tenant_id, "kg_ref", kg_ref, "space.human_gi.knowledge_graph_is_missing", "DiscoveryGeneratedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class HumanIntelligenceTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("space.human_gi.human_intelligence_digital_twin_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "space.human_gi.human_intelligence_digital_twin_is_missing", "CognitiveEvolutionDetectedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class HumanAiCollaborationRoot(AggregateRoot):
    tenant_id: str; collaboration_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, collaboration_ref: str, present: bool = True):
        if not present: raise ValueError("space.human_gi.human_ai_collaboration_is_missing")
        return _mk(cls, tenant_id, "collaboration_ref", collaboration_ref, "space.human_gi.human_ai_collaboration_is_missing", "HumanAiCollaborationSessionStartedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class GiEthicsRoot(AggregateRoot):
    tenant_id: str; ethics_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, ethics_ref: str, present: bool = True):
        if not present: raise ValueError("space.human_gi.ethical_governance_is_missing")
        return _mk(cls, tenant_id, "ethics_ref", ethics_ref, "space.human_gi.ethical_governance_is_missing", "EthicalIntelligenceReviewCompletedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class GiGovernanceRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("space.human_gi.governance_is_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "space.human_gi.governance_is_missing", "CognitiveSovereigntyValidatedEvent")
    def is_missing(self) -> bool: return not self.present
