"""Notification service — event-driven delivery tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.accounting.container import get_accounting_service, reset_accounting_service
from contexts.finance.container import get_finance_service, reset_finance_service
from contexts.notifications.container import get_notification_service, reset_notification_service
from contexts.notifications.infrastructure.persistence.memory_store import NotificationMemoryStore
from contexts.hospital.container import reset_hospital_service
from contexts.hospital.infrastructure.persistence.memory_store import HospitalMemoryStore
from contexts.accounting.infrastructure.persistence.memory_store import AccountingMemoryStore
from contexts.finance.infrastructure.persistence.memory_store import FinanceMemoryStore
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from core.presentation.api.app_factory import create_app
from core.presentation.api.startup_registry import configure_application
from shared.infrastructure.messaging.event_bus import InProcessEventBus


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    HospitalMemoryStore.reset()
    AccountingMemoryStore.reset()
    FinanceMemoryStore.reset()
    NotificationMemoryStore.reset()
    InProcessEventBus.reset()
    reset_hospital_service()
    reset_accounting_service()
    reset_finance_service()
    reset_notification_service()
    get_accounting_service()
    get_finance_service()
    get_notification_service()
    yield


@pytest.fixture
async def client():
    application = create_app(profile="industry", startup_mode="lazy")
    configure_application(application, profile="industry", startup_mode="lazy")
    transport = ASGITransport(app=application)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str, email: str = "user@notify.dev") -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "SecurePass123!", "display_name": "Notify User"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_register_creates_welcome_inbox(client):
    tenant = "notify-hospital"
    headers = await _auth_headers(client, tenant)

    inbox = await client.get("/api/v1/notifications/inbox", headers=headers)
    assert inbox.status_code == 200
    messages = inbox.json()["data"]
    assert len(messages) >= 1
    welcome = next(m for m in messages if m["category"] == "onboarding")
    assert "Welcome" in welcome["title"]
    assert welcome["status"] == "unread"


@pytest.mark.asyncio
async def test_mark_inbox_read(client):
    tenant = "notify-read"
    headers = await _auth_headers(client, tenant, email="read@notify.dev")

    inbox = await client.get("/api/v1/notifications/inbox", headers=headers)
    message_id = inbox.json()["data"][0]["id"]

    read = await client.patch(f"/api/v1/notifications/inbox/{message_id}/read", headers=headers)
    assert read.status_code == 200
    assert read.json()["data"]["status"] == "read"


@pytest.mark.asyncio
async def test_manual_send_notification(client):
    tenant = "notify-send"
    headers = await _auth_headers(client, tenant, email="send@notify.dev")

    sent = await client.post(
        "/api/v1/notifications/send",
        json={"channel": "inbox", "title": "Test", "body": "Hello team", "user_id": None},
        headers=headers,
    )
    assert sent.status_code == 202

    inbox = await client.get("/api/v1/notifications/inbox", headers=headers)
    titles = [m["title"] for m in inbox.json()["data"]]
    assert "Test" in titles


@pytest.mark.asyncio
async def test_hospital_flow_creates_encounter_notification(client):
    tenant = "notify-clinical"
    headers = await _auth_headers(client, tenant, email="clinical@notify.dev")

    patient = await client.post(
        "/api/v1/hospital/patients",
        json={"mrn": "MRN-N1", "first_name": "Ali", "last_name": "N", "date_of_birth": "1990-01-01"},
        headers=headers,
    )
    patient_id = patient.json()["data"]["id"]

    admission = await client.post(
        "/api/v1/hospital/admissions",
        json={"patient_id": patient_id, "ward": "Ward-1"},
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

    inbox = await client.get("/api/v1/notifications/inbox", headers=headers)
    categories = [m["category"] for m in inbox.json()["data"]]
    assert "healthcare" in categories
