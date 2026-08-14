"""P214-B aggregates — quality-gate invariants."""
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
class AiMissionDefinedRoot(AggregateRoot):
    tenant_id: str
    mission_ref: str
    defined: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(cls, *, tenant_id: str, mission_ref: str, defined: bool = True):
        tid = _tid(tenant_id, "ai.mission.tenant_required")
        if not defined:
            raise ValueError("ai.mission.mission_is_undefined")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            mission_ref=mission_ref.strip(),
            defined=True,
            status="published",
        )
        root.pending_events.append("AiMissionPublishedEvent")
        return root

    def is_undefined(self) -> bool:
        return not self.defined


@dataclass(eq=False, kw_only=True)
class AiVisionDefinedRoot(AggregateRoot):
    tenant_id: str
    vision_ref: str
    defined: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(cls, *, tenant_id: str, vision_ref: str, defined: bool = True):
        tid = _tid(tenant_id, "ai.mission.vision_tenant_required")
        if not defined:
            raise ValueError("ai.mission.vision_is_undefined")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            vision_ref=vision_ref.strip(),
            defined=True,
            status="published",
        )
        root.pending_events.append("AiVisionPublishedEvent")
        return root

    def is_undefined(self) -> bool:
        return not self.defined


@dataclass(eq=False, kw_only=True)
class AiCapabilityMapRoot(AggregateRoot):
    tenant_id: str
    map_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, map_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.mission.map_tenant_required")
        if not present:
            raise ValueError("ai.mission.ai_capability_map_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            map_ref=map_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("AiStrategicObjectiveRegisteredEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class AiMaturityModelRoot(AggregateRoot):
    tenant_id: str
    maturity_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, maturity_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.mission.maturity_tenant_required")
        if not present:
            raise ValueError("ai.mission.ai_maturity_model_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            maturity_ref=maturity_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("AiMaturityLevelAssessedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class AiGovernanceStrategyRoot(AggregateRoot):
    tenant_id: str
    governance_ref: str
    defined: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(
        cls, *, tenant_id: str, governance_ref: str, defined: bool = True
    ):
        tid = _tid(tenant_id, "ai.mission.gov_tenant_required")
        if not defined:
            raise ValueError(
                "ai.mission.ai_governance_strategy_is_undefined"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            governance_ref=governance_ref.strip(),
            defined=True,
            status="published",
        )
        root.pending_events.append("AiGovernanceStrategyValidatedEvent")
        return root

    def is_undefined(self) -> bool:
        return not self.defined


@dataclass(eq=False, kw_only=True)
class AiRoadmapRoot(AggregateRoot):
    tenant_id: str
    roadmap_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, roadmap_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.mission.roadmap_tenant_required")
        if not present:
            raise ValueError(
                "ai.mission.ai_transformation_roadmap_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            roadmap_ref=roadmap_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("AiTransformationPhaseApprovedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present
