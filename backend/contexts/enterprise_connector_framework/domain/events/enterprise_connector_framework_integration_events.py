"""Enterprise Connector Framework integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent


@dataclass(frozen=True, kw_only=True)
class ConnectorInstanceRegisteredIntegration(IntegrationEvent):
    instance_ref: str
    connector_type: str

    @property
    def event_name(self) -> str:
        return "enterprise_connector_framework.instance.registered"

    @property
    def source_context(self) -> str:
        return "enterprise_connector_framework"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"instance_ref": self.instance_ref, "connector_type": self.connector_type}


@dataclass(frozen=True, kw_only=True)
class ConnectorOperationExecutedIntegration(IntegrationEvent):
    execution_ref: str
    connector_type: str
    operation: str
    status: str

    @property
    def event_name(self) -> str:
        return "enterprise_connector_framework.operation.executed"

    @property
    def source_context(self) -> str:
        return "enterprise_connector_framework"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "execution_ref": self.execution_ref,
            "connector_type": self.connector_type,
            "operation": self.operation,
            "status": self.status,
        }


@dataclass(frozen=True, kw_only=True)
class ConnectorHealthCheckedIntegration(IntegrationEvent):
    instance_ref: str
    healthy: bool

    @property
    def event_name(self) -> str:
        return "enterprise_connector_framework.health.checked"

    @property
    def source_context(self) -> str:
        return "enterprise_connector_framework"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"instance_ref": self.instance_ref, "healthy": self.healthy}


@dataclass(frozen=True, kw_only=True)
class ConnectorDashboardGeneratedIntegration(IntegrationEvent):
    instances_total: int
    success_rate_pct: float

    @property
    def event_name(self) -> str:
        return "enterprise_connector_framework.dashboard.generated"

    @property
    def source_context(self) -> str:
        return "enterprise_connector_framework"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"instances_total": self.instances_total, "success_rate_pct": self.success_rate_pct}
