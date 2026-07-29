"""P214-R aggregates — quality-gate invariants."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


def _tid(tenant_id: str, code: str) -> str:
    if not tenant_id.strip():
        raise ValueError(code)
    return tenant_id.strip()


@dataclass(eq=False, kw_only=True)
class MarketplaceRoot(AggregateRoot):
    tenant_id: str
    marketplace_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, marketplace_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aimarket.tenant_required")
        if not present:
            raise ValueError("ai.aimarket.enterprise_ai_marketplace_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, marketplace_ref=marketplace_ref.strip(), present=True, status="enabled")
        root.pending_events.append("ListingCreatedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class CapabilityRegistryRoot(AggregateRoot):
    tenant_id: str
    capability_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, capability_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aimarket.capability_tenant_required")
        if not present:
            raise ValueError("ai.aimarket.ai_capability_registry_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, capability_ref=capability_ref.strip(), present=True, status="enabled")
        root.pending_events.append("CapabilityPublishedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class ModelExchangeRoot(AggregateRoot):
    tenant_id: str
    model_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, model_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aimarket.model_tenant_required")
        if not present:
            raise ValueError("ai.aimarket.ai_model_exchange_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, model_ref=model_ref.strip(), present=True, status="enabled")
        root.pending_events.append("AssetRegisteredEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class AgentExchangeRoot(AggregateRoot):
    tenant_id: str
    agent_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, agent_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aimarket.agent_tenant_required")
        if not present:
            raise ValueError("ai.aimarket.ai_agent_marketplace_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, agent_ref=agent_ref.strip(), present=True, status="enabled")
        root.pending_events.append("CapabilityPublishedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class ServiceCatalogRoot(AggregateRoot):
    tenant_id: str
    service_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, service_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aimarket.service_tenant_required")
        if not present:
            raise ValueError("ai.aimarket.ai_service_marketplace_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, service_ref=service_ref.strip(), present=True, status="enabled")
        root.pending_events.append("SubscriptionActivatedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class PluginMarketplaceRoot(AggregateRoot):
    tenant_id: str
    plugin_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, plugin_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aimarket.plugin_tenant_required")
        if not present:
            raise ValueError("ai.aimarket.ai_plugin_marketplace_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, plugin_ref=plugin_ref.strip(), present=True, status="enabled")
        root.pending_events.append("PluginValidatedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class EconomyRoot(AggregateRoot):
    tenant_id: str
    economy_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, economy_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aimarket.economy_tenant_required")
        if not present:
            raise ValueError("ai.aimarket.ai_economy_platform_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, economy_ref=economy_ref.strip(), present=True, status="enabled")
        root.pending_events.append("ContractCompletedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class MarketplaceDigitalTwinRoot(AggregateRoot):
    tenant_id: str
    twin_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aimarket.twin_tenant_required")
        if not present:
            raise ValueError("ai.aimarket.digital_twin_integration_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, twin_ref=twin_ref.strip(), present=True, status="enabled")
        root.pending_events.append("RatingUpdatedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present
