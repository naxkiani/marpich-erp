"""P218-K aggregates — scientific intelligence invariants."""
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
class ScientificIntelPlatformRoot(AggregateRoot):
    tenant_id: str; platform_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, platform_ref: str, present: bool = True):
        if not present: raise ValueError("space.scientific.scientific_intelligence_platform_is_missing")
        return _mk(cls, tenant_id, "platform_ref", platform_ref, "space.scientific.scientific_intelligence_platform_is_missing", "ResearchCreatedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class ResearchPlatformRoot(AggregateRoot):
    tenant_id: str; research_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, research_ref: str, present: bool = True):
        if not present: raise ValueError("space.scientific.space_research_platform_is_missing")
        return _mk(cls, tenant_id, "research_ref", research_ref, "space.scientific.space_research_platform_is_missing", "ResearchCreatedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class DiscoveryRoot(AggregateRoot):
    tenant_id: str; discovery_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, discovery_ref: str, present: bool = True):
        if not present: raise ValueError("space.scientific.autonomous_scientific_discovery_is_missing")
        return _mk(cls, tenant_id, "discovery_ref", discovery_ref, "space.scientific.autonomous_scientific_discovery_is_missing", "DiscoveryDetectedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class LaboratoryRoot(AggregateRoot):
    tenant_id: str; laboratory_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, laboratory_ref: str, present: bool = True):
        if not present: raise ValueError("space.scientific.space_laboratory_intelligence_is_missing")
        return _mk(cls, tenant_id, "laboratory_ref", laboratory_ref, "space.scientific.space_laboratory_intelligence_is_missing", "ExperimentStartedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class ScientificAiRoot(AggregateRoot):
    tenant_id: str; ai_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, ai_ref: str, present: bool = True):
        if not present: raise ValueError("space.scientific.scientific_ai_is_missing")
        return _mk(cls, tenant_id, "ai_ref", ai_ref, "space.scientific.scientific_ai_is_missing", "HypothesisGeneratedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class ExperimentRoot(AggregateRoot):
    tenant_id: str; experiment_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, experiment_ref: str, present: bool = True):
        if not present: raise ValueError("space.scientific.experiment_management_is_missing")
        return _mk(cls, tenant_id, "experiment_ref", experiment_ref, "space.scientific.experiment_management_is_missing", "ExperimentCompletedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class ScientificDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("space.scientific.scientific_digital_twin_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "space.scientific.scientific_digital_twin_is_missing", "ExperimentApprovedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class ScientificGovernanceRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("space.scientific.scientific_governance_is_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "space.scientific.scientific_governance_is_missing", "PublicationPublishedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class ScientificSecurityRoot(AggregateRoot):
    tenant_id: str; security_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, security_ref: str, present: bool = True):
        if not present: raise ValueError("space.scientific.security_architecture_is_missing")
        return _mk(cls, tenant_id, "security_ref", security_ref, "space.scientific.security_architecture_is_missing", "PublicationSubmittedEvent")
    def is_missing(self) -> bool: return not self.present
