"""Enterprise Connector Framework engine."""
from __future__ import annotations

from pathlib import Path

import yaml

from contexts.enterprise_connector_framework.domain.aggregates.enterprise_connector_framework_platform import (
    ConnectorFrameworkCapability,
    ConnectorInstanceStatus,
    ExecutionStatus,
)

POLICY_KEYS = [
    "enterprise_connector_framework.health_check.enabled",
    "enterprise_connector_framework.retry.enabled",
    "enterprise_connector_framework.plugin_connectors.enabled",
    "enterprise_connector_framework.sdk_extensions.enabled",
]

CAPABILITY_LABELS = {
    ConnectorFrameworkCapability.CORE_BANKING_SYSTEMS.value: "Core Banking Systems",
    ConnectorFrameworkCapability.PAYMENT_GATEWAYS.value: "Payment Gateways",
    ConnectorFrameworkCapability.GOVERNMENT_SERVICES.value: "Government Services",
    ConnectorFrameworkCapability.TAX_AUTHORITIES.value: "Tax Authorities",
    ConnectorFrameworkCapability.CENTRAL_BANKS.value: "Central Banks",
    ConnectorFrameworkCapability.ERP_SYSTEMS.value: "ERP Systems",
    ConnectorFrameworkCapability.CRM_SYSTEMS.value: "CRM Systems",
    ConnectorFrameworkCapability.MOODLE.value: "Moodle",
    ConnectorFrameworkCapability.GOOGLE_CLASSROOM.value: "Google Classroom",
    ConnectorFrameworkCapability.MICROSOFT_365.value: "Microsoft 365",
    ConnectorFrameworkCapability.GOOGLE_WORKSPACE.value: "Google Workspace",
    ConnectorFrameworkCapability.LDAP.value: "LDAP",
    ConnectorFrameworkCapability.ACTIVE_DIRECTORY.value: "Active Directory",
    ConnectorFrameworkCapability.AZURE_AD.value: "Azure AD",
    ConnectorFrameworkCapability.EMAIL.value: "Email",
    ConnectorFrameworkCapability.SMS.value: "SMS",
    ConnectorFrameworkCapability.WHATSAPP_BUSINESS_API.value: "WhatsApp Business API",
    ConnectorFrameworkCapability.PUSH_NOTIFICATIONS.value: "Push Notifications",
    ConnectorFrameworkCapability.CLOUD_STORAGE.value: "Cloud Storage",
    ConnectorFrameworkCapability.DOCUMENT_MANAGEMENT_SYSTEMS.value: "Document Management Systems",
    ConnectorFrameworkCapability.PLUGIN_ARCHITECTURE.value: "Plug-in Architecture",
    ConnectorFrameworkCapability.CONNECTOR_SDK.value: "Connector SDK",
    ConnectorFrameworkCapability.CONNECTOR_MONITORING.value: "Connector Monitoring",
    ConnectorFrameworkCapability.CONNECTOR_MANAGEMENT_CONSOLE.value: "Connector Management Console",
}

CAPABILITY_TO_CONNECTOR_TYPE: dict[str, str] = {
    ConnectorFrameworkCapability.CORE_BANKING_SYSTEMS.value: "bank_api",
    ConnectorFrameworkCapability.PAYMENT_GATEWAYS.value: "payment_gateway",
    ConnectorFrameworkCapability.GOVERNMENT_SERVICES.value: "government_api",
    ConnectorFrameworkCapability.TAX_AUTHORITIES.value: "tax_api",
    ConnectorFrameworkCapability.CENTRAL_BANKS.value: "currency_api",
    ConnectorFrameworkCapability.ERP_SYSTEMS.value: "erp_connector",
    ConnectorFrameworkCapability.CRM_SYSTEMS.value: "crm_connector",
    ConnectorFrameworkCapability.MOODLE.value: "moodle",
    ConnectorFrameworkCapability.GOOGLE_CLASSROOM.value: "google_classroom",
    ConnectorFrameworkCapability.MICROSOFT_365.value: "microsoft_365",
    ConnectorFrameworkCapability.GOOGLE_WORKSPACE.value: "google_workspace",
    ConnectorFrameworkCapability.LDAP.value: "ldap",
    ConnectorFrameworkCapability.ACTIVE_DIRECTORY.value: "active_directory",
    ConnectorFrameworkCapability.AZURE_AD.value: "azure_ad",
    ConnectorFrameworkCapability.EMAIL.value: "email_provider",
    ConnectorFrameworkCapability.SMS.value: "sms_provider",
    ConnectorFrameworkCapability.WHATSAPP_BUSINESS_API.value: "whatsapp_provider",
    ConnectorFrameworkCapability.PUSH_NOTIFICATIONS.value: "push_provider",
    ConnectorFrameworkCapability.CLOUD_STORAGE.value: "cloud_storage",
    ConnectorFrameworkCapability.DOCUMENT_MANAGEMENT_SYSTEMS.value: "document_management",
}

_CATALOG_PATH = Path(__file__).resolve().parents[5] / "docs" / "architecture" / "integration" / "CONNECTOR_CATALOG.yaml"

