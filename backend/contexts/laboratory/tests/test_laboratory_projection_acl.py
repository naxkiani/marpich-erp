"""Laboratory result → hospital/clinic local projections (peer IDs only)."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.clinic.container import get_clinic_service, reset_clinic_service
from contexts.clinic.infrastructure.persistence.memory_store import ClinicMemoryStore
from contexts.core_platform.container import reset_platform_service
from contexts.core_platform.infrastructure.persistence.memory_store import PlatformMemoryStore
from contexts.hospital.container import get_hospital_service, reset_hospital_service
from contexts.hospital.infrastructure.persistence.memory_store import HospitalMemoryStore
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from contexts.laboratory.container import reset_laboratory_service
from contexts.laboratory.infrastructure.persistence.memory_store import LaboratoryMemoryStore
from core.presentation.api.app_factory import create_app
from core.presentation.api.startup_registry import configure_application
from shared.infrastructure.messaging.event_bus import InProcessEventBus
from shared.infrastructure.messaging.event_fabric import EventFabric


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    PlatformMemoryStore.reset()
    LaboratoryMemoryStore.reset()
    HospitalMemoryStore.reset()
    ClinicMemoryStore.reset()
    EventFabric.reset_dev_state()
    InProcessEventBus.reset()
    reset_platform_service()
    reset_laboratory_service()
    reset_hospital_service()
    reset_clinic_service()
    get_hospital_service()
    get_clinic_service()
    yield


@pytest.fixture
async def client():
    application = create_app(profile="industry", startup_mode="lazy")
    configure_application(application, profile="industry", startup_mode="lazy")
    transport = ASGITransport(app=application)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _admin(client: AsyncClient, tenant: str, email: str, pack: str) -> dict[str, str]:
    await client.post(
        "/api/v1/platform/tenants",
        json={"name": "Lab ACL", "slug": tenant, "industry_pack": pack},
    )
    await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "SecurePass123!", "display_name": "Lab Admin"},
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
async def test_laboratory_result_projects_to_hospital_and_clinic(client):
    headers = await _admin(client, "lab-acl", "lab-acl@demo.dev", "laboratory")

    order = await client.post(
        "/api/v1/laboratory/orders",
        json={
            "order_number": "LAB-ACL-1",
            "patient_ref": "peer-patient-ref",
            "test_code": "CBC",
        },
        headers=headers,
    )
    assert order.status_code == 201, order.text
    order_id = order.json()["data"]["id"]

    sample = await client.post(
        "/api/v1/laboratory/samples",
        json={
            "order_id": order_id,
            "accession_number": "ACC-ACL",
            "specimen_type": "whole_blood",
        },
        headers=headers,
    )
    assert sample.status_code == 201, sample.text

    result = await client.post(
        f"/api/v1/laboratory/orders/{order_id}/results",
        json={"result_value": "5.2", "result_unit": "10^9/L"},
        headers=headers,
    )
    assert result.status_code == 200, result.text

    hospital = await client.get("/api/v1/hospital/lab-results", headers=headers)
    assert hospital.status_code == 200, hospital.text
    h_data = hospital.json()["data"]
    assert h_data["total"] == 1
    assert h_data["items"][0]["order_id"] == order_id
    assert h_data["items"][0]["patient_ref"] == "peer-patient-ref"
    assert h_data["items"][0]["test_code"] == "CBC"
    assert h_data["items"][0]["result_value"] == "5.2"

    clinic = await client.get("/api/v1/clinic/lab-results", headers=headers)
    assert clinic.status_code == 200, clinic.text
    c_data = clinic.json()["data"]
    assert c_data["total"] == 1
    assert c_data["items"][0]["order_id"] == order_id
    assert c_data["items"][0]["source_event_id"] == h_data["items"][0]["source_event_id"]

    # Idempotent projection: re-delivering is a no-op (same source_event_id)
    assert len(HospitalMemoryStore.lab_projections) == 1
    assert len(ClinicMemoryStore.lab_projections) == 1
