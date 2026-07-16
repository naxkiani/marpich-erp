"""P0 — Pharmacy CAP-HLT-008 receive→dispense stub."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.core_platform.container import reset_platform_service
from contexts.core_platform.infrastructure.persistence.memory_store import PlatformMemoryStore
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from contexts.pharmacy.container import reset_pharmacy_service
from contexts.pharmacy.infrastructure.persistence.memory_store import PharmacyMemoryStore
from core.presentation.api.app_factory import create_app
from core.presentation.api.startup_registry import configure_application
from shared.infrastructure.messaging.event_fabric import EventFabric


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    PlatformMemoryStore.reset()
    PharmacyMemoryStore.reset()
    EventFabric.reset_dev_state()
    reset_platform_service()
    reset_pharmacy_service()
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
        json={"name": "Pharmacy Co", "slug": tenant, "industry_pack": "pharmacy"},
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
async def test_pharmacy_receive_and_dispense(client):
    headers = await _admin(client, "pharm-p0", "rx@demo.dev")
    missing = await client.get("/api/v1/pharmacy/prescriptions")
    assert missing.status_code == 400

    rx = await client.post(
        "/api/v1/pharmacy/prescriptions",
        json={
            "rx_number": "RX-1001",
            "patient_ref": "hospital-patient-uuid",
            "drug_code": "AMOX500",
            "drug_name": "Amoxicillin 500mg",
            "quantity": 20,
        },
        headers=headers,
    )
    assert rx.status_code == 201, rx.text
    data = rx.json()["data"]
    assert data["status"] == "received"
    prescription_id = data["id"]

    listed = await client.get("/api/v1/pharmacy/prescriptions", headers=headers)
    assert listed.status_code == 200
    assert listed.json()["data"]["total"] == 1

    dispense = await client.post(
        "/api/v1/pharmacy/dispenses",
        json={"prescription_id": prescription_id},
        headers=headers,
    )
    assert dispense.status_code == 201, dispense.text
    assert dispense.json()["data"]["quantity_dispensed"] == 20

    again = await client.post(
        "/api/v1/pharmacy/dispenses",
        json={"prescription_id": prescription_id},
        headers=headers,
    )
    assert again.status_code == 400
