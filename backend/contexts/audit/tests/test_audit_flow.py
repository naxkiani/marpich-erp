"""Audit — event fan-out and compliance export tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.audit.container import get_audit_service, reset_audit_service
from contexts.audit.infrastructure.persistence.memory_store import AuditMemoryStore
from contexts.core_platform.container import reset_platform_service
from contexts.core_platform.infrastructure.persistence.memory_store import PlatformMemoryStore
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from contexts.notifications.container import get_notification_service, reset_notification_service
from contexts.notifications.infrastructure.persistence.memory_store import NotificationMemoryStore
from contexts.organization.container import get_organization_service, reset_organization_service
from contexts.organization.infrastructure.persistence.memory_store import OrganizationMemoryStore
from contexts.settings.container import get_settings_service, reset_settings_service
from contexts.settings.infrastructure.persistence.memory_store import SettingsMemoryStore
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
    InProcessEventBus.reset()
    reset_platform_service()
    reset_organization_service()
    reset_settings_service()
    reset_notification_service()
    reset_audit_service()
    get_audit_service()
    get_organization_service()
    get_settings_service()
    get_notification_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "admin@audit.dev", "password": "SecurePass123!", "display_name": "Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "admin@audit.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_tenant_provision_creates_audit_entries(client):
    slug = "audit-provision"
    provision = await client.post(
        "/api/v1/platform/tenants",
        json={"name": "Audit Hospital", "slug": slug, "industry_pack": "hospital"},
    )
    assert provision.status_code == 201

    headers = await _auth_headers(client, slug)

    entries = await client.get("/api/v1/audit/entries", headers=headers)
    assert entries.status_code == 200
    data = entries.json()["data"]
    assert data["total"] >= 1
    event_names = {e["event_name"] for e in data["items"]}
    assert "platform.tenant.provisioned" in event_names


@pytest.mark.asyncio
async def test_user_register_logs_identity_event(client):
    slug = "audit-identity"
    headers = await _auth_headers(client, slug)

    entries = await client.get(
        "/api/v1/audit/entries",
        params={"event_name": "identity.user.created"},
        headers=headers,
    )
    assert entries.status_code == 200
    items = entries.json()["data"]["items"]
    assert len(items) >= 1
    assert items[0]["resource_type"] == "user"


@pytest.mark.asyncio
async def test_login_creates_security_audit_entry(client):
    slug = "audit-login"
    headers = await _auth_headers(client, slug)

    entries = await client.get(
        "/api/v1/audit/entries",
        params={"severity": "security"},
        headers=headers,
    )
    assert entries.status_code == 200
    items = entries.json()["data"]["items"]
    assert any(e["event_name"] == "identity.user.logged_in" for e in items)


@pytest.mark.asyncio
async def test_direct_record_and_stats(client):
    slug = "audit-direct"
    headers = await _auth_headers(client, slug)

    recorded = await client.post(
        "/api/v1/audit/entries",
        json={
            "action": "manual.review",
            "resource_type": "document",
            "resource_id": "doc-99",
            "severity": "compliance",
        },
        headers=headers,
    )
    assert recorded.status_code == 201

    stats = await client.get("/api/v1/audit/stats", headers=headers)
    assert stats.status_code == 200
    assert stats.json()["data"]["total_entries"] >= 1


@pytest.mark.asyncio
async def test_compliance_export(client):
    slug = "audit-export"
    headers = await _auth_headers(client, slug)

    export = await client.post(
        "/api/v1/audit/exports",
        json={"format": "json"},
        headers=headers,
    )
    assert export.status_code == 202
    export_id = export.json()["data"]["id"]

    fetched = await client.get(f"/api/v1/audit/exports/{export_id}", headers=headers)
    assert fetched.status_code == 200
    data = fetched.json()["data"]
    assert data["status"] == "completed"
    assert data["entry_count"] >= 1
    assert len(data["data"]) >= 1
