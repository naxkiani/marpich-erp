"""Enterprise Connector Framework aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class ConnectorFrameworkCapability(StrEnum):
    CORE_BANKING_SYSTEMS = "core_banking_systems"
    PAYMENT_GATEWAYS = "payment_gateways"
    GOVERNMENT_SERVICES = "government_services"
    TAX_AUTHORITIES = "tax_authorities"
    CENTRAL_BANKS = "central_banks"
    ERP_SYSTEMS = "erp_systems"
    CRM_SYSTEMS = "crm_systems"
    MOODLE = "moodle"
    GOOGLE_CLASSROOM = "google_classroom"
    MICROSOFT_365 = "microsoft_365"
    GOOGLE_WORKSPACE = "google_workspace"
    LDAP = "ldap"
    ACTIVE_DIRECTORY = "active_directory"
    AZURE_AD = "azure_ad"
    EMAIL = "email"
    SMS = "sms"
    WHATSAPP_BUSINESS_API = "whatsapp_business_api"
    PUSH_NOTIFICATIONS = "push_notifications"
    CLOUD_STORAGE = "cloud_storage"
    DOCUMENT_MANAGEMENT_SYSTEMS = "document_management_systems"
    PLUGIN_ARCHITECTURE = "plugin_architecture"
    CONNECTOR_SDK = "connector_sdk"
    CONNECTOR_MONITORING = "connector_monitoring"
    CONNECTOR_MANAGEMENT_CONSOLE = "connector_management_console"


class ConnectorInstanceStatus(StrEnum):
    REGISTERED = "registered"
    ACTIVE = "active"
    DEGRADED = "degraded"
    DISABLED = "disabled"


class ExecutionStatus(StrEnum):
    PENDING = "pending"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


@dataclass(eq=False, kw_only=True)
class ConnectorFrameworkProfile(AggregateRoot):
    tenant_id: str
    profile_ref: str
    health_check_enabled: bool = True
    retry_enabled: bool = True
    plugin_connectors_enabled: bool = True
    sdk_extensions_enabled: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(cls, *, tenant_id: str, profile_ref: str) -> ConnectorFrameworkProfile:
        return cls(id=UniqueId.generate(), tenant_id=tenant_id, profile_ref=profile_ref)

    def to_dict(self) -> dict:
        return {
            "profile_ref": self.profile_ref,
            "tenant_id": self.tenant_id,
            "health_check_enabled": self.health_check_enabled,
            "retry_enabled": self.retry_enabled,
            "plugin_connectors_enabled": self.plugin_connectors_enabled,
            "sdk_extensions_enabled": self.sdk_extensions_enabled,
        }


@dataclass(eq=False, kw_only=True)
class ConnectorInstance(AggregateRoot):
    tenant_id: str
    instance_ref: str
    connector_type: str
    display_name: str
    category: str
    direction: str
    config: dict = field(default_factory=dict)
    secret_ref: str = ""
    plugin_id: str = ""
    status: str = ConnectorInstanceStatus.REGISTERED.value
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        instance_ref: str,
        connector_type: str,
        display_name: str,
        category: str,
        direction: str,
        config: dict | None = None,
        secret_ref: str = "",
        plugin_id: str = "",
    ) -> ConnectorInstance:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            instance_ref=instance_ref,
            connector_type=connector_type,
            display_name=display_name,
            category=category,
            direction=direction,
            config=config or {},
            secret_ref=secret_ref,
            plugin_id=plugin_id,
        )

    def to_dict(self) -> dict:
        return {
            "instance_ref": self.instance_ref,
            "tenant_id": self.tenant_id,
            "connector_type": self.connector_type,
            "display_name": self.display_name,
            "category": self.category,
            "direction": self.direction,
            "config": self.config,
            "secret_ref": self.secret_ref,
            "plugin_id": self.plugin_id,
            "status": self.status,
        }


@dataclass(eq=False, kw_only=True)
class ConnectorHealthRecord(AggregateRoot):
    tenant_id: str
    health_ref: str
    instance_ref: str
    healthy: bool
    latency_ms: int = 0
    message: str = ""
    checked_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        health_ref: str,
        instance_ref: str,
        healthy: bool,
        latency_ms: int = 0,
        message: str = "",
    ) -> ConnectorHealthRecord:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            health_ref=health_ref,
            instance_ref=instance_ref,
            healthy=healthy,
            latency_ms=latency_ms,
            message=message,
        )

    def to_dict(self) -> dict:
        return {
            "health_ref": self.health_ref,
            "tenant_id": self.tenant_id,
            "instance_ref": self.instance_ref,
            "healthy": self.healthy,
            "latency_ms": self.latency_ms,
            "message": self.message,
            "checked_at": self.checked_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class OperationExecution(AggregateRoot):
    tenant_id: str
    execution_ref: str
    instance_ref: str
    connector_type: str
    operation: str
    status: str = ExecutionStatus.PENDING.value
    idempotency_key: str = ""
    correlation_id: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        execution_ref: str,
        instance_ref: str,
        connector_type: str,
        operation: str,
        idempotency_key: str = "",
        correlation_id: str = "",
    ) -> OperationExecution:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            execution_ref=execution_ref,
            instance_ref=instance_ref,
            connector_type=connector_type,
            operation=operation,
            idempotency_key=idempotency_key,
            correlation_id=correlation_id,
        )

    def to_dict(self) -> dict:
        return {
            "execution_ref": self.execution_ref,
            "tenant_id": self.tenant_id,
            "instance_ref": self.instance_ref,
            "connector_type": self.connector_type,
            "operation": self.operation,
            "status": self.status,
            "idempotency_key": self.idempotency_key,
            "correlation_id": self.correlation_id,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class PluginConnectorBinding(AggregateRoot):
    tenant_id: str
    binding_ref: str
    plugin_id: str
    instance_ref: str
    extension_point: str = "connector.execute"
    active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        binding_ref: str,
        plugin_id: str,
        instance_ref: str,
        extension_point: str = "connector.execute",
    ) -> PluginConnectorBinding:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            binding_ref=binding_ref,
            plugin_id=plugin_id,
            instance_ref=instance_ref,
            extension_point=extension_point,
        )

    def to_dict(self) -> dict:
        return {
            "binding_ref": self.binding_ref,
            "tenant_id": self.tenant_id,
            "plugin_id": self.plugin_id,
            "instance_ref": self.instance_ref,
            "extension_point": self.extension_point,
            "active": self.active,
        }
