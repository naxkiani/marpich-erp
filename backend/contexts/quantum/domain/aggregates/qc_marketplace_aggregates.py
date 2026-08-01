"""P215-P aggregates — quantum marketplace / economy / innovation invariants."""
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
class QuantumMarketplacePlatformRoot(AggregateRoot):
    tenant_id: str; marketplace_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, marketplace_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.marketplace.quantum_marketplace_platform_is_missing")
        return _mk(cls, tenant_id, "marketplace_ref", marketplace_ref, "quantum.marketplace.quantum_marketplace_platform_is_missing", "MarketplaceTransactionCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class CapabilityExchangePlatformRoot(AggregateRoot):
    tenant_id: str; capability_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, capability_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.marketplace.capability_exchange_platform_is_missing")
        return _mk(cls, tenant_id, "capability_ref", capability_ref, "quantum.marketplace.capability_exchange_platform_is_missing", "CapabilityRegisteredEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class QuantumServiceEconomyRoot(AggregateRoot):
    tenant_id: str; service_economy_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, service_economy_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.marketplace.quantum_service_economy_is_missing")
        return _mk(cls, tenant_id, "service_economy_ref", service_economy_ref, "quantum.marketplace.quantum_service_economy_is_missing", "ServicePublishedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class AlgorithmMarketplaceRoot(AggregateRoot):
    tenant_id: str; algorithm_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, algorithm_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.marketplace.algorithm_marketplace_is_missing")
        return _mk(cls, tenant_id, "algorithm_ref", algorithm_ref, "quantum.marketplace.algorithm_marketplace_is_missing", "AlgorithmReleasedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class ApplicationMarketplaceRoot(AggregateRoot):
    tenant_id: str; application_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, application_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.marketplace.application_marketplace_is_missing")
        return _mk(cls, tenant_id, "application_ref", application_ref, "quantum.marketplace.application_marketplace_is_missing", "ApplicationSubscribedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class InnovationEcosystemRoot(AggregateRoot):
    tenant_id: str; innovation_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, innovation_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.marketplace.innovation_ecosystem_is_missing")
        return _mk(cls, tenant_id, "innovation_ref", innovation_ref, "quantum.marketplace.innovation_ecosystem_is_missing", "InnovationProjectCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class EconomicIntelligenceRoot(AggregateRoot):
    tenant_id: str; economy_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, economy_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.marketplace.economic_intelligence_is_missing")
        return _mk(cls, tenant_id, "economy_ref", economy_ref, "quantum.marketplace.economic_intelligence_is_missing", "MarketplaceTransactionCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class MarketplaceKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; graph_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, graph_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.marketplace.knowledge_graph_integration_is_missing")
        return _mk(cls, tenant_id, "graph_ref", graph_ref, "quantum.marketplace.knowledge_graph_integration_is_missing", "CapabilityRegisteredEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class MarketplaceDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.marketplace.digital_twin_integration_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "quantum.marketplace.digital_twin_integration_is_missing", "MarketplaceTransactionCompletedEvent")
    def is_missing(self)->bool: return not self.present
