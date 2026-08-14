"""P217-C aggregates — biotechnology DDD bounded-context invariants."""
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
class CoreDomainRoot(AggregateRoot):
    tenant_id: str; domain_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, domain_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.domain.biotechnology_core_domain_is_missing")
        return _mk(cls, tenant_id, "domain_ref", domain_ref, "biotechnology.domain.biotechnology_core_domain_is_missing", "BioIntelligenceCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class BoundedContextMapRoot(AggregateRoot):
    tenant_id: str; map_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, map_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.domain.bounded_context_map_is_missing")
        return _mk(cls, tenant_id, "map_ref", map_ref, "biotechnology.domain.bounded_context_map_is_missing", "BioIntelligenceCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class BioIntelligenceDomainRoot(AggregateRoot):
    tenant_id: str; intelligence_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, intelligence_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.domain.aggregates_are_missing")
        return _mk(cls, tenant_id, "intelligence_ref", intelligence_ref, "biotechnology.domain.aggregates_are_missing", "BioIntelligenceCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SyntheticBiologyDomainRoot(AggregateRoot):
    tenant_id: str; synthetic_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, synthetic_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.domain.aggregates_are_missing")
        return _mk(cls, tenant_id, "synthetic_ref", synthetic_ref, "biotechnology.domain.aggregates_are_missing", "SyntheticSystemDesignedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class ComputationalBiologyDomainRoot(AggregateRoot):
    tenant_id: str; computational_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, computational_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.domain.aggregates_are_missing")
        return _mk(cls, tenant_id, "computational_ref", computational_ref, "biotechnology.domain.aggregates_are_missing", "GenomeProcessedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class DigitalHealthDomainRoot(AggregateRoot):
    tenant_id: str; health_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, health_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.domain.aggregates_are_missing")
        return _mk(cls, tenant_id, "health_ref", health_ref, "biotechnology.domain.aggregates_are_missing", "HealthPredictionGeneratedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class BioDigitalTwinDomainRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.domain.aggregates_are_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "biotechnology.domain.aggregates_are_missing", "BiologicalSimulationCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class ResearchIntelligenceDomainRoot(AggregateRoot):
    tenant_id: str; research_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, research_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.domain.aggregates_are_missing")
        return _mk(cls, tenant_id, "research_ref", research_ref, "biotechnology.domain.aggregates_are_missing", "ResearchDiscoveryCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class BioGovernanceDomainRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.domain.aggregates_are_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "biotechnology.domain.aggregates_are_missing", "GovernanceApprovalCompletedEvent")
    def is_missing(self)->bool: return not self.present
