"""P217-Z aggregates — biotechnology bio nexus invariants."""
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
class UltimateBioMasterRoot(AggregateRoot):
    tenant_id: str; master_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, master_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_nexus.ultimate_bio_master_architecture_is_missing")
        return _mk(cls, tenant_id, "master_ref", master_ref, "biotechnology.bio_nexus.ultimate_bio_master_architecture_is_missing", "BioNexusPlatformActivatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class BioSupremeControlPlaneRoot(AggregateRoot):
    tenant_id: str; control_plane_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, control_plane_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_nexus.meos_bio_supreme_control_plane_is_missing")
        return _mk(cls, tenant_id, "control_plane_ref", control_plane_ref, "biotechnology.bio_nexus.meos_bio_supreme_control_plane_is_missing", "ControlPlaneOrchestratedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class AutonomousBiologicalNexusRoot(AggregateRoot):
    tenant_id: str; nexus_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, nexus_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_nexus.autonomous_biological_intelligence_nexus_is_missing")
        return _mk(cls, tenant_id, "nexus_ref", nexus_ref, "biotechnology.bio_nexus.autonomous_biological_intelligence_nexus_is_missing", "NexusCapabilityRegisteredEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class BioCivilizationIntelligenceCoreRoot(AggregateRoot):
    tenant_id: str; core_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, core_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_nexus.bio_civilization_intelligence_core_is_missing")
        return _mk(cls, tenant_id, "core_ref", core_ref, "biotechnology.bio_nexus.bio_civilization_intelligence_core_is_missing", "CivilizationStrategyCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class UniversalBioKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_nexus.universal_bio_knowledge_graph_is_missing")
        return _mk(cls, tenant_id, "kg_ref", kg_ref, "biotechnology.bio_nexus.universal_bio_knowledge_graph_is_missing", "BioIntelligenceCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class UltimateBioDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_nexus.ultimate_bio_digital_twin_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "biotechnology.bio_nexus.ultimate_bio_digital_twin_is_missing", "FutureStateReachedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SupremeBioAgentsRoot(AggregateRoot):
    tenant_id: str; agents_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, agents_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_nexus.supreme_bio_intelligence_agents_are_missing")
        return _mk(cls, tenant_id, "agents_ref", agents_ref, "biotechnology.bio_nexus.supreme_bio_intelligence_agents_are_missing", "EvolutionAdvancedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class FinalBioIntelligenceArchitectureRoot(AggregateRoot):
    tenant_id: str; architecture_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, architecture_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_nexus.meos_final_bio_intelligence_architecture_is_missing")
        return _mk(cls, tenant_id, "architecture_ref", architecture_ref, "biotechnology.bio_nexus.meos_final_bio_intelligence_architecture_is_missing", "BioNexusPlatformActivatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class HumanSupremeOversightRoot(AggregateRoot):
    tenant_id: str; oversight_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, oversight_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_nexus.human_supreme_oversight_is_missing")
        return _mk(cls, tenant_id, "oversight_ref", oversight_ref, "biotechnology.bio_nexus.human_supreme_oversight_is_missing", "NexusGovernanceViolationEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class BioNexusSecurityRoot(AggregateRoot):
    tenant_id: str; security_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, security_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_nexus.security_architecture_is_missing")
        return _mk(cls, tenant_id, "security_ref", security_ref, "biotechnology.bio_nexus.security_architecture_is_missing", "NexusGovernanceViolationEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class BioNexusGovernanceRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_nexus.governance_architecture_is_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "biotechnology.bio_nexus.governance_architecture_is_missing", "NexusGovernanceViolationEvent")
    def is_missing(self)->bool: return not self.present
