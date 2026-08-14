"""P219-C aggregates — civilization DDD domain model invariants."""
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
class CivilizationDomainModelRoot(AggregateRoot):
    tenant_id: str; domain_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, domain_ref: str, present: bool = True):
        if not present: raise ValueError("civilization.domain.civilization_os_domain_model_is_missing")
        return _mk(cls, tenant_id, "domain_ref", domain_ref, "civilization.domain.civilization_os_domain_model_is_missing", "CivilizationCreatedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class BoundedContextArchitectureRoot(AggregateRoot):
    tenant_id: str; bc_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, bc_ref: str, present: bool = True):
        if not present: raise ValueError("civilization.domain.bounded_context_architecture_is_missing")
        return _mk(cls, tenant_id, "bc_ref", bc_ref, "civilization.domain.bounded_context_architecture_is_missing", "CivilizationStateChangedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class AggregateModelRoot(AggregateRoot):
    tenant_id: str; aggregate_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, aggregate_ref: str, present: bool = True):
        if not present: raise ValueError("civilization.domain.aggregate_model_is_missing")
        return _mk(cls, tenant_id, "aggregate_ref", aggregate_ref, "civilization.domain.aggregate_model_is_missing", "CivilizationEvolutionTriggeredEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class DomainEventsModelRoot(AggregateRoot):
    tenant_id: str; events_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, events_ref: str, present: bool = True):
        if not present: raise ValueError("civilization.domain.domain_events_model_is_missing")
        return _mk(cls, tenant_id, "events_ref", events_ref, "civilization.domain.domain_events_model_is_missing", "PolicyApprovedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class CqrsModelRoot(AggregateRoot):
    tenant_id: str; cqrs_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, cqrs_ref: str, present: bool = True):
        if not present: raise ValueError("civilization.domain.cqrs_model_is_missing")
        return _mk(cls, tenant_id, "cqrs_ref", cqrs_ref, "civilization.domain.cqrs_model_is_missing", "GovernanceDecisionIssuedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class KnowledgeGraphDomainRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present: raise ValueError("civilization.domain.knowledge_graph_domain_model_is_missing")
        return _mk(cls, tenant_id, "kg_ref", kg_ref, "civilization.domain.knowledge_graph_domain_model_is_missing", "KnowledgeDiscoveredEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class DigitalTwinDomainRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("civilization.domain.digital_twin_domain_model_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "civilization.domain.digital_twin_domain_model_is_missing", "PlanetaryConditionChangedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class DomainServicesModelRoot(AggregateRoot):
    tenant_id: str; services_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, services_ref: str, present: bool = True):
        if not present: raise ValueError("civilization.domain.domain_services_model_is_missing")
        return _mk(cls, tenant_id, "services_ref", services_ref, "civilization.domain.domain_services_model_is_missing", "SystemOptimizationCompletedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class EnterpriseDddArchitectureRoot(AggregateRoot):
    tenant_id: str; ddd_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, ddd_ref: str, present: bool = True):
        if not present: raise ValueError("civilization.domain.enterprise_ddd_architecture_is_missing")
        return _mk(cls, tenant_id, "ddd_ref", ddd_ref, "civilization.domain.enterprise_ddd_architecture_is_missing", "CivilizationCreatedEvent")
    def is_missing(self) -> bool: return not self.present
