"""Media — upload, transcode, variant tests."""
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
from contexts.integration.infrastructure.persistence.memory_store import IntegrationMemoryStore
from contexts.media.container import get_media_service, reset_media_service
from contexts.media.infrastructure.persistence.memory_store import MediaMemoryStore
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
    MediaMemoryStore.reset()
    InProcessEventBus.reset()
    reset_platform_service()
    reset_organization_service()
    reset_settings_service()
    reset_notification_service()
    reset_audit_service()
    reset_documents_service()
    reset_workflow_service()
    reset_integration_service()
    reset_media_service()
    get_media_service()
    get_documents_service()
    get_organization_service()
    get_settings_service()
    get_notification_service()
    get_audit_service()
    get_workflow_service()
    get_integration_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "admin@media.dev", "password": "SecurePass123!", "display_name": "Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "admin@media.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_register_complete_and_get_asset(client):
    slug = "media-upload"
    headers = await _auth_headers(client, slug)

    registered = await client.post(
        "/api/v1/media/assets",
        json={"file_name": "photo.jpg", "content_type": "image/jpeg"},
        headers=headers,
    )
    assert registered.status_code == 201
    asset_id = registered.json()["data"]["asset"]["id"]
    assert "presigned_url" in registered.json()["data"]

    completed = await client.post(
        f"/api/v1/media/assets/{asset_id}/complete",
        json={"checksum": "abc123"},
        headers=headers,
    )
    assert completed.status_code == 200
    assert completed.json()["data"]["status"] == "ready"

    detail = await client.get(f"/api/v1/media/assets/{asset_id}", headers=headers)
    assert detail.status_code == 200
    assert len(detail.json()["data"]["variants"]) == 1


@pytest.mark.asyncio
async def test_transcode_creates_variant(client):
    slug = "media-transcode"
    headers = await _auth_headers(client, slug)

    registered = await client.post(
        "/api/v1/media/assets",
        json={"file_name": "banner.png", "content_type": "image/png"},
        headers=headers,
    )
    asset_id = registered.json()["data"]["asset"]["id"]
    await client.post(f"/api/v1/media/assets/{asset_id}/complete", json={}, headers=headers)

    transcode = await client.post(
        f"/api/v1/media/assets/{asset_id}/transcode",
        json={"profile": "thumbnail"},
        headers=headers,
    )
    assert transcode.status_code == 202
    assert transcode.json()["data"]["variant"]["profile"] == "thumbnail"

    variant = await client.get(
        f"/api/v1/media/assets/{asset_id}/variants/thumbnail",
        headers=headers,
    )
    assert variant.status_code == 200
    assert "cdn.marpich.dev" in variant.json()["data"]["url"]


@pytest.mark.asyncio
async def test_document_upload_extracts_media_asset(client):
    slug = "media-doc"
    await client.post(
        "/api/v1/platform/tenants",
        json={"name": "Media Docs", "slug": slug, "industry_pack": "hospital"},
    )
    headers = await _auth_headers(client, slug)

    root_id = (await client.get("/api/v1/documents/folders/root", headers=headers)).json()["data"]["id"]
    await client.post(
        "/api/v1/documents/documents",
        json={
            "folder_id": root_id,
            "title": "Scan",
            "file_name": "scan.jpg",
            "content": "binary-placeholder",
            "content_type": "image/jpeg",
        },
        headers=headers,
    )

    entries = await client.get(
        "/api/v1/audit/entries",
        params={"event_name": "media.asset.uploaded"},
        headers=headers,
    )
    assert entries.status_code == 200
    assert len(entries.json()["data"]["items"]) >= 1


@pytest.mark.asyncio
async def test_soft_delete_asset(client):
    slug = "media-delete"
    headers = await _auth_headers(client, slug)

    registered = await client.post(
        "/api/v1/media/assets",
        json={"file_name": "old.mp4", "content_type": "video/mp4"},
        headers=headers,
    )
    asset_id = registered.json()["data"]["asset"]["id"]
    await client.post(f"/api/v1/media/assets/{asset_id}/complete", json={}, headers=headers)

    deleted = await client.delete(f"/api/v1/media/assets/{asset_id}", headers=headers)
    assert deleted.status_code == 200
    assert deleted.json()["data"]["status"] == "deleted"

    detail = await client.get(f"/api/v1/media/assets/{asset_id}", headers=headers)
    assert detail.status_code == 404
