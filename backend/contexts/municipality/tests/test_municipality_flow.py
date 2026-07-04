"""Municipality flow tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from contexts.municipality.container import reset_municipality_service
from contexts.municipality.infrastructure.persistence.memory_store import MunicipalityMemoryStore
from core.presentation.api.main import app
from shared.infrastructure.messaging.event_bus import InProcessEventBus


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    MunicipalityMemoryStore.reset()
    InProcessEventBus.reset()
    reset_municipality_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "muni@dev.io", "password": "SecurePass123!", "display_name": "Muni Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "muni@dev.io", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_permit_and_utility_bill_flow(client):
    tenant = "north-muni"
    headers = await _auth_headers(client, tenant)

    permit = await client.post(
        "/api/v1/municipality/permits",
        json={
            "applicant_name": "Building Co",
            "permit_type": "construction",
            "description": "Residential extension",
        },
        headers=headers,
    )
    assert permit.status_code == 201
    permit_id = permit.json()["data"]["id"]

    issued = await client.post(f"/api/v1/municipality/permits/{permit_id}/issue", headers=headers)
    assert issued.status_code == 200
    assert issued.json()["data"]["status"] == "issued"

    account = await client.post(
        "/api/v1/municipality/utilities/accounts",
        json={"account_number": "WTR-9001", "holder_name": "Building Co", "utility_type": "water"},
        headers=headers,
    )
    assert account.status_code == 201
    account_id = account.json()["data"]["id"]

    bill = await client.post(
        f"/api/v1/municipality/utilities/accounts/{account_id}/bill",
        json={"amount": "125000.00", "period": "2026-Q2"},
        headers=headers,
    )
    assert bill.status_code == 201
    assert bill.json()["data"]["bill"]["amount"] == "125000.00"
