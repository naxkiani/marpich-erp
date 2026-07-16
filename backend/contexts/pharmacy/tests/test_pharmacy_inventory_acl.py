"""Pharmacy dispense → inventory stock ACL (drug_code as SKU)."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.core_platform.container import reset_platform_service
from contexts.core_platform.infrastructure.persistence.memory_store import PlatformMemoryStore
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from contexts.inventory.container import get_inventory_service, reset_inventory_service
from contexts.inventory.infrastructure.persistence.memory_store import InventoryMemoryStore
from contexts.pharmacy.container import reset_pharmacy_service
from contexts.pharmacy.infrastructure.persistence.memory_store import PharmacyMemoryStore
from core.presentation.api.app_factory import create_app
from core.presentation.api.startup_registry import configure_application
from shared.infrastructure.messaging.event_bus import InProcessEventBus
from shared.infrastructure.messaging.event_fabric import EventFabric


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    PlatformMemoryStore.reset()
    PharmacyMemoryStore.reset()
    InventoryMemoryStore.reset()
    EventFabric.reset_dev_state()
    InProcessEventBus.reset()
    reset_platform_service()
    reset_pharmacy_service()
    reset_inventory_service()
    get_inventory_service()
    yield


@pytest.fixture
async def client():
    application = create_app(profile="industry", startup_mode="lazy")
    configure_application(application, profile="industry", startup_mode="lazy")
    transport = ASGITransport(app=application)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _admin(client: AsyncClient, tenant: str, email: str) -> dict[str, str]:
    await client.post(
        "/api/v1/platform/tenants",
        json={"name": "Pharmacy ACL", "slug": tenant, "industry_pack": "pharmacy"},
    )
    await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "SecurePass123!", "display_name": "Rx Admin"},
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
async def test_pharmacy_dispense_decrements_inventory(client):
    headers = await _admin(client, "pharm-acl", "rx-acl@demo.dev")

    stock = await client.put(
        "/api/v1/inventory/stock",
        json={"sku": "AMOX500", "quantity": "100"},
        headers=headers,
    )
    assert stock.status_code == 200, stock.text

    rx = await client.post(
        "/api/v1/pharmacy/prescriptions",
        json={
            "rx_number": "RX-ACL-1",
            "patient_ref": "peer-patient-1",
            "drug_code": "AMOX500",
            "drug_name": "Amoxicillin 500mg",
            "quantity": 12,
        },
        headers=headers,
    )
    assert rx.status_code == 201, rx.text
    prescription_id = rx.json()["data"]["id"]

    dispense = await client.post(
        "/api/v1/pharmacy/dispenses",
        json={"prescription_id": prescription_id},
        headers=headers,
    )
    assert dispense.status_code == 201, dispense.text

    after = await client.get("/api/v1/inventory/stock/AMOX500", headers=headers)
    assert after.status_code == 200, after.text
    assert float(after.json()["data"]["quantity_on_hand"]) == 88.0

    # Idempotent: replaying the ACL via a second dispense is blocked at pharmacy,
    # but inventory dedupe key would also no-op for the same dispense_id.
    listed = await client.get("/api/v1/inventory/stock", headers=headers)
    assert listed.status_code == 200
