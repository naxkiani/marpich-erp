"""End-to-end: Hospital → Accounting → Finance GL via events."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.accounting.container import get_accounting_service, reset_accounting_service
from contexts.finance.container import get_finance_service, reset_finance_service
from contexts.finance.infrastructure.persistence.memory_store import FinanceMemoryStore
from contexts.accounting.infrastructure.persistence.memory_store import AccountingMemoryStore
from contexts.hospital.container import reset_hospital_service
from contexts.hospital.infrastructure.persistence.memory_store import HospitalMemoryStore
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from core.presentation.api.main import app
from shared.infrastructure.messaging.event_bus import InProcessEventBus


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    HospitalMemoryStore.reset()
    AccountingMemoryStore.reset()
    FinanceMemoryStore.reset()
    InProcessEventBus.reset()
    reset_hospital_service()
    reset_accounting_service()
    reset_finance_service()
    get_accounting_service()
    get_finance_service()
    yield
    identity_container._container = None
    InMemoryStore.reset()
    HospitalMemoryStore.reset()
    AccountingMemoryStore.reset()
    FinanceMemoryStore.reset()
    InProcessEventBus.reset()
    reset_hospital_service()
    reset_accounting_service()
    reset_finance_service()


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "admin@finance.com", "password": "SecurePass123!", "display_name": "Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "admin@finance.com", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_hospital_to_finance_gl_flow(client):
    tenant = "gl-hospital"
    headers = await _auth_headers(client, tenant)

    patient = await client.post(
        "/api/v1/hospital/patients",
        json={"mrn": "MRN-GL", "first_name": "Ali", "last_name": "Test", "date_of_birth": "1990-01-01"},
        headers=headers,
    )
    patient_id = patient.json()["data"]["id"]

    admission = await client.post(
        "/api/v1/hospital/admissions",
        json={"patient_id": patient_id, "ward": "Ward-A"},
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
        json={"procedure_codes": ["99214"]},
        headers=headers,
    )

    billing = await client.get(
        f"/api/v1/accounting/billings/by-encounter/{encounter_id}",
        headers=headers,
    )
    assert billing.status_code == 200
    billing_id = billing.json()["data"]["id"]

    journal = await client.get(
        f"/api/v1/finance/journal-entries/by-source/billing_encounter/{billing_id}",
        headers=headers,
    )
    assert journal.status_code == 200
    data = journal.json()["data"]
    assert data["source_type"] == "billing_encounter"
    assert data["total_debits"] == 200.0
    assert data["total_credits"] == 200.0

    trial = await client.get("/api/v1/finance/trial-balance", headers=headers)
    assert trial.status_code == 200
    tb = trial.json()["data"]
    ar = next(a for a in tb["accounts"] if a["code"] == "1200")
    revenue = next(a for a in tb["accounts"] if a["code"] == "4000")
    assert ar["balance"] == 200.0
    assert revenue["balance"] == 200.0


@pytest.mark.asyncio
async def test_open_and_close_fiscal_period(client):
    tenant = "period-test"
    headers = await _auth_headers(client, tenant)

    opened = await client.post(
        "/api/v1/finance/fiscal-periods",
        json={"name": "Q1 2025", "start_date": "2025-01-01", "end_date": "2025-03-31"},
        headers=headers,
    )
    assert opened.status_code == 201
    period_id = opened.json()["data"]["id"]

    closed = await client.post(
        f"/api/v1/finance/fiscal-periods/{period_id}/close",
        headers=headers,
    )
    assert closed.status_code == 200
    assert closed.json()["data"]["status"] == "closed"
