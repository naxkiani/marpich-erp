"""Cross-context: Laboratory/Pharmacy events → Hospital care-event projections via ACL."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.hospital.container import get_hospital_service, reset_hospital_service
from contexts.hospital.infrastructure.persistence.memory_store import HospitalMemoryStore
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from contexts.laboratory.domain.events.integration_events import ResultAvailableIntegration
from contexts.pharmacy.domain.events.integration_events import DispenseCompletedIntegration
from core.presentation.api.app_factory import create_app
from core.presentation.api.startup_registry import configure_application
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.messaging.event_bus import InProcessEventBus
from shared.infrastructure.messaging.event_fabric import EventFabric


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    HospitalMemoryStore.reset()
    InProcessEventBus.reset()
    EventFabric.reset_dev_state()
    reset_hospital_service()
    get_hospital_service()  # re-register ACL subscribers after bus reset
    yield
    identity_container._container = None
    InMemoryStore.reset()
    HospitalMemoryStore.reset()
    InProcessEventBus.reset()
    EventFabric.reset_dev_state()
    reset_hospital_service()


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
            "email": "admin@hospital-care.com",
            "password": "SecurePass123!",
            "display_name": "Admin",
        },
        headers={"X-Tenant-ID": tenant},
    )
    assert reg.status_code in (200, 201), reg.text
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "admin@hospital-care.com", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    assert login.status_code == 200, login.text
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_lab_and_pharmacy_events_project_care_timeline(client):
    tenant = "acme-care-events"
    headers = await _auth_headers(client, tenant)

    patient = await client.post(
        "/api/v1/hospital/patients",
        json={
            "mrn": "MRN-CARE-1",
            "first_name": "Sara",
            "last_name": "Karimi",
            "date_of_birth": "1988-03-12",
        },
        headers=headers,
    )
    assert patient.status_code == 201, patient.text
    patient_id = patient.json()["data"]["id"]

    admission = await client.post(
        "/api/v1/hospital/admissions",
        json={"patient_id": patient_id, "ward": "Ward-B"},
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

    tid = TenantId(tenant)
    order_id = UniqueId.generate()
    lab_event = ResultAvailableIntegration(
        tenant_id=tid,
        correlation_id="corr-lab-1",
        order_id=order_id,
        patient_ref=patient_id,
        test_code="CBC",
        result_value="12.4",
        result_unit="g/dL",
    )
    await EventFabric.publish(lab_event)

    dispense_id = UniqueId.generate()
    rx_id = UniqueId.generate()
    pharmacy_event = DispenseCompletedIntegration(
        tenant_id=tid,
        correlation_id="corr-rx-1",
        dispense_id=dispense_id,
        prescription_id=rx_id,
        patient_ref=patient_id,
        drug_code="AMOX500",
        quantity_dispensed=21.0,
    )
    await EventFabric.publish(pharmacy_event)

    listed = await client.get("/api/v1/hospital/care-events", headers=headers)
    assert listed.status_code == 200, listed.text
    body = listed.json()["data"]
    assert body["total"] == 2
    kinds = {item["event_kind"] for item in body["items"]}
    assert kinds == {"lab_result", "pharmacy_dispense"}

    for item in body["items"]:
        assert item["patient_id"] == patient_id
        assert item["admission_id"] == admission_id
        assert item["encounter_id"] == encounter_id

    lab = next(i for i in body["items"] if i["event_kind"] == "lab_result")
    assert lab["summary"]["test_code"] == "CBC"
    assert lab["summary"]["result_value"] == "12.4"
    assert lab["peer_id"] == str(order_id)
    assert lab["source_context"] == "laboratory"

    rx = next(i for i in body["items"] if i["event_kind"] == "pharmacy_dispense")
    assert rx["summary"]["drug_code"] == "AMOX500"
    assert rx["summary"]["quantity_dispensed"] == 21.0
    assert rx["peer_id"] == str(dispense_id)
    assert rx["source_context"] == "pharmacy"

    filtered = await client.get(
        f"/api/v1/hospital/care-events?encounter_id={encounter_id}",
        headers=headers,
    )
    assert filtered.status_code == 200
    assert filtered.json()["data"]["total"] == 2


@pytest.mark.asyncio
async def test_care_event_idempotent_on_source_event_id(client):
    tenant = "acme-care-idem"
    headers = await _auth_headers(client, tenant)

    patient = await client.post(
        "/api/v1/hospital/patients",
        json={
            "mrn": "MRN-CARE-2",
            "first_name": "Nima",
            "last_name": "Ahmadi",
            "date_of_birth": "1995-07-01",
        },
        headers=headers,
    )
    patient_id = patient.json()["data"]["id"]

    tid = TenantId(tenant)
    order_id = UniqueId.generate()
    event = ResultAvailableIntegration(
        tenant_id=tid,
        correlation_id="corr-idem",
        order_id=order_id,
        patient_ref=patient_id,
        test_code="CRP",
        result_value="3.1",
        result_unit="mg/L",
    )
    await EventFabric.publish(event)
    # Re-deliver same envelope (handler idempotency + projection source_event_id)
    await InProcessEventBus.deliver(event.envelope())

    listed = await client.get("/api/v1/hospital/care-events", headers=headers)
    assert listed.status_code == 200
    assert listed.json()["data"]["total"] == 1


@pytest.mark.asyncio
async def test_unknown_patient_ref_does_not_create_projection(client):
    tenant = "acme-care-unknown"
    headers = await _auth_headers(client, tenant)

    event = ResultAvailableIntegration(
        tenant_id=TenantId(tenant),
        correlation_id="corr-unknown",
        order_id=UniqueId.generate(),
        patient_ref=str(UniqueId.generate()),
        test_code="GLU",
        result_value="95",
        result_unit="mg/dL",
    )
    await EventFabric.publish(event)

    listed = await client.get("/api/v1/hospital/care-events", headers=headers)
    assert listed.status_code == 200
    assert listed.json()["data"]["total"] == 0
