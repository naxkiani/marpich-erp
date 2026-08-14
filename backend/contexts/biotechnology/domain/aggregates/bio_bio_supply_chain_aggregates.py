"""P217-M aggregates — biotechnology bio supply chain invariants."""
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
class BioSupplyChainPlatformRoot(AggregateRoot):
    tenant_id: str; platform_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, platform_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_supply_chain.bio_supply_chain_platform_is_missing")
        return _mk(cls, tenant_id, "platform_ref", platform_ref, "biotechnology.bio_supply_chain.bio_supply_chain_platform_is_missing", "BioSupplyChainPlatformActivatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class BioLogisticsRoot(AggregateRoot):
    tenant_id: str; logistics_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, logistics_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_supply_chain.bio_logistics_is_missing")
        return _mk(cls, tenant_id, "logistics_ref", logistics_ref, "biotechnology.bio_supply_chain.bio_logistics_is_missing", "ShipmentStartedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class ColdChainIntelligenceRoot(AggregateRoot):
    tenant_id: str; cold_chain_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, cold_chain_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_supply_chain.cold_chain_intelligence_is_missing")
        return _mk(cls, tenant_id, "cold_chain_ref", cold_chain_ref, "biotechnology.bio_supply_chain.cold_chain_intelligence_is_missing", "TemperatureAlertEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class BioInventoryIntelligenceRoot(AggregateRoot):
    tenant_id: str; inventory_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, inventory_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_supply_chain.inventory_intelligence_is_missing")
        return _mk(cls, tenant_id, "inventory_ref", inventory_ref, "biotechnology.bio_supply_chain.inventory_intelligence_is_missing", "InventoryCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class TraceabilityNetworkRoot(AggregateRoot):
    tenant_id: str; trace_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, trace_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_supply_chain.traceability_is_missing")
        return _mk(cls, tenant_id, "trace_ref", trace_ref, "biotechnology.bio_supply_chain.traceability_is_missing", "MaterialMovedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SupplyDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_supply_chain.digital_twin_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "biotechnology.bio_supply_chain.digital_twin_is_missing", "ShipmentDeliveredEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SupplyAgentsRoot(AggregateRoot):
    tenant_id: str; agents_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, agents_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_supply_chain.ai_agents_are_missing")
        return _mk(cls, tenant_id, "agents_ref", agents_ref, "biotechnology.bio_supply_chain.ai_agents_are_missing", "ColdChainRecoveredEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class BioSupplyGovernanceRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_supply_chain.governance_is_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "biotechnology.bio_supply_chain.governance_is_missing", "QualityUpdatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class BioSupplySecurityRoot(AggregateRoot):
    tenant_id: str; security_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, security_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_supply_chain.security_architecture_is_missing")
        return _mk(cls, tenant_id, "security_ref", security_ref, "biotechnology.bio_supply_chain.security_architecture_is_missing", "TemperatureAlertEvent")
    def is_missing(self)->bool: return not self.present
