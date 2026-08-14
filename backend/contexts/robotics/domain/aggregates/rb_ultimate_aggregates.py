"""P216-Y aggregates — ultimate / future robotics intelligence invariants."""
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
    obj = root_cls(id=UniqueId.generate(), tenant_id=tid, **{ref_name: ref_value.strip()}, present=True, status="enabled")
    obj.pending_events.append(event)
    return obj

@dataclass(eq=False, kw_only=True)
class FutureRoboticsRoot(AggregateRoot):
    tenant_id: str; future_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, future_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.ultimate.future_robotics_architecture_is_missing")
        return _mk(cls, tenant_id, "future_ref", future_ref, "robotics.ultimate.future_robotics_architecture_is_missing", "RobotCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class HumanMachineSymbiosisRoot(AggregateRoot):
    tenant_id: str; symbiosis_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, symbiosis_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.ultimate.human_machine_symbiosis_platform_is_missing")
        return _mk(cls, tenant_id, "symbiosis_ref", symbiosis_ref, "robotics.ultimate.human_machine_symbiosis_platform_is_missing", "HumanRobotInteractionEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class CognitiveRoboticsRoot(AggregateRoot):
    tenant_id: str; cognitive_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, cognitive_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.ultimate.cognitive_robotics_platform_is_missing")
        return _mk(cls, tenant_id, "cognitive_ref", cognitive_ref, "robotics.ultimate.cognitive_robotics_platform_is_missing", "IntelligenceUpdatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class RoboticsEvolutionRoot(AggregateRoot):
    tenant_id: str; evolution_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, evolution_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.ultimate.robotics_evolution_engine_is_missing")
        return _mk(cls, tenant_id, "evolution_ref", evolution_ref, "robotics.ultimate.robotics_evolution_engine_is_missing", "EvolutionCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class RoboticsDigitalTwinUniverseRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.ultimate.robotics_digital_twin_universe_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "robotics.ultimate.robotics_digital_twin_universe_is_missing", "IntelligenceUpdatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class RoboticsKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.ultimate.robotics_knowledge_graph_is_missing")
        return _mk(cls, tenant_id, "kg_ref", kg_ref, "robotics.ultimate.robotics_knowledge_graph_is_missing", "KnowledgeTransferredEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class AutonomousIntelligenceRoot(AggregateRoot):
    tenant_id: str; autonomy_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, autonomy_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.ultimate.autonomous_intelligence_layer_is_missing")
        return _mk(cls, tenant_id, "autonomy_ref", autonomy_ref, "robotics.ultimate.autonomous_intelligence_layer_is_missing", "CapabilityLearnedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class UltimateTrustRoot(AggregateRoot):
    tenant_id: str; trust_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, trust_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.ultimate.trust_architecture_is_missing")
        return _mk(cls, tenant_id, "trust_ref", trust_ref, "robotics.ultimate.trust_architecture_is_missing", "SafetyVerifiedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class HumanGovernanceRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.ultimate.human_governance_is_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "robotics.ultimate.human_governance_is_missing", "SafetyVerifiedEvent")
    def is_missing(self)->bool: return not self.present
