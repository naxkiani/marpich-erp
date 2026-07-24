"""End-to-end: Hospital patient → Lab/Pharmacy HTTP APIs → Hospital care-events."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.accounting.container import reset_accounting_service
from contexts.hospital.container import get_hospital_service, reset_hospital_service
from contexts.hospital.infrastructure.persistence.memory_store import HospitalMemoryStore
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from contexts.laboratory.container import get_laboratory_service, reset_laboratory_service
from contexts.laboratory.infrastructure.persistence.memory_store import LaboratoryMemoryStore
from contexts.pharmacy.container import get_pharmacy_service, reset_pharmacy_service
from contexts.pharmacy.infrastructure.persistence.memory_store import PharmacyMemoryStore
from core.presentation.api.app_factory import create_app
from core.presentation.api.startup_registry import configure_application
from shared.infrastructure.messaging.event_bus import InProcessEventBus
from shared.infrastructure.messaging.event_fabric import EventFabric


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    HospitalMemoryStore.reset()
    LaboratoryMemoryStore.reset()
    PharmacyMemoryStore.reset()
    InProcessEventBus.reset()
    EventFabric.reset_dev_state()
    reset_hospital_service()
    reset_laboratory_service()
    reset_pharmacy_service()
    reset_accounting_service()
    get_hospital_service()
    get_laboratory_service()
    get_pharmacy_service()
    yield
    identity_container._container = None
    InMemoryStore.reset()
    HospitalMemoryStore.reset()
    LaboratoryMemoryStore.reset()
    PharmacyMemoryStore.reset()
    InProcessEventBus.reset()
    EventFabric.reset_dev_state()
    reset_hospital_service()
    reset_laboratory_service()
    reset_pharmacy_service()
    reset_accounting_service()


@pytest.fixture
async def client():
    application = create_app(profile="industry", startup_mode="lazy")
    configure_application(application, profile="industry", startup_mode="lazy")
    transport = ASGITransport(app=application)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    reg = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "admin@care-seed.com",
            "password": "SecurePass123!",
            "display_name": "Admin",
        },
        headers={"X-Tenant-ID": tenant},
    )
    assert reg.status_code in (200, 201), reg.text
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "admin@care-seed.com", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    assert login.status_code == 200, login.text
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_lab_pharmacy_http_seed_fills_hospital_care_timeline(client):
    tenant = "acme-care-seed"
    headers = await _auth_headers(client, tenant)

    patient = await client.post(
        "/api/v1/hospital/patients",
        json={
            "mrn": "MRN-SEED-1",
            "first_name": "Dana",
            "last_name": "Seed",
            "date_of_birth": "1993-02-02",
        },
        headers=headers,
    )
    assert patient.status_code == 201, patient.text
    patient_id = patient.json()["data"]["id"]

    admission = await client.post(
        "/api/v1/hospital/admissions",
        json={"patient_id": patient_id, "ward": "Ward-S"},
        headers=headers,
    )
    assert admission.status_code == 201, admission.text
    admission_id = admission.json()["data"]["id"]

    encounter = await client.post(
        "/api/v1/hospital/encounters",
        json={"admission_id": admission_id},
        headers=headers,
    )
    assert encounter.status_code == 201, encounter.text
    encounter_id = encounter.json()["data"]["id"]

    order = await client.post(
        "/api/v1/laboratory/orders",
        json={
            "order_number": "CARE-SEED-CBC",
            "patient_ref": patient_id,
            "test_code": "CBC",
            "source_encounter_ref": encounter_id,
        },
        headers=headers,
    )
    assert order.status_code == 201, order.text
    order_id = order.json()["data"]["id"]

    sample = await client.post(
        "/api/v1/laboratory/samples",
        json={
            "order_id": order_id,
            "accession_number": "ACC-SEED-1",
            "specimen_type": "blood",
        },
        headers=headers,
    )
    assert sample.status_code == 201, sample.text

    result = await client.post(
        f"/api/v1/laboratory/orders/{order_id}/results",
        json={"result_value": "13.2", "result_unit": "g/dL"},
        headers=headers,
    )
    assert result.status_code == 200, result.text

    rx = await client.post(
        "/api/v1/pharmacy/prescriptions",
        json={
            "rx_number": "RX-CARE-SEED-1",
            "patient_ref": patient_id,
            "drug_code": "AMOX500",
            "drug_name": "Amoxicillin 500mg",
            "quantity": 21,
            "source_encounter_ref": encounter_id,
        },
        headers=headers,
    )
    assert rx.status_code == 201, rx.text
    rx_id = rx.json()["data"]["id"]

    dispense = await client.post(
        "/api/v1/pharmacy/dispenses",
        json={"prescription_id": rx_id, "quantity_dispensed": 21},
        headers=headers,
    )
    assert dispense.status_code == 201, dispense.text

    listed = await client.get("/api/v1/hospital/care-events", headers=headers)
    assert listed.status_code == 200, listed.text
    body = listed.json()["data"]
    assert body["total"] == 2
    kinds = {item["event_kind"] for item in body["items"]}
    assert kinds == {"lab_result", "pharmacy_dispense"}
    for item in body["items"]:
        assert item["patient_id"] == patient_id
        assert item["encounter_id"] == encounter_id


@pytest.mark.unit
def test_hospital_staff_can_write_lab_and_pharmacy():
    from contexts.identity.domain.aggregates.role import Role

    role = Role.create_hospital_staff("hospital-demo")
    assert "laboratory.orders.write" in role.permission_ids
    assert "laboratory.results.write" in role.permission_ids
    assert "pharmacy.prescriptions.write" in role.permission_ids
    assert "pharmacy.dispenses.write" in role.permission_ids


@pytest.mark.unit
def test_clinic_staff_can_write_lab_and_pharmacy():
    from contexts.identity.domain.aggregates.role import Role

    role = Role.create_clinic_staff("clinic-demo")
    assert "laboratory.orders.write" in role.permission_ids
    assert "pharmacy.dispenses.write" in role.permission_ids
