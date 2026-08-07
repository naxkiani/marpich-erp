"""P218-T aggregates — civilization intelligence invariants."""
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
class CivilizationPlatformRoot(AggregateRoot):
    tenant_id: str; platform_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, platform_ref: str, present: bool = True):
        if not present: raise ValueError("space.civilization.space_civilization_platform_is_missing")
        return _mk(cls, tenant_id, "platform_ref", platform_ref, "space.civilization.space_civilization_platform_is_missing", "SettlementCreatedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class HumanSocietyRoot(AggregateRoot):
    tenant_id: str; society_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, society_ref: str, present: bool = True):
        if not present: raise ValueError("space.civilization.human_society_intelligence_is_missing")
        return _mk(cls, tenant_id, "society_ref", society_ref, "space.civilization.human_society_intelligence_is_missing", "CommunityEstablishedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class InterplanetaryGovernanceRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("space.civilization.interplanetary_governance_is_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "space.civilization.interplanetary_governance_is_missing", "GovernanceDecisionMadeEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class FutureArchitectureRoot(AggregateRoot):
    tenant_id: str; future_arch_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, future_arch_ref: str, present: bool = True):
        if not present: raise ValueError("space.civilization.future_civilization_architecture_is_missing")
        return _mk(cls, tenant_id, "future_arch_ref", future_arch_ref, "space.civilization.future_civilization_architecture_is_missing", "FutureModelUpdatedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class CivilizationAiRoot(AggregateRoot):
    tenant_id: str; civilization_ai_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, civilization_ai_ref: str, present: bool = True):
        if not present: raise ValueError("space.civilization.civilization_ai_is_missing")
        return _mk(cls, tenant_id, "civilization_ai_ref", civilization_ai_ref, "space.civilization.civilization_ai_is_missing", "CivilizationScenarioGeneratedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class CivilizationDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("space.civilization.digital_civilization_twin_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "space.civilization.digital_civilization_twin_is_missing", "SocialRiskDetectedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class CivilizationKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present: raise ValueError("space.civilization.knowledge_graph_is_missing")
        return _mk(cls, tenant_id, "kg_ref", kg_ref, "space.civilization.knowledge_graph_is_missing", "InterplanetaryAgreementCreatedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class EthicsFrameworkRoot(AggregateRoot):
    tenant_id: str; ethics_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, ethics_ref: str, present: bool = True):
        if not present: raise ValueError("space.civilization.ethics_framework_is_missing")
        return _mk(cls, tenant_id, "ethics_ref", ethics_ref, "space.civilization.ethics_framework_is_missing", "EthicsReviewCompletedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class CivilizationGovernanceRoot(AggregateRoot):
    tenant_id: str; civ_gov_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, civ_gov_ref: str, present: bool = True):
        if not present: raise ValueError("space.civilization.governance_is_missing")
        return _mk(cls, tenant_id, "civ_gov_ref", civ_gov_ref, "space.civilization.governance_is_missing", "PolicyApprovedEvent")
    def is_missing(self) -> bool: return not self.present
