"""P0 — Clinic CAP-HLT-002/003 + tenant/Core smoke (industry pack clinic)."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.audit.container import get_audit_service, reset_audit_service
from contexts.audit.infrastructure.persistence.memory_store import AuditMemoryStore
from contexts.clinic.container import reset_clinic_service
from contexts.clinic.infrastructure.persistence.memory_store import ClinicMemoryStore
from contexts.core_platform.container import reset_platform_service
from contexts.core_platform.infrastructure.persistence.memory_store import PlatformMemoryStore
from contexts.documents.container import get_documents_service, reset_documents_service
from contexts.documents.infrastructure.persistence.memory_store import DocumentsMemoryStore
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
    ClinicMemoryStore.reset()
    EventFabric.reset_dev_state()
    reset_platform_service()
    reset_organization_service()
    reset_settings_service()
    reset_notification_service()
    reset_audit_service()
    reset_documents_service()
    reset_workflow_service()
    reset_clinic_service()
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


async def _register_login(
    client: AsyncClient, tenant: str, email: str, display_name: str = "Clinic User"
) -> dict[str, str]:
    reg = await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "SecurePass123!", "display_name": display_name},
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
async def test_clinic_pack_patient_walkin_encounter_and_core_smoke(client):
    slug = "clinic-p0-demo"
    provision = await client.post(
        "/api/v1/platform/tenants",
        json={"name": "City Clinic", "slug": slug, "industry_pack": "clinic"},
    )
    assert provision.status_code == 201, provision.text
    assert provision.json()["data"]["industry_pack"] == "clinic"

    headers = await _register_login(client, slug, "clinic-admin@demo.dev")

    seed = await client.post("/api/v1/identity/personas/clinic/seed", headers=headers)
    assert seed.status_code == 200, seed.text
    assert "clinic_staff" in seed.json()["data"]["created"] or seed.json()["data"][
        "clinic_staff_role_id"
    ]

    missing = await client.get("/api/v1/clinic/patients")
    assert missing.status_code == 400

    patient = await client.post(
        "/api/v1/clinic/patients",
        json={
            "patient_number": "CLN-2001",
            "first_name": "Sara",
            "last_name": "Ahmadi",
            "date_of_birth": "1988-03-12",
        },
        headers=headers,
    )
    assert patient.status_code == 201, patient.text
    patient_id = patient.json()["data"]["id"]

    listed = await client.get("/api/v1/clinic/patients?limit=10", headers=headers)
    assert listed.status_code == 200, listed.text
    assert listed.json()["data"]["total"] >= 1
    assert any(p["id"] == patient_id for p in listed.json()["data"]["items"])

    encounter = await client.post(
        "/api/v1/clinic/encounters",
        json={"patient_id": patient_id},
        headers=headers,
    )
    assert encounter.status_code == 201, encounter.text
    encounter_id = encounter.json()["data"]["id"]
    assert encounter.json()["data"]["appointment_id"] is None

    complete = await client.post(
        f"/api/v1/clinic/encounters/{encounter_id}/complete",
        json={"diagnosis_codes": ["J06.9"]},
        headers=headers,
    )
    assert complete.status_code == 200, complete.text
    assert complete.json()["data"]["status"] == "completed"

    encounters = await client.get("/api/v1/clinic/encounters", headers=headers)
    assert encounters.status_code == 200
    assert encounters.json()["data"]["total"] >= 1

    # Core Document Exchange smoke (chart reference pattern)
    root = await client.get("/api/v1/documents/folders/root", headers=headers)
    assert root.status_code == 200, root.text
    root_id = root.json()["data"]["id"]
    doc = await client.post(
        "/api/v1/documents/documents",
        json={
            "folder_id": root_id,
            "title": "Visit note",
            "file_name": "note.txt",
            "content": "Outpatient visit note",
        },
        headers=headers,
    )
    assert doc.status_code == 201, doc.text
