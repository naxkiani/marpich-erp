"""P2 — POS retail slice: checkout → inventory decrement → GL posting."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.core_platform.container import reset_platform_service
from contexts.core_platform.infrastructure.persistence.memory_store import PlatformMemoryStore
from contexts.financial_kernel.container import (
    get_financial_kernel_service,
    reset_financial_kernel_service,
)
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from contexts.inventory.container import get_inventory_service, reset_inventory_service
from contexts.inventory.infrastructure.persistence.memory_store import InventoryMemoryStore
from contexts.pos.container import get_pos_service, reset_pos_service
from contexts.pos.infrastructure.persistence.memory_store import PosMemoryStore
from core.presentation.api.app_factory import create_app
from core.presentation.api.startup_registry import configure_application
from shared.infrastructure.messaging.event_fabric import EventFabric

@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    PlatformMemoryStore.reset()
    PosMemoryStore.reset()
    InventoryMemoryStore.reset()
    EventFabric.reset_dev_state()
    reset_platform_service()
    reset_pos_service()
    reset_inventory_service()
    reset_financial_kernel_service()
    get_pos_service()
    get_inventory_service()
    get_financial_kernel_service()
    yield


@pytest.fixture
async def client():
    application = create_app(profile="industry", startup_mode="lazy")
    configure_application(application, profile="industry", startup_mode="lazy")
    transport = ASGITransport(app=application)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _admin(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "pos@retail.dev", "password": "SecurePass123!", "display_name": "POS Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "pos@retail.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    assert login.status_code == 200, login.text
    return {
        "X-Tenant-ID": tenant,
        "Authorization": f"Bearer {login.json()['data']['access_token']}",
    }


@pytest.mark.asyncio
async def test_pos_sale_decrements_stock_and_posts_gl(client):
    slug = "retail-pos-p2"
    await client.post(
        "/api/v1/platform/tenants",
        json={"name": "Retail Shop", "slug": slug, "industry_pack": "retail"},
    )
    # Ensure COA for retail even if platform event path differs
    await get_financial_kernel_service().handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {"industry_pack": "retail"}}
    )
    headers = await _admin(client, slug)

    stock = await client.put(
        "/api/v1/inventory/stock",
        json={"sku": "SKU-1", "quantity": "10"},
        headers=headers,
    )
    assert stock.status_code == 200, stock.text
    assert stock.json()["data"]["quantity_on_hand"] == "10"

    terminal = await client.post(
        "/api/v1/pos/terminals",
        json={"terminal_code": "T01", "store_name": "Main Street"},
        headers=headers,
    )
    assert terminal.status_code == 201, terminal.text
    terminal_id = terminal.json()["data"]["id"]

    shift = await client.post(
        "/api/v1/pos/shifts",
        json={"terminal_id": terminal_id, "cashier_name": "Reza"},
        headers=headers,
    )
    assert shift.status_code == 201, shift.text
    shift_id = shift.json()["data"]["id"]

    sale = await client.post(
        "/api/v1/pos/sales",
        json={
            "shift_id": shift_id,
            "items": [{"sku": "SKU-1", "name": "Coffee", "quantity": 2, "unit_price": "5.00"}],
            "subtotal": "10.00",
            "tax": "1.00",
            "payment_method": "card",
        },
        headers=headers,
    )
    assert sale.status_code == 201, sale.text
    sale_id = sale.json()["data"]["sale"]["id"]

    after = await client.get("/api/v1/inventory/stock/SKU-1", headers=headers)
    assert after.status_code == 200, after.text
    assert after.json()["data"]["quantity_on_hand"] == "8"

    journals = (await get_financial_kernel_service().list_journals(slug)).unwrap()
    posted = [j for j in journals if j.get("source_document_id") == sale_id]
    assert len(posted) == 1
    assert posted[0]["status"] == "posted"
    assert posted[0]["source_context"] == "pos"

    # Idempotent: replay must not double-post or double-decrement
    from contexts.financial_kernel.application.pos_posting_bridge import PosPostingBridge
    from contexts.inventory.infrastructure.acl.pos_events import handle_pos_sale_completed

    envelope = {
        "event_name": "pos.sale.completed",
        "event_id": "replay-evt-1",
        "tenant_id": slug,
        "correlation_id": "replay",
        "payload": {
            "sale_id": sale_id,
            "total": "11.00",
            "currency": "USD",
            "payment_method": "card",
            "items": [{"sku": "SKU-1", "quantity": 2, "unit_price": "5.00"}],
        },
    }
    await handle_pos_sale_completed(envelope)
    await PosPostingBridge(get_financial_kernel_service()).handle_sale_completed(envelope)

    after2 = await client.get("/api/v1/inventory/stock/SKU-1", headers=headers)
    assert after2.json()["data"]["quantity_on_hand"] == "8"
    journals2 = (await get_financial_kernel_service().list_journals(slug)).unwrap()
    posted2 = [j for j in journals2 if j.get("source_document_id") == sale_id]
    assert len(posted2) == 1
