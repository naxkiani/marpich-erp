"""POS checkout flow tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
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
    PosMemoryStore.reset()
    InventoryMemoryStore.reset()
    EventFabric.reset_dev_state()
    reset_pos_service()
    reset_inventory_service()
    get_pos_service()
    get_inventory_service()
    yield


@pytest.fixture
async def client():
    application = create_app(profile="industry", startup_mode="lazy")
    configure_application(application, profile="industry", startup_mode="lazy")
    transport = ASGITransport(app=application)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "pos@dev.io", "password": "SecurePass123!", "display_name": "POS Cashier"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "pos@dev.io", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_pos_sale_and_shift_close(client):
    tenant = "retail-pos"
    headers = await _auth_headers(client, tenant)

    stock = await client.put(
        "/api/v1/inventory/stock",
        json={"sku": "SKU-1", "quantity": "20"},
        headers=headers,
    )
    assert stock.status_code == 200, stock.text

    terminal = await client.post(
        "/api/v1/pos/terminals",
        json={"terminal_code": "T01", "store_name": "Main Street"},
        headers=headers,
    )
    assert terminal.status_code == 201
    terminal_id = terminal.json()["data"]["id"]

    shift = await client.post(
        "/api/v1/pos/shifts",
        json={"terminal_id": terminal_id, "cashier_name": "Reza"},
        headers=headers,
    )
    assert shift.status_code == 201
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
    assert "receipt" in sale.json()["data"]

    closed = await client.post(f"/api/v1/pos/shifts/{shift_id}/close", headers=headers)
    assert closed.status_code == 200
    assert closed.json()["data"]["status"] == "closed"
