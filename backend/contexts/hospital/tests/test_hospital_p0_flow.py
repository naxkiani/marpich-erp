"""P0 — Hospital CAP-HLT-001 acute lifecycle + tenant/Core smoke."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.audit.container import get_audit_service, reset_audit_service
from contexts.audit.infrastructure.persistence.memory_store import AuditMemoryStore
from contexts.core_platform.container import reset_platform_service
from contexts.core_platform.infrastructure.persistence.memory_store import PlatformMemoryStore
from contexts.documents.container import get_documents_service, reset_documents_service
from contexts.documents.infrastructure.persistence.memory_store import DocumentsMemoryStore
from contexts.hospital.container import reset_hospital_service
from contexts.hospital.infrastructure.persistence.memory_store import HospitalMemoryStore
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from contexts.notifications.container import get_notification_service, reset_notification_service
from contexts.notifications.infrastructure.persistence.memory_store import NotificationMemoryStore
from contexts.organization.container import get_organization_service, reset_organization_service
from contexts.organization.infrastructure.persistence.memory_store import OrganizationMemoryStore
from contexts.settings.container import get_settings_service, reset_settings_service
from contexts.settings.infrastructure.persistence.memory_store import SettingsMemoryStore
from contexts.workflow.container import get_workflow_service, reset_workflow_service
from contexts.workflow.infrastructure.persistence.memory_store import WorkflowMemoryStore
from core.presentation.api.app_factory import create_app
from core.presentation.api.startup_registry import configure_application
from shared.infrastructure.messaging.event_fabric import EventFabric


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    PlatformMemoryStore.reset()
    OrganizationMemoryStore.reset()
    SettingsMemoryStore.reset()
    NotificationMemoryStore.reset()
    AuditMemoryStore.reset()
    DocumentsMemoryStore.reset()
    WorkflowMemoryStore.reset()
    HospitalMemoryStore.reset()
    EventFabric.reset_dev_state()
    reset_platform_service()
    reset_organization_service()
    reset_settings_service()
    reset_notification_service()
    reset_audit_service()
    reset_documents_service()
    reset_workflow_service()
    reset_hospital_service()
    get_documents_service()
    get_organization_service()
    get_settings_service()
    get_notification_service()
    get_audit_service()
    get_workflow_service()
    yield


@pytest.fixture
async def client():
    application = create_app(profile="industry", startup_mode="lazy")
    configure_application(application, profile="industry", startup_mode="lazy")
    transport = ASGITransport(app=application)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _register_login(client: AsyncClient, tenant: str, email: str) -> dict[str, str]:
    reg = await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "SecurePass123!", "display_name": "Hospital Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    assert reg.status_code in (200, 201), reg.text
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    assert login.status_code == 200, login.text
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_hospital_pack_register_admit_encounter(client):
    slug = "hospital-p0-demo"
    provision = await client.post(
        "/api/v1/platform/tenants",
        json={"name": "City Hospital", "slug": slug, "industry_pack": "hospital"},
    )
    assert provision.status_code == 201, provision.text
    assert provision.json()["data"]["industry_pack"] == "hospital"

    headers = await _register_login(client, slug, "hospital-admin@demo.dev")

    seed = await client.post("/api/v1/identity/personas/hospital/seed", headers=headers)
    assert seed.status_code == 200, seed.text

    missing = await client.get("/api/v1/hospital/patients")
    assert missing.status_code == 400

    patient = await client.post(
        "/api/v1/hospital/patients",
        json={
            "mrn": "MRN-9001",
            "first_name": "Ali",
            "last_name": "Rezaei",
            "date_of_birth": "1975-01-20",
        },
        headers=headers,
    )
    assert patient.status_code == 201, patient.text
    patient_id = patient.json()["data"]["id"]

    listed = await client.get("/api/v1/hospital/patients?limit=10", headers=headers)
    assert listed.status_code == 200
    assert listed.json()["data"]["total"] >= 1

    admission = await client.post(
        "/api/v1/hospital/admissions",
        json={"patient_id": patient_id, "ward": "ICU-1"},
        headers=headers,
    )
    assert admission.status_code == 201, admission.text
    admission_id = admission.json()["data"]["id"]

    # Acute care: encounter requires admission (no walk-in)
    walkin = await client.post(
        "/api/v1/hospital/encounters",
        json={"patient_id": patient_id},
        headers=headers,
    )
    assert walkin.status_code == 422

    encounter = await client.post(
        "/api/v1/hospital/encounters",
        json={"admission_id": admission_id},
        headers=headers,
    )
    assert encounter.status_code == 201, encounter.text
    encounter_id = encounter.json()["data"]["id"]

    complete = await client.post(
        f"/api/v1/hospital/encounters/{encounter_id}/complete",
        json={"procedure_codes": ["99223"], "diagnosis_codes": ["J18.9"]},
        headers=headers,
    )
    assert complete.status_code == 200, complete.text
    assert complete.json()["data"]["status"] == "completed"

    admissions = await client.get("/api/v1/hospital/admissions", headers=headers)
    assert admissions.status_code == 200
    assert admissions.json()["data"]["total"] >= 1

    encounters = await client.get("/api/v1/hospital/encounters", headers=headers)
    assert encounters.status_code == 200
    assert encounters.json()["data"]["total"] >= 1
