"""CAP-HLT-004 — beds, assign, transfer, discharge."""
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
        json={"name": "Hospital Beds", "slug": tenant, "industry_pack": "hospital"},
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


async def _patient_and_beds(client: AsyncClient, headers: dict[str, str]) -> tuple[str, str, str]:
    patient = await client.post(
        "/api/v1/hospital/patients",
        json={
            "mrn": "MRN-BED-1",
            "first_name": "Ava",
            "last_name": "Nouri",
            "date_of_birth": "1990-01-02",
        },
        headers=headers,
    )
    assert patient.status_code == 201, patient.text
    patient_id = patient.json()["data"]["id"]

    bed_a = await client.post(
        "/api/v1/hospital/beds",
        json={"ward": "ICU", "room": "101", "bed_code": "A"},
        headers=headers,
    )
    assert bed_a.status_code == 201, bed_a.text
    bed_a_id = bed_a.json()["data"]["id"]

    bed_b = await client.post(
        "/api/v1/hospital/beds",
        json={"ward": "MED", "room": "201", "bed_code": "B"},
        headers=headers,
    )
    assert bed_b.status_code == 201, bed_b.text
    bed_b_id = bed_b.json()["data"]["id"]
    return patient_id, bed_a_id, bed_b_id


@pytest.mark.asyncio
async def test_bed_assign_transfer_discharge(client):
    headers = await _admin(client, "hosp-beds", "beds@demo.dev")
    patient_id, bed_a_id, bed_b_id = await _patient_and_beds(client, headers)

    admit = await client.post(
        "/api/v1/hospital/admissions",
        json={"patient_id": patient_id, "ward": "ICU", "bed_id": bed_a_id},
        headers=headers,
    )
    assert admit.status_code == 201, admit.text
    admission_id = admit.json()["data"]["id"]
    assert admit.json()["data"]["bed_id"] == bed_a_id
    assert admit.json()["data"]["status"] == "active"

    beds = await client.get("/api/v1/hospital/beds", headers=headers)
    assert beds.status_code == 200
    by_id = {b["id"]: b for b in beds.json()["data"]["items"]}
    assert by_id[bed_a_id]["status"] == "occupied"
    assert by_id[bed_b_id]["status"] == "available"

    transfer = await client.post(
        f"/api/v1/hospital/admissions/{admission_id}/transfer",
        json={"to_ward": "MED", "to_bed_id": bed_b_id},
        headers=headers,
    )
    assert transfer.status_code == 200, transfer.text
    assert transfer.json()["data"]["ward"] == "MED"
    assert transfer.json()["data"]["bed_id"] == bed_b_id

    beds2 = await client.get("/api/v1/hospital/beds", headers=headers)
    by_id2 = {b["id"]: b for b in beds2.json()["data"]["items"]}
    assert by_id2[bed_a_id]["status"] == "available"
    assert by_id2[bed_b_id]["status"] == "occupied"

    encounter = await client.post(
        "/api/v1/hospital/encounters",
        json={"admission_id": admission_id},
        headers=headers,
    )
    assert encounter.status_code == 201, encounter.text

    discharge = await client.post(
        f"/api/v1/hospital/admissions/{admission_id}/discharge",
        headers=headers,
    )
    assert discharge.status_code == 200, discharge.text
    assert discharge.json()["data"]["status"] == "discharged"
    assert discharge.json()["data"]["bed_id"] is None
    assert discharge.json()["data"]["discharged_at"]

    beds3 = await client.get("/api/v1/hospital/beds", headers=headers)
    by_id3 = {b["id"]: b for b in beds3.json()["data"]["items"]}
    assert by_id3[bed_b_id]["status"] == "available"

    again = await client.post(
        f"/api/v1/hospital/admissions/{admission_id}/discharge",
        headers=headers,
    )
    assert again.status_code == 400

    blocked_enc = await client.post(
        "/api/v1/hospital/encounters",
        json={"admission_id": admission_id},
        headers=headers,
    )
    assert blocked_enc.status_code == 400


