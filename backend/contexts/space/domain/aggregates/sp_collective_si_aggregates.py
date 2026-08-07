"""P218-W aggregates — collective super intelligence invariants."""
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
class CollectiveSiCoreRoot(AggregateRoot):
    tenant_id: str; core_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, core_ref: str, present: bool = True):
        if not present: raise ValueError("space.collective_si.collective_super_intelligence_is_missing")
        return _mk(cls, tenant_id, "core_ref", core_ref, "space.collective_si.collective_super_intelligence_is_missing", "CollectiveIntelligenceExpandedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class HumanAiCivilizationNetworkRoot(AggregateRoot):
    tenant_id: str; network_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, network_ref: str, present: bool = True):
        if not present: raise ValueError("space.collective_si.human_ai_civilization_network_is_missing")
        return _mk(cls, tenant_id, "network_ref", network_ref, "space.collective_si.human_ai_civilization_network_is_missing", "AIHumanCollaborationCreatedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class GlobalCognitiveEcosystemRoot(AggregateRoot):
    tenant_id: str; ecosystem_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, ecosystem_ref: str, present: bool = True):
        if not present: raise ValueError("space.collective_si.global_cognitive_ecosystem_is_missing")
        return _mk(cls, tenant_id, "ecosystem_ref", ecosystem_ref, "space.collective_si.global_cognitive_ecosystem_is_missing", "CivilizationInsightDiscoveredEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class CollectiveReasoningRoot(AggregateRoot):
    tenant_id: str; reasoning_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, reasoning_ref: str, present: bool = True):
        if not present: raise ValueError("space.collective_si.collective_reasoning_architecture_is_missing")
        return _mk(cls, tenant_id, "reasoning_ref", reasoning_ref, "space.collective_si.collective_reasoning_architecture_is_missing", "CollectiveReasoningStartedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class CollectiveSiKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present: raise ValueError("space.collective_si.knowledge_graph_is_missing")
        return _mk(cls, tenant_id, "kg_ref", kg_ref, "space.collective_si.knowledge_graph_is_missing", "KnowledgeSharedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class CollectiveIntelligenceTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("space.collective_si.digital_twin_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "space.collective_si.digital_twin_is_missing", "SolutionGeneratedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class IntelligenceAlignmentRoot(AggregateRoot):
    tenant_id: str; alignment_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, alignment_ref: str, present: bool = True):
        if not present: raise ValueError("space.collective_si.intelligence_alignment_is_missing")
        return _mk(cls, tenant_id, "alignment_ref", alignment_ref, "space.collective_si.intelligence_alignment_is_missing", "IntelligenceAlignmentValidatedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class CsiEthicsRoot(AggregateRoot):
    tenant_id: str; ethics_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, ethics_ref: str, present: bool = True):
        if not present: raise ValueError("space.collective_si.governance_framework_is_missing")
        return _mk(cls, tenant_id, "ethics_ref", ethics_ref, "space.collective_si.governance_framework_is_missing", "DecisionValidatedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class CsiGovernanceRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("space.collective_si.governance_is_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "space.collective_si.governance_is_missing", "HumanAuthorityConfirmedEvent")
    def is_missing(self) -> bool: return not self.present
