"""Enterprise fiscal calendar tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.financial_kernel.container import get_financial_kernel_service, reset_financial_kernel_service
from contexts.financial_kernel.domain.aggregates.fiscal_calendar import CloseActionType
from contexts.financial_kernel.domain.services.fiscal_calendar_engine import (
    build_closing_assistant,
    generate_ai_closing_checklist,
    validate_period_for_posting,
)
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from core.presentation.api.main import app


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    reset_financial_kernel_service()
    get_financial_kernel_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "fiscal@kernel.dev", "password": "SecurePass123!", "display_name": "Fiscal Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "fiscal@kernel.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


def test_soft_close_allows_adjustments():
    ok, _ = validate_period_for_posting(
        period_status="soft_closed", journal_entry_type="adjusting"
    )
    assert ok is True


def test_hard_close_blocks_posting():
    ok, code = validate_period_for_posting(period_status="hard_closed")
    assert ok is False
    assert code == "period_closed"


def test_closing_assistant_and_ai_checklist():
    period = {"id": "p1", "name": "P01", "status": "open", "accepts_adjustments": True}
    trial = [{"debit_balance": 100, "credit_balance": 100}]
    assistant = build_closing_assistant(
        period=period, trial_balance=trial, journal_count=2, unposted_count=0
    )
    assert assistant["ready_for_close"] is True
    assert len(assistant["steps"]) == 6

    checklist = generate_ai_closing_checklist(
        period=period, trial_balance=trial, journals=[], unposted_count=0
    )
    assert checklist["recommendation"] == "proceed"


@pytest.mark.asyncio
async def test_create_calendar_and_generate_periods(client):
    slug = "fiscal-cal"
    headers = await _auth_headers(client, slug)

    cal = await client.post(
        "/api/v1/financial-kernel/fiscal-calendar/calendars",
        headers=headers,
        json={"name": "Hospital Calendar", "is_default": True},
    )
    assert cal.status_code == 201
    calendar_id = cal.json()["data"]["id"]

    year = await client.post(
        f"/api/v1/financial-kernel/fiscal-calendar/calendars/{calendar_id}/fiscal-years",
        headers=headers,
        json={"name": "FY2026", "start_date": "2026-01-01", "end_date": "2026-12-31"},
    )
    assert year.status_code == 201
    year_id = year.json()["data"]["id"]

    periods = await client.post(
        f"/api/v1/financial-kernel/fiscal-calendar/fiscal-years/{year_id}/generate-periods",
        headers=headers,
    )
    assert periods.status_code == 201
    assert len(periods.json()["data"]) == 12


@pytest.mark.asyncio
async def test_soft_close_with_dual_approval(client):
    slug = "fiscal-close"
    svc = get_financial_kernel_service()
    await svc.handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {"industry_pack": "hospital"}}
    )
    headers = await _auth_headers(client, slug)
    period_id = (await svc.list_periods(slug)).unwrap()[0]["id"]

    req = await client.post(
        f"/api/v1/financial-kernel/fiscal-calendar/periods/{period_id}/close-request",
        headers=headers,
        json={"action_type": CloseActionType.MONTHLY_CLOSE.value, "reason": "month end"},
    )
    assert req.status_code == 201
    request_id = req.json()["data"]["id"]

    first = await svc.approve_period_close_action(
        tenant_id=slug, request_id=request_id, approver_id="approver-1"
    )
    assert first.succeeded
    assert first.unwrap()["status"] == "first_approved"

    second = await svc.approve_period_close_action(
        tenant_id=slug, request_id=request_id, approver_id="approver-2"
    )
    assert second.succeeded
    period = (await svc.list_periods(slug)).unwrap()[0]
    assert period["status"] == "soft_closed"
    assert period["is_financially_locked"] is True


@pytest.mark.asyncio
async def test_closing_assistant_api(client):
    slug = "fiscal-assist"
    svc = get_financial_kernel_service()
    await svc.handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {"industry_pack": "hospital"}}
    )
    headers = await _auth_headers(client, slug)
    period_id = (await svc.list_periods(slug)).unwrap()[0]["id"]

    assistant = await client.get(
        f"/api/v1/financial-kernel/fiscal-calendar/periods/{period_id}/closing-assistant",
        headers=headers,
    )
    assert assistant.status_code == 200
    assert "steps" in assistant.json()["data"]

    checklist = await client.get(
        f"/api/v1/financial-kernel/fiscal-calendar/periods/{period_id}/ai-closing-checklist",
        headers=headers,
    )
    assert checklist.status_code == 200
    assert "items" in checklist.json()["data"]
