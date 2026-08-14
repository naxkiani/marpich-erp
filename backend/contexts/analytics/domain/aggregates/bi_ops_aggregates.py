"""P213-N aggregates — quality-gate invariants."""
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
class BiOpsProfileRoot(AggregateRoot):
    tenant_id: str
    profile_ref: str
    complete: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(cls, *, tenant_id: str, profile_ref: str, complete: bool = True):
        tid = _tid(tenant_id, "analytics.ops.tenant_required")
        if not complete:
            raise ValueError(
                "analytics.ops.bi_cqrs_architecture_is_incomplete"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            profile_ref=profile_ref.strip(),
            complete=True,
            status="published",
        )
        root.pending_events.append("BiCommandExecuted")
        return root

    def is_incomplete(self) -> bool:
        return not self.complete


@dataclass(eq=False, kw_only=True)
class BiCqrsPlatformRoot(AggregateRoot):
    tenant_id: str
    cqrs_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, cqrs_ref: str, present: bool = True):
        tid = _tid(tenant_id, "analytics.ops.cqrs_tenant_required")
        if not present:
            raise ValueError("analytics.ops.cqrs_architecture_is_incomplete")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            cqrs_ref=cqrs_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("CommandAcceptedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BiEventSourcingRoot(AggregateRoot):
    tenant_id: str
    store_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, store_ref: str, present: bool = True):
        tid = _tid(tenant_id, "analytics.ops.es_tenant_required")
        if not present:
            raise ValueError(
                "analytics.ops.event_sourcing_platform_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            store_ref=store_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("EventPublishedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BiEventStreamingRoot(AggregateRoot):
    tenant_id: str
    stream_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, stream_ref: str, present: bool = True):
        tid = _tid(tenant_id, "analytics.ops.stream_tenant_required")
        if not present:
            raise ValueError(
                "analytics.ops.event_streaming_platform_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            stream_ref=stream_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("ConsumerSubscribedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BiApiManagementRoot(AggregateRoot):
    tenant_id: str
    api_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, api_ref: str, present: bool = True):
        tid = _tid(tenant_id, "analytics.ops.api_tenant_required")
        if not present:
            raise ValueError(
                "analytics.ops.api_management_platform_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            api_ref=api_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("ApiRegisteredEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BiMicroservicesPlatformRoot(AggregateRoot):
    tenant_id: str
    service_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, service_ref: str, present: bool = True):
        tid = _tid(tenant_id, "analytics.ops.ms_tenant_required")
        if not present:
            raise ValueError(
                "analytics.ops.microservices_platform_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            service_ref=service_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("BiIntegrationPublished")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BiIntegrationPlatformRoot(AggregateRoot):
    tenant_id: str
    integration_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, integration_ref: str, present: bool = True
    ):
        tid = _tid(tenant_id, "analytics.ops.int_tenant_required")
        if not present:
            raise ValueError(
                "analytics.ops.enterprise_integration_platform_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            integration_ref=integration_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("BiIntegrationPublished")
        return root

    def is_missing(self) -> bool:
        return not self.present
