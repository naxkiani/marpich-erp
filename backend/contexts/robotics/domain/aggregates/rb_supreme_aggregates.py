"""P216-Z aggregates — supreme control plane / intelligence nexus invariants."""
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
class SupremeControlPlaneRoot(AggregateRoot):
    tenant_id: str; control_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, control_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.supreme.meos_robotics_supreme_control_plane_is_missing")
        return _mk(cls, tenant_id, "control_ref", control_ref, "robotics.supreme.meos_robotics_supreme_control_plane_is_missing", "RobotRegisteredEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class UniversalRoboticsNetworkRoot(AggregateRoot):
    tenant_id: str; network_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, network_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.supreme.universal_robotics_network_is_missing")
        return _mk(cls, tenant_id, "network_ref", network_ref, "robotics.supreme.universal_robotics_network_is_missing", "RoboticsNetworkUpdatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class RoboticsCivilizationRoot(AggregateRoot):
    tenant_id: str; civilization_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, civilization_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.supreme.autonomous_robotics_civilization_layer_is_missing")
        return _mk(cls, tenant_id, "civilization_ref", civilization_ref, "robotics.supreme.autonomous_robotics_civilization_layer_is_missing", "CivilizationLayerUpdatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class CollectiveIntelligenceRoot(AggregateRoot):
    tenant_id: str; collective_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, collective_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.supreme.collective_intelligence_engine_is_missing")
        return _mk(cls, tenant_id, "collective_ref", collective_ref, "robotics.supreme.collective_intelligence_engine_is_missing", "IntelligenceEvolutionEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class UniversalDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.supreme.robotics_digital_twin_universe_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "robotics.supreme.robotics_digital_twin_universe_is_missing", "RobotRegisteredEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class KnowledgeGraphUniverseRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.supreme.robotics_knowledge_graph_is_missing")
        return _mk(cls, tenant_id, "kg_ref", kg_ref, "robotics.supreme.robotics_knowledge_graph_is_missing", "CapabilityExchangeEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class AutonomousGovernanceRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.supreme.autonomous_governance_is_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "robotics.supreme.autonomous_governance_is_missing", "GovernanceDecisionEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SupremeSecurityRoot(AggregateRoot):
    tenant_id: str; security_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, security_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.supreme.security_architecture_is_missing")
        return _mk(cls, tenant_id, "security_ref", security_ref, "robotics.supreme.security_architecture_is_missing", "SafetyValidationEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class HumanAuthorityRoot(AggregateRoot):
    tenant_id: str; authority_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, authority_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.supreme.human_authority_framework_is_missing")
        return _mk(cls, tenant_id, "authority_ref", authority_ref, "robotics.supreme.human_authority_framework_is_missing", "GovernanceDecisionEvent")
    def is_missing(self)->bool: return not self.present
