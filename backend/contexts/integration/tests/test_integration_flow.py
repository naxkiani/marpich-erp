"""Integration — webhooks, connectors, sync tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.audit.container import get_audit_service, reset_audit_service
from contexts.audit.infrastructure.persistence.memory_store import AuditMemoryStore
from contexts.core_platform.container import reset_platform_service
from contexts.core_platform.infrastructure.persistence.memory_store import PlatformMemoryStore
from contexts.documents.container import get_documents_service, reset_documents_service
from contexts.documents.infrastructure.persistence.memory_store import DocumentsMemoryStore
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from contexts.integration.container import get_integration_service, reset_integration_service
from contexts.integration.infrastructure.channels.console_webhook import ConsoleWebhookChannel
from contexts.integration.infrastructure.persistence.memory_store import IntegrationMemoryStore
from contexts.notifications.container import get_notification_service, reset_notification_service
from contexts.notifications.infrastructure.persistence.memory_store import NotificationMemoryStore
from contexts.organization.container import get_organization_service, reset_organization_service
from contexts.organization.infrastructure.persistence.memory_store import OrganizationMemoryStore
from contexts.settings.container import get_settings_service, reset_settings_service
from contexts.settings.infrastructure.persistence.memory_store import SettingsMemoryStore
from contexts.workflow.container import get_workflow_service, reset_workflow_service
from contexts.workflow.infrastructure.persistence.memory_store import WorkflowMemoryStore
from core.presentation.api.main import app
from shared.infrastructure.messaging.event_bus import InProcessEventBus


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    PlatformMemoryStore.reset()
    OrganizationMemoryStore.reset()
    SettingsMemoryStore.reset()
    NotificationMemoryStore.reset()
    AuditMemoryStore.reset()
    DocumentsMemoryStore.reset()
    WorkflowMemoryStore.reset()
    IntegrationMemoryStore.reset()
    ConsoleWebhookChannel.reset()
    InProcessEventBus.reset()
    reset_platform_service()
    reset_organization_service()
    reset_settings_service()
    reset_notification_service()
    reset_audit_service()
    reset_documents_service()
    reset_workflow_service()
    reset_integration_service()
    get_integration_service()
    get_organization_service()
    get_settings_service()
    get_notification_service()
    get_audit_service()
    get_documents_service()
    get_workflow_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "admin@int.dev", "password": "SecurePass123!", "display_name": "Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "admin@int.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_tenant_provision_creates_connector_slots(client):
    slug = "int-provision"
    provision = await client.post(
        "/api/v1/platform/tenants",
        json={"name": "Integration Co", "slug": slug, "industry_pack": "hospital"},
    )
    assert provision.status_code == 201

    headers = await _auth_headers(client, slug)
    connectors = await client.get("/api/v1/integrations/connectors", headers=headers)
    assert connectors.status_code == 200
    types = {c["connector_type"] for c in connectors.json()["data"]}
    assert "crm" in types
    assert "erp" in types


@pytest.mark.asyncio
async def test_register_connector_and_webhook(client):
    slug = "int-webhook"
    headers = await _auth_headers(client, slug)

    connector = await client.post(
        "/api/v1/integrations/connectors",
        json={"connector_type": "custom", "name": "Partner API", "config": {"base_url": "https://api.example.com"}},
        headers=headers,
    )
    assert connector.status_code == 201

    webhook = await client.post(
        "/api/v1/integrations/webhooks",
        json={
            "target_url": "https://hooks.example.com/events",
            "event_pattern": "identity.user.created",
            "description": "User sync",
        },
        headers=headers,
    )
    assert webhook.status_code == 201
    webhook_id = webhook.json()["data"]["id"]

    tested = await client.post(f"/api/v1/integrations/webhooks/{webhook_id}/test", headers=headers)
    assert tested.status_code == 200
    assert tested.json()["data"]["status"] == "delivered"


@pytest.mark.asyncio
async def test_event_triggers_webhook_delivery(client):
    slug = "int-event"
    headers = await _auth_headers(client, slug)

    await client.post(
        "/api/v1/integrations/webhooks",
        json={
            "target_url": "https://hooks.example.com/user-created",
            "event_pattern": "identity.user.created",
        },
        headers=headers,
    )

    await client.post(
        "/api/v1/auth/register",
        json={"email": "newuser@int.dev", "password": "SecurePass123!", "display_name": "New"},
        headers={"X-Tenant-ID": slug},
    )

    logs = await client.get("/api/v1/integrations/logs", headers=headers)
    assert logs.status_code == 200
    delivered = [log for log in logs.json()["data"] if log["status"] == "delivered"]
    assert len(delivered) >= 1
    assert len(ConsoleWebhookChannel.deliveries) >= 1


@pytest.mark.asyncio
async def test_sync_job(client):
    slug = "int-sync"
    headers = await _auth_headers(client, slug)

    connector = await client.post(
        "/api/v1/integrations/connectors",
        json={"connector_type": "crm", "name": "Salesforce", "config": {"instance": "demo"}},
        headers=headers,
    )
    connector_id = connector.json()["data"]["id"]

    sync = await client.post(
        "/api/v1/integrations/sync-jobs",
        json={"connector_id": connector_id, "job_type": "contacts_sync"},
        headers=headers,
    )
    assert sync.status_code == 202
    assert sync.json()["data"]["status"] == "completed"


@pytest.mark.asyncio
async def test_webhook_failure_logged(client):
    slug = "int-fail"
    headers = await _auth_headers(client, slug)

    webhook = await client.post(
        "/api/v1/integrations/webhooks",
        json={"target_url": "fail://simulated", "event_pattern": "identity.user.created"},
        headers=headers,
    )
    webhook_id = webhook.json()["data"]["id"]

    failed = await client.post(f"/api/v1/integrations/webhooks/{webhook_id}/test", headers=headers)
    assert failed.status_code == 400

    logs = await client.get("/api/v1/integrations/logs", headers=headers)
    failed_logs = [log for log in logs.json()["data"] if log["status"] == "failed"]
    assert len(failed_logs) >= 1
