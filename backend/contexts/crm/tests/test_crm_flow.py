"""CRM contact + opportunity flow tests — CAP-ENT-001."""
import uuid

import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.crm.container import reset_crm_service
from contexts.crm.infrastructure.persistence.memory_store import CrmMemoryStore
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from core.presentation.api.app_factory import create_app
from core.presentation.api.startup_registry import configure_application
from shared.infrastructure.messaging.event_bus import InProcessEventBus
from shared.infrastructure.messaging.event_fabric import EventFabric


@pytest.fixture(autouse=True)
async def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    CrmMemoryStore.reset()
    InProcessEventBus.reset()
    EventFabric.reset_dev_state()
    reset_crm_service()
    yield
    from shared.infrastructure.database.engine import dispose_engine

    await dispose_engine()


@pytest.fixture
async def client():
    application = create_app(profile="full", startup_mode="lazy")
    configure_application(application, profile="full", startup_mode="lazy")
    transport = ASGITransport(app=application)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str, email: str | None = None) -> dict[str, str]:
    login_email = email or f"crm-{uuid.uuid4().hex[:8]}@dev.io"
    await client.post(
        "/api/v1/auth/register",
        json={"email": login_email, "password": "SecurePass123!", "display_name": "CRM Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": login_email, "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    assert login.status_code == 200, login.text
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_crm_contact_opportunity_win_flow(client):
    tenant = f"crm-demo-{uuid.uuid4().hex[:8]}"
    headers = await _auth_headers(client, tenant)

    contact = await client.post(
        "/api/v1/crm/contacts",
        json={
            "email": f"buyer-{uuid.uuid4().hex[:8]}@acme.io",
            "full_name": "Ada Buyer",
            "company": "Acme",
            "phone": "+1-555-0100",
        },
        headers=headers,
    )
    assert contact.status_code == 201, contact.text
    contact_id = contact.json()["data"]["id"]

    listed = await client.get("/api/v1/crm/contacts", headers=headers)
    assert listed.status_code == 200
    assert listed.json()["data"]["total"] >= 1

    opportunity = await client.post(
        "/api/v1/crm/opportunities",
        json={
            "contact_id": contact_id,
            "title": "Enterprise license",
            "amount": "25000.00",
            "currency": "USD",
        },
        headers=headers,
    )
    assert opportunity.status_code == 201, opportunity.text
    opportunity_id = opportunity.json()["data"]["id"]
    assert opportunity.json()["data"]["stage"] == "qualifying"

    won = await client.post(
        f"/api/v1/crm/opportunities/{opportunity_id}/win",
        headers=headers,
    )
    assert won.status_code == 200, won.text
    assert won.json()["data"]["stage"] == "won"

    again = await client.post(
        f"/api/v1/crm/opportunities/{opportunity_id}/win",
        headers=headers,
    )
    assert again.status_code == 400


@pytest.mark.asyncio
async def test_crm_tenant_b_cannot_list_tenant_a_contacts(client):
    headers_a = await _auth_headers(client, f"crm-tenant-a-{uuid.uuid4().hex[:8]}")
    created = await client.post(
        "/api/v1/crm/contacts",
        json={
            "email": f"secret-{uuid.uuid4().hex[:8]}@a.example",
            "full_name": "Tenant A Only",
            "company": "A",
        },
        headers=headers_a,
    )
    assert created.status_code == 201, created.text
    contact_id = created.json()["data"]["id"]

    headers_b = await _auth_headers(client, f"crm-tenant-b-{uuid.uuid4().hex[:8]}")
    listed = await client.get("/api/v1/crm/contacts", headers=headers_b)
    assert listed.status_code == 200
    ids = [row.get("id") for row in listed.json()["data"].get("items", [])]
    assert contact_id not in ids

    leaked = await client.get(f"/api/v1/crm/contacts/{contact_id}", headers=headers_b)
    assert leaked.status_code in (403, 404)
