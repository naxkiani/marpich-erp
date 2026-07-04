"""Integration integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(frozen=True, kw_only=True)
class WebhookDeliveredIntegration(IntegrationEvent):
    webhook_id: UniqueId
    source_event: str
    target_url: str

    @property
    def event_name(self) -> str:
        return "integration.webhook.delivered"

    @property
    def source_context(self) -> str:
        return "integration"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "webhook_id": str(self.webhook_id),
            "source_event": self.source_event,
            "target_url": self.target_url,
        }


@dataclass(frozen=True, kw_only=True)
class WebhookFailedIntegration(IntegrationEvent):
    webhook_id: UniqueId
    source_event: str
    error: str

    @property
    def event_name(self) -> str:
        return "integration.webhook.failed"

    @property
    def source_context(self) -> str:
        return "integration"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "webhook_id": str(self.webhook_id),
            "source_event": self.source_event,
            "error": self.error,
        }


@dataclass(frozen=True, kw_only=True)
class SyncCompletedIntegration(IntegrationEvent):
    sync_job_id: UniqueId
    connector_id: UniqueId
    job_type: str

    @property
    def event_name(self) -> str:
        return "integration.sync.completed"

    @property
    def source_context(self) -> str:
        return "integration"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "sync_job_id": str(self.sync_job_id),
            "connector_id": str(self.connector_id),
            "job_type": self.job_type,
        }


@dataclass(frozen=True, kw_only=True)
class ConnectorRegisteredIntegration(IntegrationEvent):
    connector_id: UniqueId
    connector_type: str
    name: str

    @property
    def event_name(self) -> str:
        return "integration.connector.registered"

    @property
    def source_context(self) -> str:
        return "integration"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "connector_id": str(self.connector_id),
            "connector_type": self.connector_type,
            "name": self.name,
        }
