"""P213-H aggregates — quality-gate invariants."""
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
class BiSelfServiceProfileRoot(AggregateRoot):
    tenant_id: str
    profile_ref: str
    complete: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(cls, *, tenant_id: str, profile_ref: str, complete: bool = True):
        tid = _tid(tenant_id, "analytics.self_service.tenant_required")
        if not complete:
            raise ValueError(
                "analytics.self_service.self_service_bi_architecture_is_incomplete"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            profile_ref=profile_ref.strip(),
            complete=True,
            status="published",
        )
        root.pending_events.append("DatasetCertified")
        root.pending_events.append("WorkspaceCreatedEvent")
        return root

    def is_incomplete(self) -> bool:
        return not self.complete


@dataclass(eq=False, kw_only=True)
class BiAnalyticsWorkspaceRoot(AggregateRoot):
    tenant_id: str
    workspace_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls, *, tenant_id: str, workspace_ref: str, present: bool = True
    ):
        tid = _tid(tenant_id, "analytics.self_service.ws_tenant_required")
        if not present:
            raise ValueError(
                "analytics.self_service.analytics_workspace_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            workspace_ref=workspace_ref.strip(),
            present=True,
            status="created",
        )
        root.pending_events.append("WorkspaceCreatedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BiNoCodeAnalyticsRoot(AggregateRoot):
    tenant_id: str
    builder_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, builder_ref: str, present: bool = True
    ):
        tid = _tid(tenant_id, "analytics.self_service.nc_tenant_required")
        if not present:
            raise ValueError(
                "analytics.self_service.no_code_analytics_platform_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            builder_ref=builder_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("VisualizationCreatedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BiAiAssistantRoot(AggregateRoot):
    tenant_id: str
    assistant_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, assistant_ref: str, present: bool = True
    ):
        tid = _tid(tenant_id, "analytics.self_service.ai_tenant_required")
        if not present:
            raise ValueError(
                "analytics.self_service.ai_analytics_assistant_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            assistant_ref=assistant_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("InsightSharedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BiCollaborativeAnalyticsRoot(AggregateRoot):
    tenant_id: str
    collab_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, collab_ref: str, present: bool = True):
        tid = _tid(tenant_id, "analytics.self_service.col_tenant_required")
        if not present:
            raise ValueError(
                "analytics.self_service.collaborative_analytics_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            collab_ref=collab_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("InsightSharedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present
