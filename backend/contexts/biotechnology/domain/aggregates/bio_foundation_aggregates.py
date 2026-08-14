"""P217 aggregates — biotechnology / bio intelligence foundation invariants."""
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
class BiotechnologyPlatformRoot(AggregateRoot):
    tenant_id: str; bio_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, bio_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.foundation.biotechnology_platform_is_missing")
        return _mk(cls, tenant_id, "bio_ref", bio_ref, "biotechnology.foundation.biotechnology_platform_is_missing", "BioProjectCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SyntheticBiologyRoot(AggregateRoot):
    tenant_id: str; synthetic_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, synthetic_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.foundation.synthetic_biology_platform_is_missing")
        return _mk(cls, tenant_id, "synthetic_ref", synthetic_ref, "biotechnology.foundation.synthetic_biology_platform_is_missing", "SyntheticDesignCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class BioAiEngineRoot(AggregateRoot):
    tenant_id: str; bio_ai_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, bio_ai_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.foundation.bio_ai_intelligence_engine_is_missing")
        return _mk(cls, tenant_id, "bio_ai_ref", bio_ai_ref, "biotechnology.foundation.bio_ai_intelligence_engine_is_missing", "DiscoveryGeneratedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class DigitalHealthRoot(AggregateRoot):
    tenant_id: str; health_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, health_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.foundation.digital_health_platform_is_missing")
        return _mk(cls, tenant_id, "health_ref", health_ref, "biotechnology.foundation.digital_health_platform_is_missing", "HealthInsightCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class PrecisionMedicineRoot(AggregateRoot):
    tenant_id: str; precision_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, precision_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.foundation.precision_medicine_platform_is_missing")
        return _mk(cls, tenant_id, "precision_ref", precision_ref, "biotechnology.foundation.precision_medicine_platform_is_missing", "TreatmentValidatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class BiologicalDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.foundation.biological_digital_twin_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "biotechnology.foundation.biological_digital_twin_is_missing", "BiologicalTwinUpdatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class LifeScienceKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.foundation.life_science_knowledge_graph_is_missing")
        return _mk(cls, tenant_id, "kg_ref", kg_ref, "biotechnology.foundation.life_science_knowledge_graph_is_missing", "DiscoveryGeneratedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class BioEthicsGovernanceRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.foundation.bio_ethics_governance_is_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "biotechnology.foundation.bio_ethics_governance_is_missing", "TreatmentValidatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class BioSecurityRoot(AggregateRoot):
    tenant_id: str; security_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, security_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.foundation.security_architecture_is_missing")
        return _mk(cls, tenant_id, "security_ref", security_ref, "biotechnology.foundation.security_architecture_is_missing", "GenomeProcessedEvent")
    def is_missing(self)->bool: return not self.present
