"""P1 Document Exchange — QR verify, RSA-PSS sign evidence, watermarked preview."""
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
        json={"email": "docs-p1@dev.io", "password": "SecurePass123!", "display_name": "Docs Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "docs-p1@dev.io", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    assert login.status_code == 200, login.text
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_sign_hmac_evidence_and_public_qr_verify(client):
    """Legacy name — content seal is RSA-PSS-SHA256 (P5.1)."""
    slug = "docs-p1-verify"
    await client.post(
        "/api/v1/platform/tenants",
        json={"name": "Verify Co", "slug": slug, "industry_pack": "university"},
    )
    headers = await _auth_headers(client, slug)
    root_id = (await client.get("/api/v1/documents/folders/root", headers=headers)).json()["data"]["id"]

    created = await client.post(
        "/api/v1/documents/documents",
        json={
            "folder_id": root_id,
            "title": "Certificate",
            "file_name": "cert.txt",
            "content": "Official certificate body",
        },
        headers=headers,
    )
    assert created.status_code == 201, created.text
    document_id = created.json()["data"]["document"]["id"]
    qr_token = created.json()["data"]["document"]["qr_token"]
    assert qr_token

    signed = await client.post(
        f"/api/v1/documents/documents/{document_id}/sign",
        json={"signers": ["registrar@uni.dev"]},
        headers=headers,
    )
    assert signed.status_code == 201, signed.text
    body = signed.json()["data"]
    assert body["algorithm"] == "RSA-PSS-SHA256"
    assert body["signature_hash"]
    assert body["content_checksum"]
    qr_token = body["qr_token"] or qr_token

    public = await client.get(f"/api/v1/documents/verify/{qr_token}")
    assert public.status_code == 200, public.text
    data = public.json()["data"]
    assert data["valid"] is True
    assert data["document_id"] == document_id
    assert data["checksum_matches"] is True
    assert data["signature_valid"] is True
    assert data["signature"]["algorithm"] == "RSA-PSS-SHA256"

    # Tampered token must fail
    bad = await client.get(f"/api/v1/documents/verify/{qr_token}xx")
    assert bad.status_code == 404


@pytest.mark.asyncio
async def test_preview_applies_serve_time_watermark(client):
    slug = "docs-p1-wm"
    await client.post(
        "/api/v1/platform/tenants",
        json={"name": "Watermark Co", "slug": slug, "industry_pack": "clinic"},
    )
    headers = await _auth_headers(client, slug)
    root_id = (await client.get("/api/v1/documents/folders/root", headers=headers)).json()["data"]["id"]
    created = await client.post(
        "/api/v1/documents/documents",
        json={
            "folder_id": root_id,
            "title": "Sensitive Note",
            "file_name": "note.txt",
            "content": "Confidential content",
        },
        headers=headers,
    )
    document_id = created.json()["data"]["document"]["id"]

    preview = await client.get(
        f"/api/v1/documents/documents/{document_id}/preview",
        headers=headers,
    )
    assert preview.status_code == 200, preview.text
    data = preview.json()["data"]
    assert data["content"] == "Confidential content"
    assert data["stored_mutated"] is False
    assert data["watermark"] is not None
    assert "data.watermark" in data["obligations"]
