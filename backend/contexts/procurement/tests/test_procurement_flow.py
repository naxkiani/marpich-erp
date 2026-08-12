"""Procurement requisition from low stock — CAP-ENT-040."""
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
from contexts.procurement.container import reset_procurement_service
from contexts.procurement.infrastructure.persistence.memory_store import ProcurementMemoryStore
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
    ProcurementMemoryStore.reset()
    InProcessEventBus.reset()
    EventFabric.reset_dev_state()
    reset_crm_service()
    reset_sales_service()
    reset_inventory_service()
    reset_accounting_service()
    reset_procurement_service()
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
            "email": "proc@dev.io",
            "password": "SecurePass123!",
            "display_name": "Procurement Admin",
        },
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "proc@dev.io", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    assert login.status_code == 200, login.text
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_low_stock_triggers_requisition_submit_approve(client):
    tenant = "proc-demo"
    headers = await _auth_headers(client, tenant)

    # 20 on hand → reserve 1 → available 19 < threshold 20 → reorder → requisition
    seeded = await client.put(
        "/api/v1/inventory/stock",
        json={"sku": "SALES-STD", "quantity": "20"},
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

    assert (
        await client.post(f"/api/v1/crm/opportunities/{opportunity_id}/win", headers=headers)
    ).status_code == 200

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

    requisitions = await client.get("/api/v1/procurement/requisitions", headers=headers)
    assert requisitions.status_code == 200, requisitions.text
    body = requisitions.json()["data"]
    assert body["total"] >= 1
    req = next(r for r in body["items"] if r["sku"] == "SALES-STD")
    assert req["status"] == "draft"
    assert Decimal(req["quantity_available"]) < Decimal("20")
    req_id = req["id"]

    submitted = await client.post(
        f"/api/v1/procurement/requisitions/{req_id}/submit",
        headers=headers,
    )
    assert submitted.status_code == 200, submitted.text
    assert submitted.json()["data"]["status"] == "submitted"

    approved = await client.post(
        f"/api/v1/procurement/requisitions/{req_id}/approve",
        headers=headers,
    )
    assert approved.status_code == 200, approved.text
    assert approved.json()["data"]["status"] == "approved"
