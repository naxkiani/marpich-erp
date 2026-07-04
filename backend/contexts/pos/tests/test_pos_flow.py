"""POS checkout flow tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from contexts.pos.container import reset_pos_service
from contexts.pos.infrastructure.persistence.memory_store import PosMemoryStore
from core.presentation.api.main import app
from shared.infrastructure.messaging.event_bus import InProcessEventBus


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    PosMemoryStore.reset()
    InProcessEventBus.reset()
    reset_pos_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
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
    assert sale.status_code == 201
    assert "receipt" in sale.json()["data"]

    closed = await client.post(f"/api/v1/pos/shifts/{shift_id}/close", headers=headers)
    assert closed.status_code == 200
    assert closed.json()["data"]["status"] == "closed"
