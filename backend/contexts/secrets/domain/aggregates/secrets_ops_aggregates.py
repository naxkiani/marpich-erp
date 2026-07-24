"""P209-L CQRS, Events, APIs & Microservices aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class SecretsOpsDbOwnershipRoot(AggregateRoot):
    """Services must not share databases."""

    tenant_id: str
    service_ref: str
    owns_database: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def verify(
        cls,
        *,
        tenant_id: str,
        service_ref: str,
        owns_database: bool = True,
        shares_database: bool = False,
    ) -> SecretsOpsDbOwnershipRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.ops.db_tenant_required")
        if shares_database or not owns_database:
            raise ValueError("secrets.ops.services_share_databases")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            service_ref=service_ref.strip(),
            owns_database=True,
            status="verified",
        )
        root.pending_events.append("OpsDbOwnershipVerified")
        root.history.append({"event": "OpsDbOwnershipVerified"})
        return root

    def shares_databases(self) -> bool:
        return not self.owns_database


@dataclass(eq=False, kw_only=True)
class SecretsOpsEventsPresentRoot(AggregateRoot):
    """Events must not be missing."""

    tenant_id: str
    stream_ref: str
    events_present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def verify(
        cls,
        *,
        tenant_id: str,
        stream_ref: str,
        events_present: bool = True,
    ) -> SecretsOpsEventsPresentRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.ops.events_tenant_required")
        if not events_present:
            raise ValueError("secrets.ops.events_are_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            stream_ref=stream_ref.strip(),
            events_present=True,
            status="verified",
        )
        root.pending_events.append("OpsEventsPresent")
        root.pending_events.append("TrustCreated")
        root.history.append({"event": "OpsEventsPresent"})
        return root

    def are_missing(self) -> bool:
        return not self.events_present


@dataclass(eq=False, kw_only=True)
class SecretsOpsApiSecurityRoot(AggregateRoot):
    """APIs must not lack security."""

    tenant_id: str
    api_ref: str
    secured: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def secure(
        cls,
        *,
        tenant_id: str,
        api_ref: str,
        secured: bool = True,
    ) -> SecretsOpsApiSecurityRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.ops.api_tenant_required")
        if not secured:
            raise ValueError("secrets.ops.apis_lack_security")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            api_ref=api_ref.strip(),
            secured=True,
            status="secured",
        )
        root.pending_events.append("OpsApiSecured")
        root.history.append({"event": "OpsApiSecured"})
        return root

    def lacks_security(self) -> bool:
        return not self.secured


@dataclass(eq=False, kw_only=True)
class SecretsOpsCryptoAuditableRoot(AggregateRoot):
    """Cryptographic operations must be auditable."""

    tenant_id: str
    operation_ref: str
    auditable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def record(
        cls,
        *,
        tenant_id: str,
        operation_ref: str,
        auditable: bool = True,
    ) -> SecretsOpsCryptoAuditableRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.ops.crypto_tenant_required")
        if not auditable:
            raise ValueError(
                "secrets.ops.cryptographic_operations_not_auditable"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            operation_ref=operation_ref.strip(),
            auditable=True,
            status="recorded",
        )
        root.pending_events.append("OpsCryptoAudited")
        root.pending_events.append("EncryptionExecuted")
        root.history.append({"event": "OpsCryptoAudited"})
        return root

    def is_unauditable(self) -> bool:
        return not self.auditable


@dataclass(eq=False, kw_only=True)
class SecretsOpsServiceOwnershipRoot(AggregateRoot):
    """Microservices must have clear ownership."""

    tenant_id: str
    service_ref: str
    ownership_clear: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def assign(
        cls,
        *,
        tenant_id: str,
        service_ref: str,
        ownership_clear: bool = True,
    ) -> SecretsOpsServiceOwnershipRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.ops.own_tenant_required")
        if not ownership_clear:
            raise ValueError("secrets.ops.microservices_unclear_ownership")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            service_ref=service_ref.strip(),
            ownership_clear=True,
            status="assigned",
        )
        root.pending_events.append("OpsOwnershipClear")
        root.history.append({"event": "OpsOwnershipClear"})
        return root

    def is_unclear(self) -> bool:
        return not self.ownership_clear


@dataclass(eq=False, kw_only=True)
class SecretsOpsObservabilityRoot(AggregateRoot):
    """Observability must be complete."""

    tenant_id: str
    service_ref: str
    complete: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def complete_surface(
        cls,
        *,
        tenant_id: str,
        service_ref: str,
        complete: bool = True,
    ) -> SecretsOpsObservabilityRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.ops.obs_tenant_required")
        if not complete:
            raise ValueError("secrets.ops.observability_incomplete")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            service_ref=service_ref.strip(),
            complete=True,
            status="complete",
        )
        root.pending_events.append("OpsObservabilityComplete")
        root.history.append({"event": "OpsObservabilityComplete"})
        return root

    def is_incomplete(self) -> bool:
        return not self.complete


@dataclass(eq=False, kw_only=True)
class SecretsOpsScalableDeployRoot(AggregateRoot):
    """Deployment must scale."""

    tenant_id: str
    deploy_ref: str
    scalable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls,
        *,
        tenant_id: str,
        deploy_ref: str,
        scalable: bool = True,
    ) -> SecretsOpsScalableDeployRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.ops.deploy_tenant_required")
        if not scalable:
            raise ValueError("secrets.ops.deployment_cannot_scale")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            deploy_ref=deploy_ref.strip(),
            scalable=True,
            status="enabled",
        )
        root.pending_events.append("OpsDeploymentScalable")
        root.history.append({"event": "OpsDeploymentScalable"})
        return root

    def cannot_scale(self) -> bool:
        return not self.scalable


@dataclass(eq=False, kw_only=True)
class SecretsOpsSeriesCloseoutRoot(AggregateRoot):
    """P209 series closeout marker."""

    tenant_id: str
    series_ref: str
    closed: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def close(
        cls,
        *,
        tenant_id: str,
        series_ref: str = "P209",
        closed: bool = True,
    ) -> SecretsOpsSeriesCloseoutRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.ops.close_tenant_required")
        if not closed:
            raise ValueError("secrets.ops.deployment_cannot_scale")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            series_ref=series_ref.strip(),
            closed=True,
            status="closed",
        )
        root.pending_events.append("OpsSeriesClosed")
        root.history.append({"event": "OpsSeriesClosed"})
        return root

    def is_open(self) -> bool:
        return not self.closed
