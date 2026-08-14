"""P218-R aggregates — commerce intelligence invariants."""
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
    obj = root_cls(
        id=UniqueId.generate(), tenant_id=tid, **{ref_name: ref_value.strip()},
        present=True, status="enabled",
    )
    obj.pending_events.append(event)
    return obj


@dataclass(eq=False, kw_only=True)
class CommercePlatformRoot(AggregateRoot):
    tenant_id: str; platform_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, platform_ref: str, present: bool = True):
        if not present: raise ValueError("space.commerce.space_commerce_platform_is_missing")
        return _mk(cls, tenant_id, "platform_ref", platform_ref, "space.commerce.space_commerce_platform_is_missing", "CompanyRegisteredEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class MarketplaceRoot(AggregateRoot):
    tenant_id: str; marketplace_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, marketplace_ref: str, present: bool = True):
        if not present: raise ValueError("space.commerce.space_marketplace_is_missing")
        return _mk(cls, tenant_id, "marketplace_ref", marketplace_ref, "space.commerce.space_marketplace_is_missing", "ServiceListedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class CommercialOperationsRoot(AggregateRoot):
    tenant_id: str; operations_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, operations_ref: str, present: bool = True):
        if not present: raise ValueError("space.commerce.commercial_operations_is_missing")
        return _mk(cls, tenant_id, "operations_ref", operations_ref, "space.commerce.commercial_operations_is_missing", "CommercialMissionCreatedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class SpaceEconomyRoot(AggregateRoot):
    tenant_id: str; economy_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, economy_ref: str, present: bool = True):
        if not present: raise ValueError("space.commerce.space_economy_intelligence_is_missing")
        return _mk(cls, tenant_id, "economy_ref", economy_ref, "space.commerce.space_economy_intelligence_is_missing", "MarketTrendDetectedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class InvestmentIntelligenceRoot(AggregateRoot):
    tenant_id: str; investment_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, investment_ref: str, present: bool = True):
        if not present: raise ValueError("space.commerce.investment_intelligence_is_missing")
        return _mk(cls, tenant_id, "investment_ref", investment_ref, "space.commerce.investment_intelligence_is_missing", "InvestmentIdentifiedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class ContractIntelligenceRoot(AggregateRoot):
    tenant_id: str; contract_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, contract_ref: str, present: bool = True):
        if not present: raise ValueError("space.commerce.contract_intelligence_is_missing")
        return _mk(cls, tenant_id, "contract_ref", contract_ref, "space.commerce.contract_intelligence_is_missing", "ContractCreatedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class CommerceAiRoot(AggregateRoot):
    tenant_id: str; commerce_ai_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, commerce_ai_ref: str, present: bool = True):
        if not present: raise ValueError("space.commerce.commerce_ai_is_missing")
        return _mk(cls, tenant_id, "commerce_ai_ref", commerce_ai_ref, "space.commerce.commerce_ai_is_missing", "BusinessRiskDetectedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class EconomicDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("space.commerce.economic_digital_twin_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "space.commerce.economic_digital_twin_is_missing", "CustomerMatchedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class CommerceGovernanceRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("space.commerce.governance_is_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "space.commerce.governance_is_missing", "SettlementPostedEvent")
    def is_missing(self) -> bool: return not self.present
