"""Identity resilience platform aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class ResilienceCapability(StrEnum):
    REGION_CATALOG = "region_catalog"
    WORKER_REGISTRY = "worker_registry"
    DIRECTORY_SYNC_WORKER_HA = "directory_sync_worker_ha"
    RISK_SCORING_WORKER_HA = "risk_scoring_worker_ha"
    LEADER_ELECTION = "leader_election"
    FAILOVER_ORCHESTRATION = "failover_orchestration"
    REPLICATION_HEALTH = "replication_health"
    POLICY_DRIVEN_RESILIENCE = "policy_driven_resilience"
    RESILIENCE_DASHBOARD = "resilience_dashboard"
    IDENTITY_RESILIENCE_API = "identity_resilience_api"


class WorkerType(StrEnum):
    DIRECTORY_SYNC = "directory_sync"
    RISK_SCORING = "risk_scoring"


class WorkerRole(StrEnum):
    LEADER = "leader"
    STANDBY = "standby"


class WorkerStatus(StrEnum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    OFFLINE = "offline"


class RegionHealth(StrEnum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"


class FailoverStatus(StrEnum):
    INITIATED = "initiated"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(eq=False, kw_only=True)
class ResilienceProfile(AggregateRoot):
    tenant_id: str
    profile_ref: str
    multi_region_enabled: bool = True
    auto_failover: bool = True
    heartbeat_timeout_seconds: int = 60
    replication_lag_threshold_seconds: int = 30
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(cls, *, tenant_id: str, profile_ref: str) -> ResilienceProfile:
        return cls(id=UniqueId.generate(), tenant_id=tenant_id, profile_ref=profile_ref)

    def to_dict(self) -> dict:
        return {
            "profile_ref": self.profile_ref,
            "tenant_id": self.tenant_id,
            "multi_region_enabled": self.multi_region_enabled,
            "auto_failover": self.auto_failover,
            "heartbeat_timeout_seconds": self.heartbeat_timeout_seconds,
            "replication_lag_threshold_seconds": self.replication_lag_threshold_seconds,
        }


@dataclass(eq=False, kw_only=True)
class RegionDescriptor(AggregateRoot):
    tenant_id: str
    region_ref: str
    region_id: str
    display_name: str
    is_primary: bool = False
    replication_lag_seconds: int = 0
    health: str = RegionHealth.HEALTHY.value
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(
        cls,
        *,
        tenant_id: str,
        region_ref: str,
        region_id: str,
        display_name: str,
        is_primary: bool = False,
    ) -> RegionDescriptor:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            region_ref=region_ref,
            region_id=region_id,
            display_name=display_name,
            is_primary=is_primary,
        )

    def update_health(self, *, lag_seconds: int, threshold: int) -> None:
        self.replication_lag_seconds = lag_seconds
        if lag_seconds > threshold * 2:
            self.health = RegionHealth.UNAVAILABLE.value
        elif lag_seconds > threshold:
            self.health = RegionHealth.DEGRADED.value
        else:
            self.health = RegionHealth.HEALTHY.value

    def to_dict(self) -> dict:
        return {
            "region_ref": self.region_ref,
            "tenant_id": self.tenant_id,
            "region_id": self.region_id,
            "display_name": self.display_name,
            "is_primary": self.is_primary,
            "replication_lag_seconds": self.replication_lag_seconds,
            "health": self.health,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class WorkerDeployment(AggregateRoot):
    tenant_id: str
    worker_ref: str
    worker_type: str
    region_id: str
    role: str
    status: str = WorkerStatus.HEALTHY.value
    last_heartbeat_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def deploy(
        cls,
        *,
        tenant_id: str,
        worker_ref: str,
        worker_type: str,
        region_id: str,
        role: str,
    ) -> WorkerDeployment:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            worker_ref=worker_ref,
            worker_type=worker_type,
            region_id=region_id,
            role=role,
        )

    def heartbeat(self) -> None:
        self.last_heartbeat_at = datetime.now(UTC)
        self.status = WorkerStatus.HEALTHY.value

    def mark_offline(self) -> None:
        self.status = WorkerStatus.OFFLINE.value

    def promote_leader(self) -> None:
        self.role = WorkerRole.LEADER.value
        self.status = WorkerStatus.HEALTHY.value

    def demote_standby(self) -> None:
        self.role = WorkerRole.STANDBY.value

    def to_dict(self) -> dict:
        return {
            "worker_ref": self.worker_ref,
            "tenant_id": self.tenant_id,
            "worker_type": self.worker_type,
            "region_id": self.region_id,
            "role": self.role,
            "status": self.status,
            "last_heartbeat_at": self.last_heartbeat_at.isoformat() if self.last_heartbeat_at else None,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class FailoverEvent(AggregateRoot):
    tenant_id: str
    failover_ref: str
    worker_type: str
    from_region_id: str
    to_region_id: str
    reason: str
    status: str = FailoverStatus.INITIATED.value
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    completed_at: datetime | None = None

    @classmethod
    def initiate(
        cls,
        *,
        tenant_id: str,
        failover_ref: str,
        worker_type: str,
        from_region_id: str,
        to_region_id: str,
        reason: str,
    ) -> FailoverEvent:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            failover_ref=failover_ref,
            worker_type=worker_type,
            from_region_id=from_region_id,
            to_region_id=to_region_id,
            reason=reason,
        )

    def complete(self) -> None:
        self.status = FailoverStatus.COMPLETED.value
        self.completed_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "failover_ref": self.failover_ref,
            "tenant_id": self.tenant_id,
            "worker_type": self.worker_type,
            "from_region_id": self.from_region_id,
            "to_region_id": self.to_region_id,
            "reason": self.reason,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }
