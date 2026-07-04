"""Documents — DMS flow tests."""
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
    InProcessEventBus.reset()
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
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "admin@docs.dev", "password": "SecurePass123!", "display_name": "Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "admin@docs.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_tenant_provision_creates_root_folder(client):
    slug = "docs-hospital"
    provision = await client.post(
        "/api/v1/platform/tenants",
        json={"name": "Docs Hospital", "slug": slug, "industry_pack": "hospital"},
    )
    assert provision.status_code == 201

    headers = await _auth_headers(client, slug)

    root = await client.get("/api/v1/documents/folders/root", headers=headers)
    assert root.status_code == 200
    assert root.json()["data"]["is_root"] is True


@pytest.mark.asyncio
async def test_create_folder_and_document(client):
    slug = "docs-create"
    await client.post(
        "/api/v1/platform/tenants",
        json={"name": "Docs Co", "slug": slug, "industry_pack": "clinic"},
    )
    headers = await _auth_headers(client, slug)

    root = await client.get("/api/v1/documents/folders/root", headers=headers)
    root_id = root.json()["data"]["id"]

    folder = await client.post(
        "/api/v1/documents/folders",
        json={"parent_id": root_id, "name": "Contracts"},
        headers=headers,
    )
    assert folder.status_code == 201
    folder_id = folder.json()["data"]["id"]

    doc = await client.post(
        "/api/v1/documents/documents",
        json={
            "folder_id": folder_id,
            "title": "Service Agreement",
            "file_name": "agreement.txt",
            "content": "Terms and conditions v1",
        },
        headers=headers,
    )
    assert doc.status_code == 201
    document_id = doc.json()["data"]["document"]["id"]

    contents = await client.get(f"/api/v1/documents/folders/{folder_id}/contents", headers=headers)
    assert contents.status_code == 200
    assert len(contents.json()["data"]["documents"]) == 1

    detail = await client.get(f"/api/v1/documents/documents/{document_id}", headers=headers)
    assert detail.status_code == 200
    assert len(detail.json()["data"]["versions"]) == 1


@pytest.mark.asyncio
async def test_add_version_and_download(client):
    slug = "docs-version"
    await client.post(
        "/api/v1/platform/tenants",
        json={"name": "Version Co", "slug": slug, "industry_pack": "school"},
    )
    headers = await _auth_headers(client, slug)

    root_id = (await client.get("/api/v1/documents/folders/root", headers=headers)).json()["data"]["id"]
    doc = await client.post(
        "/api/v1/documents/documents",
        json={
            "folder_id": root_id,
            "title": "Policy",
            "file_name": "policy.txt",
            "content": "Version 1 content",
        },
        headers=headers,
    )
    document_id = doc.json()["data"]["document"]["id"]

    v2 = await client.post(
        f"/api/v1/documents/documents/{document_id}/versions",
        json={"file_name": "policy-v2.txt", "content": "Version 2 content"},
        headers=headers,
    )
    assert v2.status_code == 201
    assert v2.json()["data"]["version_number"] == 2

    download = await client.get(f"/api/v1/documents/documents/{document_id}/download", headers=headers)
    assert download.status_code == 200
    assert download.json()["data"]["content"] == "Version 2 content"


@pytest.mark.asyncio
async def test_sign_and_archive_document(client):
    slug = "docs-sign"
    await client.post(
        "/api/v1/platform/tenants",
        json={"name": "Sign Co", "slug": slug, "industry_pack": "retail"},
    )
    headers = await _auth_headers(client, slug)

    root_id = (await client.get("/api/v1/documents/folders/root", headers=headers)).json()["data"]["id"]
    doc = await client.post(
        "/api/v1/documents/documents",
        json={
            "folder_id": root_id,
            "title": "NDA",
            "file_name": "nda.txt",
            "content": "Confidential",
        },
        headers=headers,
    )
    document_id = doc.json()["data"]["document"]["id"]

    signed = await client.post(
        f"/api/v1/documents/documents/{document_id}/sign",
        json={"signers": ["legal@sign.co", "ceo@sign.co"]},
        headers=headers,
    )
    assert signed.status_code == 201
    assert signed.json()["data"]["status"] == "signed"

    archived = await client.post(
        f"/api/v1/documents/documents/{document_id}/archive",
        headers=headers,
    )
    assert archived.status_code == 200
    assert archived.json()["data"]["status"] == "archived"


@pytest.mark.asyncio
async def test_document_events_in_audit_log(client):
    slug = "docs-audit"
    await client.post(
        "/api/v1/platform/tenants",
        json={"name": "Audit Docs", "slug": slug, "industry_pack": "hospital"},
    )
    headers = await _auth_headers(client, slug)

    root_id = (await client.get("/api/v1/documents/folders/root", headers=headers)).json()["data"]["id"]
    await client.post(
        "/api/v1/documents/documents",
        json={
            "folder_id": root_id,
            "title": "Chart",
            "file_name": "chart.txt",
            "content": "Patient record",
        },
        headers=headers,
    )

    entries = await client.get(
        "/api/v1/audit/entries",
        params={"event_name": "documents.document.uploaded"},
        headers=headers,
    )
    assert entries.status_code == 200
    assert len(entries.json()["data"]["items"]) >= 1
