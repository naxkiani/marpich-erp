"""P218 aggregates — space intelligence foundation invariants."""
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
class SpaceIntelligencePlatformRoot(AggregateRoot):
    tenant_id: str; space_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, space_ref: str, present: bool = True):
        if not present: raise ValueError("space.foundation.space_intelligence_platform_is_missing")
        return _mk(cls, tenant_id, "space_ref", space_ref, "space.foundation.space_intelligence_platform_is_missing", "SpaceInsightGeneratedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SpaceAiOperatingSystemRoot(AggregateRoot):
    tenant_id: str; saios_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, saios_ref: str, present: bool = True):
        if not present: raise ValueError("space.foundation.space_ai_operating_system_is_missing")
        return _mk(cls, tenant_id, "saios_ref", saios_ref, "space.foundation.space_ai_operating_system_is_missing", "MissionOptimizedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class OrbitalCivilizationRoot(AggregateRoot):
    tenant_id: str; civilization_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, civilization_ref: str, present: bool = True):
        if not present: raise ValueError("space.foundation.orbital_civilization_architecture_is_missing")
        return _mk(cls, tenant_id, "civilization_ref", civilization_ref, "space.foundation.orbital_civilization_architecture_is_missing", "OrbitalChangeDetectedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class AutonomousSpaceOperationsRoot(AggregateRoot):
    tenant_id: str; operations_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, operations_ref: str, present: bool = True):
        if not present: raise ValueError("space.foundation.autonomous_space_operations_platform_is_missing")
        return _mk(cls, tenant_id, "operations_ref", operations_ref, "space.foundation.autonomous_space_operations_platform_is_missing", "AutonomousMissionStartedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SpaceDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("space.foundation.space_digital_twin_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "space.foundation.space_digital_twin_is_missing", "SpaceTwinUpdatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SpaceKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present: raise ValueError("space.foundation.space_knowledge_graph_is_missing")
        return _mk(cls, tenant_id, "kg_ref", kg_ref, "space.foundation.space_knowledge_graph_is_missing", "SpaceInsightGeneratedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SpaceIntelligenceAgentsRoot(AggregateRoot):
    tenant_id: str; agents_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, agents_ref: str, present: bool = True):
        if not present: raise ValueError("space.foundation.space_intelligence_agents_are_missing")
        return _mk(cls, tenant_id, "agents_ref", agents_ref, "space.foundation.space_intelligence_agents_are_missing", "MissionOptimizedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class MeosSpaceIntelligenceCoreRoot(AggregateRoot):
    tenant_id: str; core_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, core_ref: str, present: bool = True):
        if not present: raise ValueError("space.foundation.meos_space_intelligence_core_is_missing")
        return _mk(cls, tenant_id, "core_ref", core_ref, "space.foundation.meos_space_intelligence_core_is_missing", "SpaceInsightGeneratedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SpaceTrustRoot(AggregateRoot):
    tenant_id: str; trust_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, trust_ref: str, present: bool = True):
        if not present: raise ValueError("space.foundation.space_trust_is_missing")
        return _mk(cls, tenant_id, "trust_ref", trust_ref, "space.foundation.space_trust_is_missing", "SpaceGovernanceViolationEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SpaceSecurityRoot(AggregateRoot):
    tenant_id: str; security_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, security_ref: str, present: bool = True):
        if not present: raise ValueError("space.foundation.security_architecture_is_missing")
        return _mk(cls, tenant_id, "security_ref", security_ref, "space.foundation.security_architecture_is_missing", "SpaceGovernanceViolationEvent")
    def is_missing(self)->bool: return not self.present
