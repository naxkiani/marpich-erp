"""Cross-context integration: Hospital encounter → Accounting billing via events."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.accounting.container import get_accounting_service, reset_accounting_service
from contexts.accounting.infrastructure.persistence.memory_store import AccountingMemoryStore
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
    HospitalMemoryStore.reset()
    AccountingMemoryStore.reset()
    InProcessEventBus.reset()
    EventFabric.reset_dev_state()
    reset_hospital_service()
    reset_accounting_service()
    get_accounting_service()  # re-register ACL subscribers after bus reset
    yield
    identity_container._container = None
    InMemoryStore.reset()
    HospitalMemoryStore.reset()
    AccountingMemoryStore.reset()
    InProcessEventBus.reset()
    EventFabric.reset_dev_state()
    reset_hospital_service()
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
            "email": "admin@hospital.com",
            "password": "SecurePass123!",
            "display_name": "Admin",
        },
        headers={"X-Tenant-ID": tenant},
    )
    assert reg.status_code in (200, 201), reg.text
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "admin@hospital.com", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    assert login.status_code == 200, login.text
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_hospital_to_accounting_event_flow(client):
    tenant = "acme-hospital"
    headers = await _auth_headers(client, tenant)

    # Register patient
    patient = await client.post(
        "/api/v1/hospital/patients",
        json={
            "mrn": "MRN-001",
            "first_name": "Ali",
            "last_name": "Rezaei",
            "date_of_birth": "1990-05-15",
        },
        headers=headers,
    )
    assert patient.status_code == 201
    patient_id = patient.json()["data"]["id"]

    # Admit
    admission = await client.post(
        "/api/v1/hospital/admissions",
        json={"patient_id": patient_id, "ward": "ICU-A"},
        headers=headers,
    )
    assert admission.status_code == 201
    admission_id = admission.json()["data"]["id"]

    # Start encounter
    encounter = await client.post(
        "/api/v1/hospital/encounters",
        json={"admission_id": admission_id},
        headers=headers,
    )
    assert encounter.status_code == 201
    encounter_id = encounter.json()["data"]["id"]

    # Complete encounter → publishes hospital.encounter.completed
    complete = await client.post(
        f"/api/v1/hospital/encounters/{encounter_id}/complete",
        json={"procedure_codes": ["99214", "80053"], "diagnosis_codes": ["J06.9"]},
        headers=headers,
    )
    assert complete.status_code == 200
    assert complete.json()["data"]["status"] == "completed"

    # Accounting receives event via ACL — no direct import
    billing = await client.get(
        f"/api/v1/accounting/billings/by-encounter/{encounter_id}",
        headers=headers,
    )
    assert billing.status_code == 200
    data = billing.json()["data"]
    assert data["external_encounter_id"] == encounter_id
    assert data["patient_ref"] == patient_id
    assert data["total_amount"] == 285.0  # 99214=200 + 80053=85
    assert data["status"] == "posted"


@pytest.mark.asyncio
async def test_accounting_idempotent_on_duplicate_event(client):
    tenant = "dup-hospital"
    headers = await _auth_headers(client, tenant)

    patient = await client.post(
        "/api/v1/hospital/patients",
        json={"mrn": "MRN-002", "first_name": "Sara", "last_name": "Ahmadi", "date_of_birth": "1985-01-01"},
        headers=headers,
    )
    patient_id = patient.json()["data"]["id"]

    admission = await client.post(
        "/api/v1/hospital/admissions",
        json={"patient_id": patient_id, "ward": "Ward-B"},
        headers=headers,
    )
    admission_id = admission.json()["data"]["id"]

    encounter = await client.post(
        "/api/v1/hospital/encounters",
        json={"admission_id": admission_id},
        headers=headers,
    )
    encounter_id = encounter.json()["data"]["id"]

    await client.post(
        f"/api/v1/hospital/encounters/{encounter_id}/complete",
        json={"procedure_codes": ["99213"]},
        headers=headers,
    )

    billings = await client.get("/api/v1/accounting/billings", headers=headers)
    assert billings.status_code == 200, billings.text
    payload = billings.json()["data"]
    items = payload["items"] if isinstance(payload, dict) and "items" in payload else payload
    assert len(items) == 1
