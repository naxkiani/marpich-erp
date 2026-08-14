"""P215-Q aggregates — quantum research / innovation lab / discovery invariants."""
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
class QuantumResearchPlatformRoot(AggregateRoot):
    tenant_id: str; research_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, research_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.research.quantum_research_platform_is_missing")
        return _mk(cls, tenant_id, "research_ref", research_ref, "quantum.research.quantum_research_platform_is_missing", "ResearchStartedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class QuantumInnovationLabRoot(AggregateRoot):
    tenant_id: str; lab_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, lab_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.research.quantum_innovation_lab_is_missing")
        return _mk(cls, tenant_id, "lab_ref", lab_ref, "quantum.research.quantum_innovation_lab_is_missing", "InnovationValidatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class ScientificCollaborationPlatformRoot(AggregateRoot):
    tenant_id: str; collaboration_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, collaboration_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.research.scientific_collaboration_platform_is_missing")
        return _mk(cls, tenant_id, "collaboration_ref", collaboration_ref, "quantum.research.scientific_collaboration_platform_is_missing", "PublicationReleasedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class DiscoveryIntelligenceRoot(AggregateRoot):
    tenant_id: str; discovery_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, discovery_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.research.discovery_intelligence_is_missing")
        return _mk(cls, tenant_id, "discovery_ref", discovery_ref, "quantum.research.discovery_intelligence_is_missing", "DiscoveryCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class AiAssistedResearchRoot(AggregateRoot):
    tenant_id: str; copilot_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, copilot_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.research.ai_assisted_research_is_missing")
        return _mk(cls, tenant_id, "copilot_ref", copilot_ref, "quantum.research.ai_assisted_research_is_missing", "DiscoveryGeneratedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class ExperimentManagementRoot(AggregateRoot):
    tenant_id: str; experiment_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, experiment_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.research.experiment_management_is_missing")
        return _mk(cls, tenant_id, "experiment_ref", experiment_ref, "quantum.research.experiment_management_is_missing", "ExperimentExecutedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class FutureTechnologyRadarRoot(AggregateRoot):
    tenant_id: str; radar_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, radar_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.research.future_technology_radar_is_missing")
        return _mk(cls, tenant_id, "radar_ref", radar_ref, "quantum.research.future_technology_radar_is_missing", "FutureTechnologyDetectedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class ResearchKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; graph_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, graph_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.research.knowledge_graph_integration_is_missing")
        return _mk(cls, tenant_id, "graph_ref", graph_ref, "quantum.research.knowledge_graph_integration_is_missing", "DiscoveryCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class ResearchDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.research.digital_twin_integration_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "quantum.research.digital_twin_integration_is_missing", "ExperimentExecutedEvent")
    def is_missing(self)->bool: return not self.present
