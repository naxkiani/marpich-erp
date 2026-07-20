"""P207-C Identity Intelligence Domain Architecture aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId

REQUIRED_PURPOSE = frozenset(
    {
        "identity_understanding",
        "identity_reasoning",
        "identity_prediction",
        "identity_optimization",
        "autonomous_identity_operations",
        "continuous_identity_intelligence",
    }
)


@dataclass(eq=False, kw_only=True)
class DomainModelBlueprintRoot(AggregateRoot):
    """DDD blueprint — boundaries clear, not anemic."""

    tenant_id: str
    blueprint_ref: str
    purpose: tuple[str, ...]
    logical_context_count: int
    aggregate_count: int
    cqrs_ready: bool
    event_driven: bool
    anemic: bool
    boundaries_clear: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def define(
        cls,
        *,
        tenant_id: str,
        blueprint_ref: str,
        purpose: tuple[str, ...] | None = None,
        logical_context_count: int = 12,
        aggregate_count: int = 12,
        cqrs_ready: bool = True,
        event_driven: bool = True,
        anemic: bool = False,
        boundaries_clear: bool = True,
    ) -> DomainModelBlueprintRoot:
        if not tenant_id.strip():
            raise ValueError("ii.domain.tenant_required")
        p = purpose or tuple(REQUIRED_PURPOSE)
        if set(p) != REQUIRED_PURPOSE:
            raise ValueError("ii.domain.domain_purpose_absent")
        if not boundaries_clear or logical_context_count < 8:
            raise ValueError("ii.domain.ddd_boundaries_unclear")
        if anemic or aggregate_count < 8:
            raise ValueError("ii.domain.anemic_domain_model")
        if not cqrs_ready:
            raise ValueError("ii.domain.cqrs_absent")
        if not event_driven:
            raise ValueError("ii.domain.event_driven_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            blueprint_ref=blueprint_ref.strip(),
            purpose=tuple(p),
            logical_context_count=logical_context_count,
            aggregate_count=aggregate_count,
            cqrs_ready=True,
            event_driven=True,
            anemic=False,
            boundaries_clear=True,
            status="defined",
        )
        root.pending_events.append("InsightGenerated")
        root.history.append({"event": "DomainBlueprintDefined"})
        return root

    def is_unclear(self) -> bool:
        return not self.boundaries_clear

    def is_anemic(self) -> bool:
        return self.anemic


@dataclass(eq=False, kw_only=True)
class ContextMapRoot(AggregateRoot):
    tenant_id: str
    map_ref: str
    partnership: tuple[str, ...]
    replaces_peers: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(
        cls,
        *,
        tenant_id: str,
        map_ref: str,
        partnership: tuple[str, ...] | None = None,
        replaces_peers: bool = False,
    ) -> ContextMapRoot:
        if not tenant_id.strip():
            raise ValueError("ii.domain.map_tenant_required")
        peers = partnership or (
            "identity_lifecycle",
            "identity_governance",
            "privileged_access",
            "authentication",
            "directory",
            "identity_digital_twin",
        )
        if len(peers) < 4:
            raise ValueError("ii.domain.context_map_undefined")
        if replaces_peers:
            raise ValueError("ii.domain.replaces_peer_sors")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            map_ref=map_ref.strip(),
            partnership=tuple(peers),
            replaces_peers=False,
            status="published",
        )
        root.pending_events.append("GraphIntegrationConnected")
        root.history.append({"event": "ContextMapPublished"})
        return root

    def is_undefined(self) -> bool:
        return len(self.partnership) < 4


@dataclass(eq=False, kw_only=True)
class IdentityInsightRoot(AggregateRoot):
    """Non-anemic insight — explanation required."""

    tenant_id: str
    insight_ref: str
    subject_ref: str
    kind: str
    explanation: str
    confidence: float
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def generate(
        cls,
        *,
        tenant_id: str,
        insight_ref: str,
        subject_ref: str,
        kind: str = "understanding",
        explanation: str,
        confidence: float = 0.85,
    ) -> IdentityInsightRoot:
        if not tenant_id.strip() or not subject_ref.strip():
            raise ValueError("ii.domain.insight_required")
        if not explanation.strip():
            raise ValueError("ii.domain.decisions_not_explainable")
        if confidence < 0 or confidence > 1:
            raise ValueError("ii.domain.confidence_invalid")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            insight_ref=insight_ref.strip(),
            subject_ref=subject_ref.strip(),
            kind=kind.strip(),
            explanation=explanation.strip(),
            confidence=confidence,
            status="generated",
        )
        root.pending_events.append("InsightGenerated")
        root.history.append({"event": "InsightGenerated"})
        return root

    def is_anemic(self) -> bool:
        return not self.explanation.strip()


@dataclass(eq=False, kw_only=True)
class RecommendationCaseRoot(AggregateRoot):
    tenant_id: str
    case_ref: str
    subject_ref: str
    action: str
    explanation: str
    governed: bool
    human_control: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def recommend(
        cls,
        *,
        tenant_id: str,
        case_ref: str,
        subject_ref: str,
        action: str,
        explanation: str,
        governed: bool = True,
        human_control: bool = True,
    ) -> RecommendationCaseRoot:
        if not tenant_id.strip():
            raise ValueError("ii.domain.rec_tenant_required")
        if not governed:
            raise ValueError("ii.domain.automation_without_governance")
        if not human_control:
            raise ValueError("ii.domain.human_control_removed")
        if not explanation.strip():
            raise ValueError("ii.domain.decisions_not_explainable")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            case_ref=case_ref.strip(),
            subject_ref=subject_ref.strip(),
            action=action.strip(),
            explanation=explanation.strip(),
            governed=True,
            human_control=True,
            status="recommended",
        )
        root.pending_events.append("ActionRecommended")
        root.history.append({"event": "ActionRecommended"})
        return root
