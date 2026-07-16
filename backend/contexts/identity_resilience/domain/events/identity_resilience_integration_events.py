"""Identity resilience integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent


@dataclass(frozen=True, kw_only=True)
class WorkerRegisteredIntegration(IntegrationEvent):
    worker_ref: str
    worker_type: str
    region_id: str

    @property
    def event_name(self) -> str:
        return "identity_resilience.worker.registered"

    @property
    def source_context(self) -> str:
        return "identity_resilience"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "worker_ref": self.worker_ref,
            "worker_type": self.worker_type,
            "region_id": self.region_id,
        }


@dataclass(frozen=True, kw_only=True)
class FailoverInitiatedIntegration(IntegrationEvent):
    failover_ref: str
    worker_type: str
    from_region_id: str
    to_region_id: str

    @property
    def event_name(self) -> str:
        return "identity_resilience.failover.initiated"

    @property
    def source_context(self) -> str:
        return "identity_resilience"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "failover_ref": self.failover_ref,
            "worker_type": self.worker_type,
            "from_region_id": self.from_region_id,
            "to_region_id": self.to_region_id,
        }


@dataclass(frozen=True, kw_only=True)
class FailoverCompletedIntegration(IntegrationEvent):
    failover_ref: str
    worker_type: str
    to_region_id: str

    @property
    def event_name(self) -> str:
        return "identity_resilience.failover.completed"

    @property
    def source_context(self) -> str:
        return "identity_resilience"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "failover_ref": self.failover_ref,
            "worker_type": self.worker_type,
            "to_region_id": self.to_region_id,
        }


@dataclass(frozen=True, kw_only=True)
class RegionHealthChangedIntegration(IntegrationEvent):
    region_id: str
    health: str
    replication_lag_seconds: int

    @property
    def event_name(self) -> str:
        return "identity_resilience.region.health_changed"

    @property
    def source_context(self) -> str:
        return "identity_resilience"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "region_id": self.region_id,
            "health": self.health,
            "replication_lag_seconds": self.replication_lag_seconds,
        }
