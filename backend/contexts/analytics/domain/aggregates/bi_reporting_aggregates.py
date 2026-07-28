"""P213-D aggregates — quality-gate invariants."""
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
class BiReportingProfileRoot(AggregateRoot):
    tenant_id: str
    profile_ref: str
    complete: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(cls, *, tenant_id: str, profile_ref: str, complete: bool = True):
        tid = _tid(tenant_id, "analytics.reporting.tenant_required")
        if not complete:
            raise ValueError(
                "analytics.reporting.reporting_architecture_is_incomplete"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            profile_ref=profile_ref.strip(),
            complete=True,
            status="published",
        )
        root.pending_events.append("ReportPublished")
        root.pending_events.append("DashboardPublishedEvent")
        return root

    def is_incomplete(self) -> bool:
        return not self.complete


@dataclass(eq=False, kw_only=True)
class BiDashboardArchitectureRoot(AggregateRoot):
    tenant_id: str
    dashboard_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(
        cls, *, tenant_id: str, dashboard_ref: str, present: bool = True
    ):
        tid = _tid(tenant_id, "analytics.reporting.dash_tenant_required")
        if not present:
            raise ValueError(
                "analytics.reporting.dashboard_architecture_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            dashboard_ref=dashboard_ref.strip(),
            present=True,
            status="published",
        )
        root.pending_events.append("DashboardPublishedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BiVisualizationPlatformRoot(AggregateRoot):
    tenant_id: str
    viz_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(cls, *, tenant_id: str, viz_ref: str, present: bool = True):
        tid = _tid(tenant_id, "analytics.reporting.viz_tenant_required")
        if not present:
            raise ValueError(
                "analytics.reporting.visualization_platform_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            viz_ref=viz_ref.strip(),
            present=True,
            status="registered",
        )
        root.pending_events.append("VisualizationUpdatedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BiSelfServiceBiRoot(AggregateRoot):
    tenant_id: str
    layer_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, layer_ref: str, present: bool = True):
        tid = _tid(tenant_id, "analytics.reporting.ss_tenant_required")
        if not present:
            raise ValueError(
                "analytics.reporting.self_service_bi_capability_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            layer_ref=layer_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("SelfServiceEnabled")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BiAiReportingRoot(AggregateRoot):
    tenant_id: str
    ai_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, ai_ref: str, present: bool = True):
        tid = _tid(tenant_id, "analytics.reporting.ai_tenant_required")
        if not present:
            raise ValueError(
                "analytics.reporting.ai_reporting_intelligence_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            ai_ref=ai_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("AiReportingEnabled")
        return root

    def is_missing(self) -> bool:
        return not self.present
