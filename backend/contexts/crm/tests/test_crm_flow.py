"""CRM contact + opportunity flow tests — CAP-ENT-001."""
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
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    CrmMemoryStore.reset()
    InProcessEventBus.reset()
    EventFabric.reset_dev_state()
    reset_crm_service()
    yield


@pytest.fixture
async def client():
    application = create_app(profile="full", startup_mode="lazy")
    configure_application(application, profile="full", startup_mode="lazy")
    transport = ASGITransport(app=application)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "crm@dev.io", "password": "SecurePass123!", "display_name": "CRM Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "crm@dev.io", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    assert login.status_code == 200, login.text
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_crm_contact_opportunity_win_flow(client):
    tenant = "crm-demo"
    headers = await _auth_headers(client, tenant)

    contact = await client.post(
        "/api/v1/crm/contacts",
        json={
            "email": "buyer@acme.io",
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
