"""Register built-in connector adapters."""
from __future__ import annotations

from shared.connectors.adapters.google_classroom_adapter import GoogleClassroomAdapter
from shared.connectors.adapters.livekit_adapter import LiveKitAdapter
from shared.connectors.adapters.moodle_adapter import MoodleAdapter
from shared.connectors.registry import register_adapter_instance
from shared.connectors.stub_adapter import BaseConnectorAdapter

_BUILTIN: list[tuple[str, list[str]]] = [
    ("bank_api", ["transfer", "statement_import", "balance_inquiry", "test_connection"]),
    ("payment_gateway", ["charge", "refund", "capture", "webhook_verify", "test_connection"]),
    ("government_api", ["verify_id", "submit_filing", "status_poll", "test_connection"]),
    ("tax_api", ["validate_vat", "file_return", "fetch_assessment", "test_connection"]),
    ("currency_api", ["fetch_rates", "historical_rates", "test_connection"]),
    ("erp_connector", ["items_sync", "orders_sync", "invoices_sync", "inventory_push", "test_connection"]),
    ("crm_connector", ["contacts_sync", "deals_sync", "activities_push", "test_connection"]),
    ("microsoft_365", ["users_sync", "calendar_sync", "sharepoint_files", "test_connection"]),
    ("google_workspace", ["users_sync", "drive_sync", "calendar_sync", "test_connection"]),
    ("ldap", ["users_sync", "groups_sync", "test_bind", "test_connection"]),
    ("active_directory", ["users_sync", "groups_sync", "password_reset_hook", "test_connection"]),
    ("azure_ad", ["users_sync", "groups_sync", "sso_metadata", "test_connection"]),
    ("email_provider", ["send_email", "bounce_webhook", "test_connection"]),
    ("sms_provider", ["send_sms", "delivery_status", "test_connection"]),
    ("whatsapp_provider", ["send_message", "delivery_status", "test_connection"]),
    ("push_provider", ["send_push", "register_device", "test_connection"]),
    ("cloud_storage", ["upload", "download", "list", "delete", "sync_folder", "test_connection"]),
    ("document_management", ["upload", "download", "metadata_sync", "version_history", "test_connection"]),
    ("custom", ["invoke", "test_connection"]),
]


def register_builtin_connectors() -> None:
    for connector_type, operations in _BUILTIN:
        register_adapter_instance(connector_type, BaseConnectorAdapter(connector_type, operations))
    register_adapter_instance("moodle", MoodleAdapter())
    register_adapter_instance("google_classroom", GoogleClassroomAdapter())
    register_adapter_instance("livekit", LiveKitAdapter())
