"""P215-C aggregates — quantum DDD domain invariants."""
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
class DomainModelRoot(AggregateRoot):
    tenant_id: str; domain_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, domain_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.domain.quantum_domain_model_is_missing")
        return _mk(cls, tenant_id, "domain_ref", domain_ref, "quantum.domain.quantum_domain_model_is_missing", "QuantumCapabilityCreatedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class BoundedContextRoot(AggregateRoot):
    tenant_id: str; context_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, context_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.domain.bounded_context_architecture_is_missing")
        return _mk(cls, tenant_id, "context_ref", context_ref, "quantum.domain.bounded_context_architecture_is_missing", "QuantumPlatformActivatedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class AggregateArchitectureRoot(AggregateRoot):
    tenant_id: str; aggregate_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, aggregate_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.domain.aggregate_architecture_is_missing")
        return _mk(cls, tenant_id, "aggregate_ref", aggregate_ref, "quantum.domain.aggregate_architecture_is_missing", "QuantumAlgorithmPublishedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class ContextMapRoot(AggregateRoot):
    tenant_id: str; map_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, map_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.domain.context_mapping_is_missing")
        return _mk(cls, tenant_id, "map_ref", map_ref, "quantum.domain.context_mapping_is_missing", "QuantumGovernanceApprovedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class DomainEventArchRoot(AggregateRoot):
    tenant_id: str; event_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, event_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.domain.domain_event_architecture_is_missing")
        return _mk(cls, tenant_id, "event_ref", event_ref, "quantum.domain.domain_event_architecture_is_missing", "QuantumExperimentCompletedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class KnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; graph_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, graph_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.domain.knowledge_graph_model_is_missing")
        return _mk(cls, tenant_id, "graph_ref", graph_ref, "quantum.domain.knowledge_graph_model_is_missing", "QuantumCapabilityCreatedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class DomainTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.domain.digital_twin_model_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "quantum.domain.digital_twin_model_is_missing", "QuantumOptimizationExecutedEvent")
    def is_missing(self)->bool: return not self.present
