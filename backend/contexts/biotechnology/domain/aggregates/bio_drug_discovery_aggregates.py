"""P217-K aggregates — biotechnology drug discovery invariants."""
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
class DrugDiscoveryPlatformRoot(AggregateRoot):
    tenant_id: str; platform_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, platform_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.drug_discovery.drug_discovery_platform_is_missing")
        return _mk(cls, tenant_id, "platform_ref", platform_ref, "biotechnology.drug_discovery.drug_discovery_platform_is_missing", "DrugDiscoveryPlatformActivatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class AiDrugDesignRoot(AggregateRoot):
    tenant_id: str; design_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, design_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.drug_discovery.ai_drug_design_is_missing")
        return _mk(cls, tenant_id, "design_ref", design_ref, "biotechnology.drug_discovery.ai_drug_design_is_missing", "DrugDesignedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class MolecularDiscoveryRoot(AggregateRoot):
    tenant_id: str; molecular_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, molecular_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.drug_discovery.molecular_discovery_is_missing")
        return _mk(cls, tenant_id, "molecular_ref", molecular_ref, "biotechnology.drug_discovery.molecular_discovery_is_missing", "MoleculeDiscoveredEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class PharmaceuticalIntelligenceRoot(AggregateRoot):
    tenant_id: str; pharma_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, pharma_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.drug_discovery.pharmaceutical_intelligence_is_missing")
        return _mk(cls, tenant_id, "pharma_ref", pharma_ref, "biotechnology.drug_discovery.pharmaceutical_intelligence_is_missing", "InteractionPredictedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class DrugDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.drug_discovery.drug_digital_twin_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "biotechnology.drug_discovery.drug_digital_twin_is_missing", "TherapeuticPredictionGeneratedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class PharmaKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.drug_discovery.knowledge_graph_is_missing")
        return _mk(cls, tenant_id, "kg_ref", kg_ref, "biotechnology.drug_discovery.knowledge_graph_is_missing", "MoleculeDiscoveredEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class DrugDiscoveryAgentsRoot(AggregateRoot):
    tenant_id: str; agents_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, agents_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.drug_discovery.ai_agents_are_missing")
        return _mk(cls, tenant_id, "agents_ref", agents_ref, "biotechnology.drug_discovery.ai_agents_are_missing", "DrugOptimizedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class DrugDiscoveryGovernanceRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.drug_discovery.governance_is_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "biotechnology.drug_discovery.governance_is_missing", "DrugDiscoveryGovernanceViolationEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class DrugDiscoverySecurityRoot(AggregateRoot):
    tenant_id: str; security_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, security_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.drug_discovery.security_architecture_is_missing")
        return _mk(cls, tenant_id, "security_ref", security_ref, "biotechnology.drug_discovery.security_architecture_is_missing", "DrugDiscoveryGovernanceViolationEvent")
    def is_missing(self)->bool: return not self.present
