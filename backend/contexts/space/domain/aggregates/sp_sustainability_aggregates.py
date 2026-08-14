"""P218-Q aggregates — sustainability intelligence invariants."""
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
class SustainabilityPlatformRoot(AggregateRoot):
    tenant_id: str; platform_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, platform_ref: str, present: bool = True):
        if not present: raise ValueError("space.sustainability.space_sustainability_platform_is_missing")
        return _mk(cls, tenant_id, "platform_ref", platform_ref, "space.sustainability.space_sustainability_platform_is_missing", "SpaceObjectDetectedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class OrbitalEnvironmentRoot(AggregateRoot):
    tenant_id: str; orbital_env_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, orbital_env_ref: str, present: bool = True):
        if not present: raise ValueError("space.sustainability.orbital_environment_protection_is_missing")
        return _mk(cls, tenant_id, "orbital_env_ref", orbital_env_ref, "space.sustainability.orbital_environment_protection_is_missing", "EnvironmentalRiskReducedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class DebrisManagementRoot(AggregateRoot):
    tenant_id: str; debris_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, debris_ref: str, present: bool = True):
        if not present: raise ValueError("space.sustainability.space_debris_management_is_missing")
        return _mk(cls, tenant_id, "debris_ref", debris_ref, "space.sustainability.space_debris_management_is_missing", "DebrisIdentifiedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class SpaceGovernanceRoot(AggregateRoot):
    tenant_id: str; space_gov_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, space_gov_ref: str, present: bool = True):
        if not present: raise ValueError("space.sustainability.space_governance_is_missing")
        return _mk(cls, tenant_id, "space_gov_ref", space_gov_ref, "space.sustainability.space_governance_is_missing", "PolicyUpdatedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class SustainabilityAiRoot(AggregateRoot):
    tenant_id: str; sustainability_ai_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, sustainability_ai_ref: str, present: bool = True):
        if not present: raise ValueError("space.sustainability.sustainability_ai_is_missing")
        return _mk(cls, tenant_id, "sustainability_ai_ref", sustainability_ai_ref, "space.sustainability.sustainability_ai_is_missing", "SustainabilityAssessmentCompletedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class PlanetaryProtectionRoot(AggregateRoot):
    tenant_id: str; planetary_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, planetary_ref: str, present: bool = True):
        if not present: raise ValueError("space.sustainability.planetary_protection_is_missing")
        return _mk(cls, tenant_id, "planetary_ref", planetary_ref, "space.sustainability.planetary_protection_is_missing", "PlanetaryProtectionValidatedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class SustainabilityDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("space.sustainability.digital_twin_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "space.sustainability.digital_twin_is_missing", "CleanupMissionScheduledEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class SustainabilityKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present: raise ValueError("space.sustainability.knowledge_graph_is_missing")
        return _mk(cls, tenant_id, "kg_ref", kg_ref, "space.sustainability.knowledge_graph_is_missing", "CollisionRiskDetectedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class SustainabilityGovernanceRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("space.sustainability.governance_framework_is_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "space.sustainability.governance_framework_is_missing", "SustainableOperationApprovedEvent")
    def is_missing(self) -> bool: return not self.present