_EMBEDDED_CATALOG: dict[str, dict] = {
    "azure_ad": {
        "display_name": "Azure AD",
        "category": "directory",
        "direction": "bidirectional",
        "auth": ["oauth2", "service_principal"],
        "operations": ["users_sync", "groups_sync", "sso_metadata"],
        "config_schema": "connectors/azure_ad.v1.json",
        "consumers": ["identity"],
    },
    "document_management": {
        "display_name": "Document Management System",
        "category": "document",
        "direction": "bidirectional",
        "auth": ["oauth2", "api_key", "service_account"],
        "operations": ["upload", "download", "metadata_sync", "version_history"],
        "config_schema": "connectors/document_management.v1.json",
        "consumers": ["documents"],
    },
}


def list_capability_catalog() -> list[dict]:
    return [
        {"capability": c.value, "label": CAPABILITY_LABELS.get(c.value, c.name.replace("_", " ").title())}
        for c in ConnectorFrameworkCapability
    ]


def list_policy_keys() -> list[str]:
    return list(POLICY_KEYS)


def dependency_map() -> dict:
    return {
        "nodes": [
            {"id": "enterprise_connector_framework", "type": "platform", "label": "Enterprise Connector Framework"},
            {"id": "connector_sdk", "type": "sdk", "label": "Connector SDK"},
            {"id": "plugins", "type": "platform", "label": "Plugin Platform"},
            {"id": "integration", "type": "context", "label": "Integration (legacy)"},
            {"id": "enterprise_event_bus", "type": "platform", "label": "Enterprise Event Bus"},
            {"id": "enterprise_api_gateway", "type": "platform", "label": "Enterprise API Gateway"},
        ],
        "edges": [
            {"from": "enterprise_connector_framework", "to": "connector_sdk", "type": "adapter_delegate"},
            {"from": "enterprise_connector_framework", "to": "plugins", "type": "plugin_binding"},
            {"from": "enterprise_connector_framework", "to": "integration", "type": "persistence_delegate"},
            {"from": "enterprise_connector_framework", "to": "enterprise_event_bus", "type": "event_publish"},
            {"from": "enterprise_api_gateway", "to": "enterprise_connector_framework", "type": "ingress_route"},
        ],
        "multi_tenant": True,
        "plugin_extensible": True,
    }


def load_connector_catalog() -> dict[str, dict]:
    catalog: dict[str, dict] = dict(_EMBEDDED_CATALOG)
    if _CATALOG_PATH.is_file():
        with _CATALOG_PATH.open(encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
        for connector_type, entry in (data.get("connectors") or {}).items():
            if connector_type not in catalog:
                catalog[connector_type] = entry
    return catalog


def catalog_entry_for_type(connector_type: str) -> dict | None:
    return load_connector_catalog().get(connector_type)


def default_seed_instances() -> list[dict]:
    catalog = load_connector_catalog()
    seeds = []
    for capability, connector_type in CAPABILITY_TO_CONNECTOR_TYPE.items():
        entry = catalog.get(connector_type, {})
        seeds.append({
            "connector_type": connector_type,
            "capability": capability,
            "display_name": entry.get("display_name", connector_type.replace("_", " ").title()),
            "category": entry.get("category", "custom"),
            "direction": entry.get("direction", "bidirectional"),
            "config": {"environment": "sandbox", "base_url": f"https://sandbox.{connector_type}.example"},
        })
    return seeds


def generate_seed_data() -> dict:
    return {
        "connector_instances": default_seed_instances(),
        "plugin_bindings": [
            {"plugin_id": "com.marpich.integration.custom-bank", "extension_point": "connector.execute"},
        ],
    }


def build_monitoring_dashboard(
    *,
    profile: dict | None,
    instances: list[dict],
    health_records: list[dict],
    executions: list[dict],
    plugin_bindings: list[dict],
    sdk_connectors: list[str],
) -> dict:
    by_status: dict[str, int] = {}
    for inst in instances:
        status = inst.get("status", ConnectorInstanceStatus.REGISTERED.value)
        by_status[status] = by_status.get(status, 0) + 1
    by_type: dict[str, int] = {}
    for inst in instances:
        ct = inst.get("connector_type", "unknown")
        by_type[ct] = by_type.get(ct, 0) + 1
    exec_by_status: dict[str, int] = {}
    for ex in executions:
        st = ex.get("status", ExecutionStatus.PENDING.value)
        exec_by_status[st] = exec_by_status.get(st, 0) + 1
    succeeded = exec_by_status.get(ExecutionStatus.SUCCEEDED.value, 0)
    total_exec = len(executions)
    success_rate = round((succeeded / total_exec) * 100, 2) if total_exec else 100.0
    healthy = sum(1 for h in health_records if h.get("healthy"))
    return {
        "summary": {
            "capabilities": len(ConnectorFrameworkCapability),
            "connector_instances": len(instances),
            "active_instances": by_status.get(ConnectorInstanceStatus.ACTIVE.value, 0),
            "plugin_bindings": len(plugin_bindings),
            "sdk_registered_types": len(sdk_connectors),
            "executions_total": total_exec,
            "executions_succeeded": succeeded,
            "success_rate_pct": success_rate,
            "health_checks": len(health_records),
            "healthy_connectors": healthy,
            "health_check_enabled": profile.get("health_check_enabled", True) if profile else True,
            "plugin_connectors_enabled": profile.get("plugin_connectors_enabled", True) if profile else True,
        },
        "profile": profile,
        "instances_by_status": by_status,
        "instances_by_type": by_type,
        "executions_by_status": exec_by_status,
        "recent_executions": executions[:20],
        "instance_health": health_records[:20],
        "plugin_bindings": plugin_bindings[:20],
    }
