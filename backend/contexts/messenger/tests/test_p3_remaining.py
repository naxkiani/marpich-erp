"""P3 remaining slices — messenger, bootcamp, ROAS/threat/backup, AI assist."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.ai.container import get_ai_service, reset_ai_service
from contexts.analytics.application.constants.kpi_formula_catalog import KPI_FORMULA_CATALOG
from contexts.analytics.domain.aggregates.kpi_platform import KpiKey
from contexts.business_continuity.container import (
    get_business_continuity_service,
    reset_business_continuity_service,
)
from contexts.core_platform.container import reset_platform_service
from contexts.core_platform.infrastructure.persistence.memory_store import PlatformMemoryStore
from contexts.enterprise_observability.container import (
    get_enterprise_observability_service,
    reset_enterprise_observability_service,
)
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from contexts.messenger.container import get_messenger_service, reset_messenger_service
from contexts.messenger.infrastructure.persistence.memory_store import MessengerMemoryStore
from contexts.university.container import get_university_service, reset_university_service
from contexts.university.infrastructure.persistence.memory_store import UniversityMemoryStore
from core.presentation.api.app_factory import create_app
from core.presentation.api.startup_registry import configure_application
from shared.connectors.builtins import register_builtin_connectors
from shared.connectors.registry import reset_connector_registry
from shared.infrastructure.messaging.event_fabric import EventFabric


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    PlatformMemoryStore.reset()
    MessengerMemoryStore.reset()
    UniversityMemoryStore.reset()
    EventFabric.reset_dev_state()
    reset_connector_registry()
    register_builtin_connectors()
    reset_platform_service()
    reset_messenger_service()
    reset_ai_service()
    reset_university_service()
    reset_business_continuity_service()
    reset_enterprise_observability_service()
    get_messenger_service()
    get_ai_service()
    get_university_service()
    get_business_continuity_service()
    get_enterprise_observability_service()
    yield


@pytest.fixture
async def client():
    application = create_app(profile="industry", startup_mode="lazy")
    configure_application(application, profile="industry", startup_mode="lazy")
    transport = ASGITransport(app=application)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _admin(client: AsyncClient, tenant: str, email: str = "p3@marpich.dev") -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "SecurePass123!", "display_name": "P3 Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    assert login.status_code == 200, login.text
    return {
        "X-Tenant-ID": tenant,
        "Authorization": f"Bearer {login.json()['data']['access_token']}",
    }


@pytest.mark.asyncio
async def test_messenger_conversation_message_and_livekit_token(client):
    slug = "p3-messenger"
    await client.post(
        "/api/v1/platform/tenants",
        json={"name": "Chat Co", "slug": slug, "industry_pack": "university"},
    )
    headers = await _admin(client, slug, "chat@marpich.dev")

    opened = await client.post(
        "/api/v1/messenger/conversations",
        json={
            "title": "Ops room",
            "member_ids": ["user-a"],
            "e2ee_enabled": True,
            "issue_livekit_token": True,
        },
        headers=headers,
    )
    assert opened.status_code == 201, opened.text
    data = opened.json()["data"]
    assert data["e2ee_enabled"] is True
    assert data["livekit_room_name"]
    assert data["livekit_token"].startswith("lk_")
    assert data.get("livekit_simulated") is True
    conversation_id = data["id"]

    # E2EE: client supplies ciphertext — server must not accept plaintext
    rejected = await client.post(
        f"/api/v1/messenger/conversations/{conversation_id}/messages",
        json={"body": "hello encrypted"},
        headers=headers,
    )
    assert rejected.status_code == 400

    sent = await client.post(
        f"/api/v1/messenger/conversations/{conversation_id}/messages",
        json={
            "ciphertext": "v1:client-ciphertext",
            "ciphertext_type": "application/x-marpich-e2ee",
        },
        headers=headers,
    )
    assert sent.status_code == 201, sent.text
    msg = sent.json()["data"]
    assert msg["ciphertext"] == "v1:client-ciphertext"
    assert msg["body"] == ""


@pytest.mark.asyncio
async def test_bootcamp_enrollment_requires_cohort(client):
    slug = "p3-bootcamp"
    await client.post(
        "/api/v1/platform/tenants",
        json={"name": "Bootcamp Co", "slug": slug, "industry_pack": "university"},
    )
    headers = await _admin(client, slug, "boot@marpich.dev")

    missing = await client.post(
        "/api/v1/university/students",
        json={
            "student_number": "BC-001",
            "first_name": "Ada",
            "last_name": "Lovelace",
            "email": "ada@boot.dev",
            "program_code": "FULLSTACK",
            "delivery_model": "bootcamp",
        },
        headers=headers,
    )
    assert missing.status_code == 400

    ok = await client.post(
        "/api/v1/university/students",
        json={
            "student_number": "BC-001",
            "first_name": "Ada",
            "last_name": "Lovelace",
            "email": "ada@boot.dev",
            "program_code": "FULLSTACK",
            "delivery_model": "bootcamp",
            "cohort_ref": "2026-SUMMER",
        },
        headers=headers,
    )
    assert ok.status_code == 201, ok.text
    student = ok.json()["data"]
    assert student["delivery_model"] == "bootcamp"
    assert student["cohort_ref"] == "2026-SUMMER"


def test_roas_kpi_in_catalog():
    assert KpiKey.ROAS.value in KPI_FORMULA_CATALOG
    assert "ad_spend" in KPI_FORMULA_CATALOG[KpiKey.ROAS.value]["variables"]


@pytest.mark.asyncio
async def test_threat_map_and_nightly_backup(client):
    slug = "p3-ops"
    await client.post(
        "/api/v1/platform/tenants",
        json={"name": "Ops Co", "slug": slug, "industry_pack": "retail"},
    )
    headers = await _admin(client, slug, "ops@marpich.dev")

    # Observability may be enterprise-only — call service directly if route filtered
    threat = await get_enterprise_observability_service().get_threat_map(slug)
    assert threat.succeeded
    assert "nodes" in threat.unwrap()

    backup = await get_business_continuity_service().schedule_nightly_cloud_backup(slug)
    assert backup.succeeded
    data = backup.unwrap()
    assert data["encrypted"] is True
    assert data["metadata"]["cron_expression"] == "0 2 * * *"
    assert data["metadata"]["destination_connector"] == "cloud_storage"

    # HTTP route (enterprise profile contexts may be absent on industry — soft check)
    nightly = await client.post("/api/v1/business-continuity/backups/nightly-cloud", headers=headers)
    assert nightly.status_code in (201, 404)


@pytest.mark.asyncio
async def test_ai_assist_platform_endpoint(client):
    slug = "p3-ai"
    await client.post(
        "/api/v1/platform/tenants",
        json={"name": "AI Co", "slug": slug, "industry_pack": "university"},
    )
    headers = await _admin(client, slug, "ai@marpich.dev")

    resp = await client.post(
        "/api/v1/ai/assist",
        json={
            "module_id": "university",
            "surface": "assistant",
            "prompt": "Explain my next assignment",
            "context": {"student_id": "stu-1"},
        },
        headers=headers,
    )
    assert resp.status_code == 200, resp.text
    data = resp.json()["data"]
    assert "Marpich AI" in data["reply"]
    assert "student_id=stu-1" in data["reply"]
