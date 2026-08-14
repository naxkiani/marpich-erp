"""Inventory stock + sales order reservation — CAP-ENT-042."""
from decimal import Decimal

import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.crm.container import reset_crm_service
from contexts.crm.infrastructure.persistence.memory_store import CrmMemoryStore
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from contexts.inventory.container import reset_inventory_service
from contexts.inventory.infrastructure.persistence.memory_store import InventoryMemoryStore
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
    InventoryMemoryStore.reset()
    InProcessEventBus.reset()
    EventFabric.reset_dev_state()
    reset_crm_service()
    reset_sales_service()
    reset_inventory_service()
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
        json={
            "email": "inventory@dev.io",
            "password": "SecurePass123!",
            "display_name": "Inventory Admin",
        },
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "inventory@dev.io", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    assert login.status_code == 200, login.text
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_sales_order_reserves_stock(client):
    tenant = "inv-demo"
    headers = await _auth_headers(client, tenant)

    seeded = await client.put(
        "/api/v1/inventory/stock",
        json={"sku": "SALES-STD", "quantity": "100"},
        headers=headers,
    )
    assert seeded.status_code == 200, seeded.text
    assert Decimal(seeded.json()["data"]["quantity_on_hand"]) == Decimal("100")

    contact = await client.post(
        "/api/v1/crm/contacts",
        json={"email": "buyer@acme.io", "full_name": "Ada Buyer", "company": "Acme"},
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

    quotations = await client.get("/api/v1/sales/quotations", headers=headers)
    assert quotations.status_code == 200, quotations.text
    quotation = next(
        q
        for q in quotations.json()["data"]["items"]
        if q["opportunity_id"] == opportunity_id
    )
    quotation_id = quotation["id"]

    sent = await client.post(
        f"/api/v1/sales/quotations/{quotation_id}/send",
        headers=headers,
    )
    assert sent.status_code == 200, sent.text

    converted = await client.post(
        f"/api/v1/sales/quotations/{quotation_id}/convert",
        headers=headers,
    )
    assert converted.status_code == 200, converted.text

    stock = await client.get("/api/v1/inventory/stock/SALES-STD", headers=headers)
    assert stock.status_code == 200, stock.text
    data = stock.json()["data"]
    assert Decimal(data["quantity_reserved"]) >= Decimal("1")
    assert Decimal(data["quantity_on_hand"]) >= Decimal("100")
    assert Decimal(data["quantity_available"]) == Decimal(data["quantity_on_hand"]) - Decimal(
        data["quantity_reserved"]
    )