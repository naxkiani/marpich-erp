"""AR invoice from sales order — CAP-ENT-023."""
from decimal import Decimal

import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.accounting.container import reset_accounting_service
from contexts.accounting.infrastructure.persistence.memory_store import AccountingMemoryStore
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
    AccountingMemoryStore.reset()
    InProcessEventBus.reset()
    EventFabric.reset_dev_state()
    reset_crm_service()
    reset_sales_service()
    reset_inventory_service()
    reset_accounting_service()
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
            "email": "ar@dev.io",
            "password": "SecurePass123!",
            "display_name": "AR Admin",
        },
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "ar@dev.io", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    assert login.status_code == 200, login.text
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_sales_order_drafts_ar_invoice_then_issue(client):
    tenant = "ar-demo"
    headers = await _auth_headers(client, tenant)

    # Seed stock so inventory ACL does not fail the sales.order.placed bus delivery
    seeded = await client.put(
        "/api/v1/inventory/stock",
        json={"sku": "SALES-STD", "quantity": "100"},
        headers=headers,
    )
    assert seeded.status_code == 200, seeded.text

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
    quotation = next(
        q
        for q in quotations.json()["data"]["items"]
        if q["opportunity_id"] == opportunity_id
    )
    quotation_id = quotation["id"]

    assert (
        await client.post(f"/api/v1/sales/quotations/{quotation_id}/send", headers=headers)
    ).status_code == 200

    converted = await client.post(
        f"/api/v1/sales/quotations/{quotation_id}/convert",
        headers=headers,
    )
    assert converted.status_code == 200, converted.text
    order_id = converted.json()["data"]["order"]["id"]

    invoices = await client.get("/api/v1/accounting/invoices", headers=headers)
    assert invoices.status_code == 200, invoices.text
    body = invoices.json()["data"]
    assert body["total"] >= 1
    invoice = next(i for i in body["items"] if i["sales_order_id"] == order_id)
    assert invoice["status"] == "draft"
    assert Decimal(invoice["amount"]) == Decimal("25000.00")
    invoice_id = invoice["id"]

    # Idempotent: no duplicate on re-list after same order
    by_order = await client.get(f"/api/v1/accounting/invoices/by-order/{order_id}", headers=headers)
    assert by_order.status_code == 200
    assert by_order.json()["data"]["id"] == invoice_id

    issued = await client.post(
        f"/api/v1/accounting/invoices/{invoice_id}/issue",
        headers=headers,
    )
    assert issued.status_code == 200, issued.text
    assert issued.json()["data"]["status"] == "issued"

    again = await client.post(
        f"/api/v1/accounting/invoices/{invoice_id}/issue",
        headers=headers,
    )
    assert again.status_code == 400
