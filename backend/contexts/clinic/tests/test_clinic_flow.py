"""Clinic ambulatory care flow tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.clinic.container import reset_clinic_service
from contexts.clinic.infrastructure.persistence.memory_store import ClinicMemoryStore
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from core.presentation.api.main import app
from shared.infrastructure.messaging.event_bus import InProcessEventBus


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    ClinicMemoryStore.reset()
    InProcessEventBus.reset()
    reset_clinic_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "clinic@dev.io", "password": "SecurePass123!", "display_name": "Clinic Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "clinic@dev.io", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_clinic_appointment_to_referral_flow(client):
    tenant = "city-clinic"
    headers = await _auth_headers(client, tenant)

    patient = await client.post(
        "/api/v1/clinic/patients",
        json={
            "patient_number": "CLN-1001",
            "first_name": "Sara",
            "last_name": "Ahmadi",
            "date_of_birth": "1988-03-12",
        },
        headers=headers,
    )
    assert patient.status_code == 201
    patient_id = patient.json()["data"]["id"]

    appointment = await client.post(
        "/api/v1/clinic/appointments",
        json={
            "patient_id": patient_id,
            "provider_name": "Dr. Karimi",
            "scheduled_at": "2026-07-10T09:00:00+00:00",
        },
        headers=headers,
    )
    assert appointment.status_code == 201
    appointment_id = appointment.json()["data"]["id"]

    encounter = await client.post(
        "/api/v1/clinic/encounters",
        json={"appointment_id": appointment_id},
        headers=headers,
    )
    assert encounter.status_code == 201
    encounter_id = encounter.json()["data"]["id"]

    complete = await client.post(
        f"/api/v1/clinic/encounters/{encounter_id}/complete",
        json={"diagnosis_codes": ["J06.9"]},
        headers=headers,
    )
    assert complete.status_code == 200

    referral = await client.post(
        "/api/v1/clinic/referrals",
        json={
            "encounter_id": encounter_id,
            "target_specialty": "cardiology",
            "reason": "Chest pain follow-up",
            "send": True,
        },
        headers=headers,
    )
    assert referral.status_code == 201
    assert referral.json()["data"]["status"] == "sent"
