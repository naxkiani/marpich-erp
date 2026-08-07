"""P218-Y aggregates — ultimate intelligence governance invariants."""
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
class UltimateGovernanceCoreRoot(AggregateRoot):
    tenant_id: str; core_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, core_ref: str, present: bool = True):
        if not present: raise ValueError("space.ultimate_governance.ultimate_intelligence_governance_is_missing")
        return _mk(cls, tenant_id, "core_ref", core_ref, "space.ultimate_governance.ultimate_intelligence_governance_is_missing", "GovernancePolicyCreatedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class IntelligenceAlignmentRoot(AggregateRoot):
    tenant_id: str; alignment_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, alignment_ref: str, present: bool = True):
        if not present: raise ValueError("space.ultimate_governance.intelligence_alignment_is_missing")
        return _mk(cls, tenant_id, "alignment_ref", alignment_ref, "space.ultimate_governance.intelligence_alignment_is_missing", "AlignmentValidatedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class FutureTrustRoot(AggregateRoot):
    tenant_id: str; trust_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, trust_ref: str, present: bool = True):
        if not present: raise ValueError("space.ultimate_governance.future_trust_architecture_is_missing")
        return _mk(cls, tenant_id, "trust_ref", trust_ref, "space.ultimate_governance.future_trust_architecture_is_missing", "TrustEstablishedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class EthicsFrameworkRoot(AggregateRoot):
    tenant_id: str; ethics_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, ethics_ref: str, present: bool = True):
        if not present: raise ValueError("space.ultimate_governance.ethics_framework_is_missing")
        return _mk(cls, tenant_id, "ethics_ref", ethics_ref, "space.ultimate_governance.ethics_framework_is_missing", "EthicalRiskDetectedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class SafetyGovernanceRoot(AggregateRoot):
    tenant_id: str; safety_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, safety_ref: str, present: bool = True):
        if not present: raise ValueError("space.ultimate_governance.safety_governance_is_missing")
        return _mk(cls, tenant_id, "safety_ref", safety_ref, "space.ultimate_governance.safety_governance_is_missing", "SafetyAssessmentCompletedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class GovernanceDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("space.ultimate_governance.digital_twin_governance_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "space.ultimate_governance.digital_twin_governance_is_missing", "GovernanceDecisionRecordedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class GovernanceKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present: raise ValueError("space.ultimate_governance.knowledge_graph_is_missing")
        return _mk(cls, tenant_id, "kg_ref", kg_ref, "space.ultimate_governance.knowledge_graph_is_missing", "AIBehaviorApprovedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class CivilizationTrustRoot(AggregateRoot):
    tenant_id: str; civilization_trust_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, civilization_trust_ref: str, present: bool = True):
        if not present: raise ValueError("space.ultimate_governance.civilization_trust_is_missing")
        return _mk(cls, tenant_id, "civilization_trust_ref", civilization_trust_ref, "space.ultimate_governance.civilization_trust_is_missing", "CivilizationTrustImprovedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class UltimateGovernanceRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("space.ultimate_governance.governance_is_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "space.ultimate_governance.governance_is_missing", "HumanAuthorityConfirmedEvent")
    def is_missing(self) -> bool: return not self.present
