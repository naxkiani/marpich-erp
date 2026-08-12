"""Sales quotation + order flow — CAP-ENT-002 (CRM win → quote → order)."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.crm.container import reset_crm_service
from contexts.crm.infrastructure.persistence.memory_store import CrmMemoryStore
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from contexts.sales.container import reset_sales_service
from contexts.sales.infrastructure.persistence.memory_store import SalesMemoryStore
from core.presentation.api.app_factory import create_app
from core.presentation.api.startup_registry import configure_application
from shared.infrastructure.messaging.event_bus import InProcessEventBus
from shared.infrastructure.messaging.event_fabric import EventFabric


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    CrmMemoryStore.reset()
    SalesMemoryStore.reset()
    InProcessEventBus.reset()
    EventFabric.reset_dev_state()
    reset_crm_service()
    reset_sales_service()
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
        json={"email": "sales@dev.io", "password": "SecurePass123!", "display_name": "Sales Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "sales@dev.io", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    assert login.status_code == 200, login.text
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_crm_win_drafts_quotation_then_order(client):
    tenant = "sales-demo"
    headers = await _auth_headers(client, tenant)

    contact = await client.post(
        "/api/v1/crm/contacts",
        json={
            "email": "buyer@acme.io",
            "full_name": "Ada Buyer",
            "company": "Acme",
        },
        headers=headers,
    )
    assert contact.status_code == 201, contact.text
    contact_id = contact.json()["data"]["id"]

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

    won = await client.post(
        f"/api/v1/crm/opportunities/{opportunity_id}/win",
        headers=headers,
    )
    assert won.status_code == 200, won.text
    assert won.json()["data"]["stage"] == "won"

    quotations = await client.get("/api/v1/sales/quotations", headers=headers)
    assert quotations.status_code == 200, quotations.text
    body = quotations.json()["data"]
    assert body["total"] >= 1
    quotation = next(q for q in body["items"] if q["opportunity_id"] == opportunity_id)
    assert quotation["status"] == "draft"
    assert quotation["amount"] == "25000.00"
    quotation_id = quotation["id"]

    # Idempotent: second win must not create a duplicate draft
    await client.post(f"/api/v1/crm/opportunities/{opportunity_id}/win", headers=headers)
    again = await client.get("/api/v1/sales/quotations", headers=headers)
    matching = [q for q in again.json()["data"]["items"] if q["opportunity_id"] == opportunity_id]
    assert len(matching) == 1

    sent = await client.post(
        f"/api/v1/sales/quotations/{quotation_id}/send",
        headers=headers,
    )
    assert sent.status_code == 200, sent.text
    assert sent.json()["data"]["status"] == "sent"

    converted = await client.post(
        f"/api/v1/sales/quotations/{quotation_id}/convert",
        headers=headers,
    )
    assert converted.status_code == 200, converted.text
    payload = converted.json()["data"]
    assert payload["quotation"]["status"] == "converted"
    assert payload["order"]["status"] == "confirmed"
    assert payload["order"]["quotation_id"] == quotation_id

    orders = await client.get("/api/v1/sales/orders", headers=headers)
    assert orders.status_code == 200
    assert orders.json()["data"]["total"] >= 1
