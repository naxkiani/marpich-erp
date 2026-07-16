"""P3.1 — Physical vault location on Document Exchange."""
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


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "vault@dev.io", "password": "SecurePass123!", "display_name": "Vault Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "vault@dev.io", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    assert login.status_code == 200, login.text
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


async def _create_doc(client: AsyncClient, headers: dict[str, str]) -> str:
    root_id = (await client.get("/api/v1/documents/folders/root", headers=headers)).json()["data"]["id"]
    created = await client.post(
        "/api/v1/documents/documents",
        json={
            "folder_id": root_id,
            "title": "Paper Contract",
            "file_name": "contract.txt",
            "content": "Physical original stored in vault",
        },
        headers=headers,
    )
    assert created.status_code == 201, created.text
    return created.json()["data"]["document"]["id"]


@pytest.mark.asyncio
async def test_assign_and_get_physical_location(client):
    slug = "docs-p3-vault"
    await client.post(
        "/api/v1/platform/tenants",
        json={"name": "Vault Co", "slug": slug, "industry_pack": "university"},
    )
    headers = await _auth_headers(client, slug)
    document_id = await _create_doc(client, headers)

    assigned = await client.put(
        f"/api/v1/documents/documents/{document_id}/physical-location",
        json={
            "site_code": "HQ-VAULT",
            "room": "B2",
            "cabinet": "C-12",
            "shelf": "3",
            "box": "BX-09",
            "file_ref": "FOLDER-A/12",
        },
        headers=headers,
    )
    assert assigned.status_code == 200, assigned.text
    loc = assigned.json()["data"]["physical_location"]
    assert loc["site_code"] == "HQ-VAULT"
    assert loc["cabinet"] == "C-12"
    assert loc["file_ref"] == "FOLDER-A/12"

    got = await client.get(
        f"/api/v1/documents/documents/{document_id}/physical-location",
        headers=headers,
    )
    assert got.status_code == 200, got.text
    assert got.json()["data"]["physical_location"]["site_code"] == "HQ-VAULT"

    detail = await client.get(
        f"/api/v1/documents/documents/{document_id}",
        headers=headers,
    )
    assert detail.json()["data"]["document"]["physical_location"]["box"] == "BX-09"


@pytest.mark.asyncio
async def test_archived_document_rejects_physical_location(client):
    slug = "docs-p3-archived"
    await client.post(
        "/api/v1/platform/tenants",
        json={"name": "Archive Co", "slug": slug, "industry_pack": "clinic"},
    )
    headers = await _auth_headers(client, slug)
    document_id = await _create_doc(client, headers)

    archived = await client.post(
        f"/api/v1/documents/documents/{document_id}/archive",
        headers=headers,
    )
    assert archived.status_code == 200

    rejected = await client.put(
        f"/api/v1/documents/documents/{document_id}/physical-location",
        json={"site_code": "HQ-VAULT", "room": "A1"},
        headers=headers,
    )
    assert rejected.status_code == 400
    assert "archived" in rejected.json()["detail"]
