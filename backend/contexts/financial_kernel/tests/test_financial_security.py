"""Enterprise Financial Security tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.financial_kernel.container import (
    get_financial_kernel_service,
    get_financial_security_service,
    reset_financial_kernel_service,
)
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from core.presentation.api.main import app


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    reset_financial_kernel_service()
    get_financial_security_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "sec@kernel.dev", "password": "SecurePass123!", "display_name": "Sec Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "sec@kernel.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_maker_checker_and_four_eyes(client):
    slug = "sec-mc"
    headers = await _auth_headers(client, slug)
    svc = get_financial_security_service()

    submit = await client.post(
        "/api/v1/financial-kernel/security/maker-checker",
        headers=headers,
        json={
            "control_type": "maker_checker",
            "resource_type": "journal",
            "resource_id": "j-1",
            "payload": {"amount": 5000},
            "checker_id": "checker-1",
        },
    )
    assert submit.status_code == 201
    req_id = submit.json()["data"]["id"]
    maker_id = submit.json()["data"]["maker_id"]
    assert submit.json()["data"]["encrypted_payload"]

    self_approve = await svc.approve_maker_checker(
        tenant_id=slug, request_id=req_id, approver_id=maker_id
    )
    assert not self_approve.succeeded

    approve = await svc.approve_maker_checker(
        tenant_id=slug, request_id=req_id, approver_id="checker-1"
    )
    assert approve.succeeded
    assert approve.unwrap()["status"] == "approved"
    assert approve.unwrap()["signature"]["algorithm"] == "RS256"


@pytest.mark.asyncio
async def test_dual_approval_four_eyes(client):
    slug = "sec-dual"
    headers = await _auth_headers(client, slug)
    svc = get_financial_security_service()

    submit = await client.post(
        "/api/v1/financial-kernel/security/maker-checker",
        headers=headers,
        json={
            "control_type": "four_eyes",
            "resource_type": "payment",
            "resource_id": "pay-1",
            "payload": {"amount": 10000},
        },
    )
    req_id = submit.json()["data"]["id"]

    first = await svc.approve_maker_checker(
        tenant_id=slug, request_id=req_id, approver_id="approver-1"
    )
    assert first.succeeded
    assert first.unwrap()["status"] == "first_approved"

    second = await svc.approve_maker_checker(
        tenant_id=slug, request_id=req_id, approver_id="approver-2"
    )
    assert second.succeeded
    assert second.unwrap()["status"] == "approved"


@pytest.mark.asyncio
async def test_transaction_lock_and_guarded_modification(client):
    slug = "sec-lock"
    headers = await _auth_headers(client, slug)

    lock = await client.post(
        "/api/v1/financial-kernel/security/locks",
        headers=headers,
        json={"resource_type": "journal", "resource_id": "j-99", "reason": "audit_review"},
    )
    assert lock.status_code == 201
    lock_id = lock.json()["data"]["id"]

    blocked = await client.post(
        "/api/v1/financial-kernel/security/guarded-modification",
        headers=headers,
        json={
            "resource_type": "journal",
            "resource_id": "j-99",
            "action": "update",
            "payload": {"amount": 100},
        },
    )
    assert blocked.status_code == 400

    release = await client.post(
        f"/api/v1/financial-kernel/security/locks/{lock_id}/release",
        headers=headers,
    )
    assert release.status_code == 200

    modify = await client.post(
        "/api/v1/financial-kernel/security/guarded-modification",
        headers=headers,
        json={
            "resource_type": "journal",
            "resource_id": "j-99",
            "action": "update",
            "payload": {"amount": 100},
        },
    )
    assert modify.status_code == 200
    assert modify.json()["data"]["audited"] is True


@pytest.mark.asyncio
async def test_rbac_abac_and_audit_tamper(client):
    slug = "sec-policy"
    headers = await _auth_headers(client, slug)

    await client.post(
        "/api/v1/financial-kernel/security/policies",
        headers=headers,
        json={
            "name": "Journal RBAC",
            "policy_type": "rbac",
            "resource_type": "journal",
            "rules": {
                "allowed_roles": ["finance_admin"],
                "role_permissions": {"finance_admin": ["journal.post"]},
            },
        },
    )
    await client.post(
        "/api/v1/financial-kernel/security/policies",
        headers=headers,
        json={
            "name": "Payment ABAC",
            "policy_type": "abac",
            "resource_type": "payment",
            "rules": {
                "required_attributes": {"department": ["finance", "treasury"]},
                "deny_if": {"risk_level": "high"},
            },
        },
    )

    rbac = await client.post(
        "/api/v1/financial-kernel/security/policies/evaluate",
        headers=headers,
        json={"resource_type": "journal", "permission": "journal.post", "role": "finance_admin"},
    )
    assert rbac.json()["data"]["allowed"] is True

    abac = await client.post(
        "/api/v1/financial-kernel/security/policies/evaluate",
        headers=headers,
        json={
            "resource_type": "payment",
            "permission": "payment.approve",
            "attributes": {"department": "finance", "risk_level": "low"},
        },
    )
    assert abac.json()["data"]["allowed"] is True

    audit = await client.get("/api/v1/financial-kernel/security/audit", headers=headers)
    assert audit.status_code == 200
    assert len(audit.json()["data"]) >= 2

    audit_id = audit.json()["data"][0]["id"]
    verify = await client.get(
        f"/api/v1/financial-kernel/security/audit/{audit_id}/verify-tamper",
        headers=headers,
    )
    assert verify.status_code == 200
    assert verify.json()["data"]["valid"] is True


@pytest.mark.asyncio
async def test_period_and_fiscal_year_close_dual_approval(client):
    slug = "sec-close"
    headers = await _auth_headers(client, slug)
    sec = get_financial_security_service()

    svc = get_financial_kernel_service()
    await svc.handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {"industry_pack": "hospital"}}
    )
    periods = (await svc.list_periods(slug)).unwrap()
    period_id = periods[0]["id"]
    year_id = periods[0]["fiscal_year_id"]

    close_req = await client.post(
        "/api/v1/financial-kernel/security/period-close",
        headers=headers,
        json={"close_type": "period", "target_id": period_id},
    )
    assert close_req.status_code == 201
    req_id = close_req.json()["data"]["id"]

    first = await sec.approve_period_close(
        tenant_id=slug, request_id=req_id, approver_id="close-approver-1"
    )
    assert first.succeeded
    assert first.unwrap()["status"] == "first_approved"

    second = await sec.approve_period_close(
        tenant_id=slug, request_id=req_id, approver_id="close-approver-2"
    )
    assert second.succeeded
    assert second.unwrap()["status"] == "approved"

    period = (await svc.list_periods(slug)).unwrap()
    assert any(p["id"] == period_id and p["status"] == "closed" for p in period)

    fy_close = await client.post(
        "/api/v1/financial-kernel/security/period-close",
        headers=headers,
        json={"close_type": "fiscal_year", "target_id": year_id},
    )
    assert fy_close.status_code == 201
