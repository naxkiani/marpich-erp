"""P4 Document Studio — HTML content_type accepted by Document Exchange."""
from __future__ import annotations

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
from contexts.notifications.container import get_notification_service, reset_notification_service
from contexts.notifications.infrastructure.persistence.memory_store import NotificationMemoryStore
from contexts.organization.container import get_organization_service, reset_organization_service
from contexts.organization.infrastructure.persistence.memory_store import OrganizationMemoryStore
from contexts.settings.container import get_settings_service, reset_settings_service
from contexts.settings.infrastructure.persistence.memory_store import SettingsMemoryStore
from core.presentation.api.app_factory import create_app
from core.presentation.api.startup_registry import configure_application
from shared.infrastructure.messaging.event_fabric import EventFabric


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
    EventFabric.reset_dev_state()
    reset_platform_service()
    reset_organization_service()
    reset_settings_service()
    reset_notification_service()
    reset_audit_service()
    reset_documents_service()
    get_documents_service()
    get_organization_service()
    get_settings_service()
    get_notification_service()
    get_audit_service()
    yield


@pytest.fixture
async def client():
    application = create_app(profile="core", startup_mode="lazy")
    configure_application(application, profile="core", startup_mode="lazy")
    transport = ASGITransport(app=application)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "studio@dev.io", "password": "SecurePass123!", "display_name": "Studio"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "studio@dev.io", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    assert login.status_code == 200, login.text
    return {
        "X-Tenant-ID": tenant,
        "Authorization": f"Bearer {login.json()['data']['access_token']}",
    }


@pytest.mark.asyncio
async def test_html_document_version_roundtrip(client):
    slug = "docs-p4-html"
    await client.post(
        "/api/v1/platform/tenants",
        json={"name": "Studio Co", "slug": slug, "industry_pack": "university"},
    )
    headers = await _auth(client, slug)
    root_id = (await client.get("/api/v1/documents/folders/root", headers=headers)).json()["data"]["id"]

    created = await client.post(
        "/api/v1/documents/documents",
        json={
            "folder_id": root_id,
            "title": "Rich Letter",
            "file_name": "letter.html",
            "content_type": "text/html",
            "content": "<p>Hello <strong>Marpich</strong></p>",
        },
        headers=headers,
    )
    assert created.status_code == 201, created.text
    document_id = created.json()["data"]["document"]["id"]

    preview = await client.get(
        f"/api/v1/documents/documents/{document_id}/preview",
        headers=headers,
    )
    assert preview.status_code == 200, preview.text
    assert "<strong>Marpich</strong>" in preview.json()["data"]["content"]
    assert preview.json()["data"]["content_type"] == "text/html"