@pytest.mark.asyncio
async def test_assign_bed_endpoint_and_events(client):
    headers = await _admin(client, "hosp-assign", "assign@demo.dev")
    published: list[str] = []

    async def capture(envelope: dict) -> None:
        published.append(envelope["event_name"])

    for name in (
        "hospital.admission.registered",
        "hospital.bed.assigned",
        "hospital.admission.transferred",
        "hospital.admission.discharged",
    ):
        InProcessEventBus.subscribe(name, capture)

    patient_id, bed_a_id, bed_b_id = await _patient_and_beds(client, headers)

    admit = await client.post(
        "/api/v1/hospital/admissions",
        json={"patient_id": patient_id, "ward": "ICU"},
        headers=headers,
    )
    assert admit.status_code == 201, admit.text
    admission_id = admit.json()["data"]["id"]
    assert admit.json()["data"]["bed_id"] is None
    assert "hospital.admission.registered" in published

    assign = await client.post(
        f"/api/v1/hospital/admissions/{admission_id}/assign-bed",
        json={"bed_id": bed_a_id},
        headers=headers,
    )
    assert assign.status_code == 200, assign.text
    assert assign.json()["data"]["bed_id"] == bed_a_id
    assert "hospital.bed.assigned" in published

    transfer = await client.post(
        f"/api/v1/hospital/admissions/{admission_id}/transfer",
        json={"to_ward": "MED", "to_bed_id": bed_b_id},
        headers=headers,
    )
    assert transfer.status_code == 200, transfer.text
    assert "hospital.admission.transferred" in published

    discharge = await client.post(
        f"/api/v1/hospital/admissions/{admission_id}/discharge",
        headers=headers,
    )
    assert discharge.status_code == 200, discharge.text
    assert "hospital.admission.discharged" in published


@pytest.mark.asyncio
async def test_bed_negatives_occupied_duplicate_ward_mismatch(client):
    headers = await _admin(client, "hosp-neg", "neg@demo.dev")
    patient_id, bed_a_id, bed_b_id = await _patient_and_beds(client, headers)

    dup = await client.post(
        "/api/v1/hospital/beds",
        json={"ward": "ICU", "room": "101", "bed_code": "A"},
        headers=headers,
    )
    assert dup.status_code == 400
    assert dup.json()["detail"] == "hospital.errors.bed_exists"

    admit = await client.post(
        "/api/v1/hospital/admissions",
        json={"patient_id": patient_id, "ward": "ICU", "bed_id": bed_a_id},
        headers=headers,
    )
    assert admit.status_code == 201, admit.text

    patient2 = await client.post(
        "/api/v1/hospital/patients",
        json={
            "mrn": "MRN-BED-2",
            "first_name": "Ben",
            "last_name": "Karimi",
            "date_of_birth": "1988-05-05",
        },
        headers=headers,
    )
    assert patient2.status_code == 201, patient2.text
    occupied = await client.post(
        "/api/v1/hospital/admissions",
        json={
            "patient_id": patient2.json()["data"]["id"],
            "ward": "ICU",
            "bed_id": bed_a_id,
        },
        headers=headers,
    )
    assert occupied.status_code == 400
    assert occupied.json()["detail"] == "hospital.errors.bed_occupied"

    mismatch = await client.post(
        f"/api/v1/hospital/admissions/{admit.json()['data']['id']}/transfer",
        json={"to_ward": "SURG", "to_bed_id": bed_b_id},
        headers=headers,
    )
    assert mismatch.status_code == 400
    assert mismatch.json()["detail"] == "hospital.errors.bed_ward_mismatch"


@pytest.mark.asyncio
async def test_hospital_ai_surfaces_and_infer(client):
    headers = await _admin(client, "hosp-ai", "ai@demo.dev")
    surfaces = await client.get("/api/v1/hospital/ai/surfaces", headers=headers)
    assert surfaces.status_code == 200, surfaces.text
    data = surfaces.json()["data"]
    assert data["module"] == "hospital"
    assert data["embedded_llm_forbidden"] is True
    assert len(data["surfaces"]) == 14

    infer = await client.post(
        "/api/v1/hospital/ai/infer",
        json={"surface": "summaries", "payload": {"admission_id": "demo"}},
        headers=headers,
    )
    assert infer.status_code == 200, infer.text
    body = infer.json()["data"]
    assert body["status"] == "delegated"
    assert body["embedded_llm"] is False
    assert body["prompt_template"] == "hospital.encounter.summary"

    bad = await client.post(
        "/api/v1/hospital/ai/infer",
        json={"surface": "not-a-surface", "payload": {}},
        headers=headers,
    )
    assert bad.status_code == 400
