"""CAP-HLT-005 — start → document → complete clinical encounter."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.core_platform.container import reset_platform_service
from contexts.core_platform.infrastructure.persistence.memory_store import PlatformMemoryStore
from contexts.hospital.container import reset_hospital_service
from contexts.hospital.infrastructure.persistence.memory_store import HospitalMemoryStore
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from core.presentation.api.app_factory import create_app
from core.presentation.api.startup_registry import configure_application
from shared.infrastructure.messaging.event_bus import InProcessEventBus
from shared.infrastructure.messaging.event_fabric import EventFabric


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    PlatformMemoryStore.reset()
    HospitalMemoryStore.reset()
    EventFabric.reset_dev_state()
    reset_platform_service()
    reset_hospital_service()
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
        json={"name": "Hospital Encounter", "slug": tenant, "industry_pack": "hospital"},
    )
    await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "SecurePass123!", "display_name": "H Admin"},
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


async def _active_admission(client: AsyncClient, headers: dict[str, str]) -> str:
    patient = await client.post(
        "/api/v1/hospital/patients",
        json={
            "mrn": "MRN-ENC-1",
            "first_name": "Sara",
            "last_name": "Rezaei",
            "date_of_birth": "1985-03-12",
        },
        headers=headers,
    )
    assert patient.status_code == 201, patient.text
    admit = await client.post(
        "/api/v1/hospital/admissions",
        json={"patient_id": patient.json()["data"]["id"], "ward": "ICU"},
        headers=headers,
    )
    assert admit.status_code == 201, admit.text
    return admit.json()["data"]["id"]


@pytest.mark.asyncio
async def test_start_document_complete_and_events(client):
    headers = await _admin(client, "hosp-enc", "enc@demo.dev")
    published: list[str] = []

    async def capture(envelope: dict) -> None:
        published.append(envelope["event_name"])

    for name in (
        "hospital.encounter.started",
        "hospital.encounter.documented",
        "hospital.encounter.completed",
    ):
        InProcessEventBus.subscribe(name, capture)

    admission_id = await _active_admission(client, headers)

    start = await client.post(
        "/api/v1/hospital/encounters",
        json={"admission_id": admission_id},
        headers=headers,
    )
    assert start.status_code == 201, start.text
    encounter_id = start.json()["data"]["id"]
    assert start.json()["data"]["status"] == "in_progress"
    assert "hospital.encounter.started" in published

    document = await client.post(
        f"/api/v1/hospital/encounters/{encounter_id}/document",
        json={"procedure_codes": ["99223", "99223"], "diagnosis_codes": ["J18.9"]},
        headers=headers,
    )
    assert document.status_code == 200, document.text
    data = document.json()["data"]
    assert data["procedure_codes"] == ["99223"]
    assert data["diagnosis_codes"] == ["J18.9"]
    assert data["status"] == "in_progress"
    assert "hospital.encounter.documented" in published

    complete = await client.post(
        f"/api/v1/hospital/encounters/{encounter_id}/complete",
        json={"procedure_codes": ["93000"], "diagnosis_codes": ["J18.9", "I10"]},
        headers=headers,
    )
    assert complete.status_code == 200, complete.text
    done = complete.json()["data"]
    assert done["status"] == "completed"
    assert done["procedure_codes"] == ["99223", "93000"]
    assert done["diagnosis_codes"] == ["J18.9", "I10"]
    assert "hospital.encounter.completed" in published


@pytest.mark.asyncio
async def test_reject_document_and_complete_after_complete(client):
    headers = await _admin(client, "hosp-enc-neg", "encneg@demo.dev")
    admission_id = await _active_admission(client, headers)
    start = await client.post(
        "/api/v1/hospital/encounters",
        json={"admission_id": admission_id},
        headers=headers,
    )
    encounter_id = start.json()["data"]["id"]
    done = await client.post(
        f"/api/v1/hospital/encounters/{encounter_id}/complete",
        json={"procedure_codes": ["99223"]},
        headers=headers,
    )
    assert done.status_code == 200, done.text

    document = await client.post(
        f"/api/v1/hospital/encounters/{encounter_id}/document",
        json={"procedure_codes": ["93000"]},
        headers=headers,
    )
    assert document.status_code == 400
    assert document.json()["detail"] == "hospital.errors.encounter_not_in_progress"

    again = await client.post(
        f"/api/v1/hospital/encounters/{encounter_id}/complete",
        json={},
        headers=headers,
    )
    assert again.status_code == 400
    assert again.json()["detail"] == "hospital.errors.encounter_already_completed"


@pytest.mark.asyncio
async def test_list_encounters_filters_by_status_and_admission(client):
    headers = await _admin(client, "hosp-enc-list", "enclist@demo.dev")
    admission_id = await _active_admission(client, headers)
    other_patient = await client.post(
        "/api/v1/hospital/patients",
        json={
            "mrn": "MRN-ENC-2",
            "first_name": "Omar",
            "last_name": "Hakimi",
            "date_of_birth": "1992-07-01",
        },
        headers=headers,
    )
    other_admit = await client.post(
        "/api/v1/hospital/admissions",
        json={"patient_id": other_patient.json()["data"]["id"], "ward": "MED"},
        headers=headers,
    )
    other_admission_id = other_admit.json()["data"]["id"]

    first = await client.post(
        "/api/v1/hospital/encounters",
        json={"admission_id": admission_id},
        headers=headers,
    )
    second = await client.post(
        "/api/v1/hospital/encounters",
        json={"admission_id": other_admission_id},
        headers=headers,
    )
    await client.post(
        f"/api/v1/hospital/encounters/{first.json()['data']['id']}/complete",
        json={"procedure_codes": ["99223"]},
        headers=headers,
    )

    by_admission = await client.get(
        "/api/v1/hospital/encounters",
        params={"admission_id": admission_id},
        headers=headers,
    )
    assert by_admission.status_code == 200
    assert by_admission.json()["data"]["total"] == 1
    assert by_admission.json()["data"]["items"][0]["id"] == first.json()["data"]["id"]

    open_only = await client.get(
        "/api/v1/hospital/encounters",
        params={"status": "in_progress"},
        headers=headers,
    )
    assert open_only.status_code == 200
    assert open_only.json()["data"]["total"] == 1
    assert open_only.json()["data"]["items"][0]["id"] == second.json()["data"]["id"]
