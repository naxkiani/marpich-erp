"""P214-C aggregates — quality-gate invariants."""
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
class AiDomainMapRoot(AggregateRoot):
    tenant_id: str
    map_ref: str
    complete: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(cls, *, tenant_id: str, map_ref: str, complete: bool = True):
        tid = _tid(tenant_id, "ai.domain.tenant_required")
        if not complete:
            raise ValueError(
                "ai.domain.complete_ai_domain_model_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            map_ref=map_ref.strip(),
            complete=True,
            status="published",
        )
        root.pending_events.append("AIPlatformCreatedEvent")
        return root

    def is_incomplete(self) -> bool:
        return not self.complete


@dataclass(eq=False, kw_only=True)
class AiBoundedContextsRoot(AggregateRoot):
    tenant_id: str
    context_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, context_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.domain.bc_tenant_required")
        if not present:
            raise ValueError("ai.domain.bounded_contexts_are_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            context_ref=context_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("AICapabilityCreatedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class AiAggregatesDefinedRoot(AggregateRoot):
    tenant_id: str
    aggregate_ref: str
    defined: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(
        cls, *, tenant_id: str, aggregate_ref: str, defined: bool = True
    ):
        tid = _tid(tenant_id, "ai.domain.agg_tenant_required")
        if not defined:
            raise ValueError("ai.domain.aggregates_are_undefined")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            aggregate_ref=aggregate_ref.strip(),
            defined=True,
            status="published",
        )
        root.pending_events.append("AIModelRegisteredEvent")
        return root

    def is_undefined(self) -> bool:
        return not self.defined


@dataclass(eq=False, kw_only=True)
class AiEventsPresentRoot(AggregateRoot):
    tenant_id: str
    events_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, events_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.domain.events_tenant_required")
        if not present:
            raise ValueError("ai.domain.domain_events_are_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            events_ref=events_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("InferenceCompletedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class AiMicroserviceBoundariesRoot(AggregateRoot):
    tenant_id: str
    boundary_ref: str
    clear: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(
        cls, *, tenant_id: str, boundary_ref: str, clear: bool = True
    ):
        tid = _tid(tenant_id, "ai.domain.ms_tenant_required")
        if not clear:
            raise ValueError("ai.domain.microservice_mapping_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            boundary_ref=boundary_ref.strip(),
            clear=True,
            status="published",
        )
        root.pending_events.append("AIServiceActivatedEvent")
        return root

    def is_unclear(self) -> bool:
        return not self.clear


@dataclass(eq=False, kw_only=True)
class AiIntegrationBoundariesRoot(AggregateRoot):
    tenant_id: str
    integration_ref: str
    clear: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(
        cls, *, tenant_id: str, integration_ref: str, clear: bool = True
    ):
        tid = _tid(tenant_id, "ai.domain.int_tenant_required")
        if not clear:
            raise ValueError(
                "ai.domain.integration_boundaries_are_unclear"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            integration_ref=integration_ref.strip(),
            clear=True,
            status="published",
        )
        root.pending_events.append("AIComplianceCheckedEvent")
        return root

    def is_unclear(self) -> bool:
        return not self.clear
