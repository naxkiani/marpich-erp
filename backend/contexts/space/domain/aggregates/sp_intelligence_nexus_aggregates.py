"""P218-Z aggregates — final intelligence nexus invariants."""
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
class IntelligenceNexusCoreRoot(AggregateRoot):
    tenant_id: str; core_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, core_ref: str, present: bool = True):
        if not present: raise ValueError("space.intelligence_nexus.ultimate_intelligence_civilization_nexus_is_missing")
        return _mk(cls, tenant_id, "core_ref", core_ref, "space.intelligence_nexus.ultimate_intelligence_civilization_nexus_is_missing", "IntelligenceNetworkCreatedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class SupremeControlPlaneRoot(AggregateRoot):
    tenant_id: str; control_plane_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, control_plane_ref: str, present: bool = True):
        if not present: raise ValueError("space.intelligence_nexus.meos_supreme_control_plane_is_missing")
        return _mk(cls, tenant_id, "control_plane_ref", control_plane_ref, "space.intelligence_nexus.meos_supreme_control_plane_is_missing", "ControlPlaneActivatedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class AutonomousCivilizationRoot(AggregateRoot):
    tenant_id: str; autonomous_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, autonomous_ref: str, present: bool = True):
        if not present: raise ValueError("space.intelligence_nexus.autonomous_civilization_intelligence_is_missing")
        return _mk(cls, tenant_id, "autonomous_ref", autonomous_ref, "space.intelligence_nexus.autonomous_civilization_intelligence_is_missing", "CivilizationModelUpdatedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class DecisionIntelligenceRoot(AggregateRoot):
    tenant_id: str; decision_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, decision_ref: str, present: bool = True):
        if not present: raise ValueError("space.intelligence_nexus.decision_intelligence_is_missing")
        return _mk(cls, tenant_id, "decision_ref", decision_ref, "space.intelligence_nexus.decision_intelligence_is_missing", "DecisionOptimizedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class AgentEcosystemRoot(AggregateRoot):
    tenant_id: str; agent_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, agent_ref: str, present: bool = True):
        if not present: raise ValueError("space.intelligence_nexus.agent_ecosystem_is_missing")
        return _mk(cls, tenant_id, "agent_ref", agent_ref, "space.intelligence_nexus.agent_ecosystem_is_missing", "AgentActivatedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class UniversalKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present: raise ValueError("space.intelligence_nexus.universal_knowledge_graph_is_missing")
        return _mk(cls, tenant_id, "kg_ref", kg_ref, "space.intelligence_nexus.universal_knowledge_graph_is_missing", "KnowledgeIntegratedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class CivilizationDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("space.intelligence_nexus.civilization_digital_twin_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "space.intelligence_nexus.civilization_digital_twin_is_missing", "EvolutionMilestoneReachedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class IntelligenceGovernanceRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("space.intelligence_nexus.intelligence_governance_is_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "space.intelligence_nexus.intelligence_governance_is_missing", "GovernanceValidatedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class FinalArchitectureRoot(AggregateRoot):
    tenant_id: str; architecture_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, architecture_ref: str, present: bool = True):
        if not present: raise ValueError("space.intelligence_nexus.final_enterprise_intelligence_architecture_is_missing")
        return _mk(cls, tenant_id, "architecture_ref", architecture_ref, "space.intelligence_nexus.final_enterprise_intelligence_architecture_is_missing", "SupremeIntelligenceExpandedEvent")
    def is_missing(self) -> bool: return not self.present
