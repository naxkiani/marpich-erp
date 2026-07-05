"""Enterprise financial validation engine tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.financial_kernel.container import get_financial_kernel_service, reset_financial_kernel_service
from contexts.financial_kernel.domain.services.financial_validation_engine import (
    VALIDATION_CATALOG,
    FinancialValidationContext,
    build_validation_report,
    reject_if_invalid,
    run_financial_validation,
    run_full_validation,
    validate_balanced_journals,
    validate_currency,
    validate_duplicate_posting,
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
        json={"email": "val@kernel.dev", "password": "SecurePass123!", "display_name": "Val Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "val@kernel.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


async def _provision_hospital(slug: str) -> dict[str, str]:
    svc = get_financial_kernel_service()
    await svc.handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {"industry_pack": "hospital"}}
    )
    periods = (await svc.list_periods(slug)).unwrap()
    return {
        "period_id": periods[0]["id"],
        "ar": (await svc.resolve_account_code(slug, "patient_receivables")).unwrap(),
        "rev": (await svc.resolve_account_code(slug, "patient_service_revenue")).unwrap(),
        "cash": (await svc.resolve_account_code(slug, "cash")).unwrap(),
        "expense": (await svc.resolve_account_code(slug, "clinical_staff")).unwrap(),
    }


def test_validation_catalog_has_eleven_checks():
    assert len(VALIDATION_CATALOG) == 11
    checks = set(VALIDATION_CATALOG.keys())
    assert "balanced_journals" in checks
    assert "posting_permissions" in checks
    assert "fiscal_period" in checks
    assert "dimension_rules" in checks
    assert "business_rules" in checks


def test_balanced_journals_rejects_unbalanced():
    lines = [
        {"account_code": "1000", "debit": 100, "credit": 0},
        {"account_code": "4000", "debit": 0, "credit": 50},
    ]
    result = validate_balanced_journals(lines)
    assert not result.valid


def test_currency_validation_rejects_zero_rate():
    result = validate_currency(currency="USD", base_currency="EUR", exchange_rate=0)
    assert not result.valid


def test_duplicate_posting_detected():
    result = validate_duplicate_posting(duplicate_exists=True, idempotency_key="ctx:doc-1")
    assert not result.valid


def test_build_validation_report_and_reject():
    ctx = FinancialValidationContext(tenant_id="t1", user_permissions=["*"])
    lines = [
        {"account_code": "1000", "debit": 100, "credit": 0},
        {"account_code": "4000", "debit": 0, "credit": 50},
    ]
    check_results = run_financial_validation(lines, context=ctx)
    report = build_validation_report(check_results)
    assert report["valid"] is False
    assert report["can_post"] is False
    assert report["summary"]["failed_checks"] >= 1
    ok, err = reject_if_invalid(report)
    assert ok is False
    assert "validation" in err


@pytest.mark.asyncio
async def test_validate_balanced_transaction(client):
    slug = "val-balanced"
    headers = await _auth_headers(client, slug)
    ctx = await _provision_hospital(slug)

    resp = await client.post(
        "/api/v1/financial-kernel/validation/validate",
        headers=headers,
        json={
            "source_context": "manual",
            "source_document_id": "val-001",
            "period_id": ctx["period_id"],
            "lines": [
                {"account_code": ctx["ar"], "debit": 200, "credit": 0},
                {"account_code": ctx["rev"], "debit": 0, "credit": 200},
            ],
        },
    )
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["report"]["can_post"] is True
    assert data["rejected"] is False
    assert data["report"]["summary"]["passed_checks"] == 11


@pytest.mark.asyncio
async def test_validate_rejects_unbalanced(client):
    slug = "val-unbalanced"
    headers = await _auth_headers(client, slug)
    ctx = await _provision_hospital(slug)

    resp = await client.post(
        "/api/v1/financial-kernel/validation/validate",
        headers=headers,
        json={
            "source_context": "manual",
            "source_document_id": "val-bad",
            "period_id": ctx["period_id"],
            "lines": [
                {"account_code": ctx["ar"], "debit": 100, "credit": 0},
                {"account_code": ctx["rev"], "debit": 0, "credit": 50},
            ],
        },
    )
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["report"]["can_post"] is False
    assert data["rejected"] is True
    failed = [c for c in data["report"]["checks"] if not c["passed"]]
    assert any(c["check"] == "balanced_journals" for c in failed)


@pytest.mark.asyncio
async def test_post_rejects_invalid_transaction(client):
    slug = "val-reject-post"
    headers = await _auth_headers(client, slug)
    ctx = await _provision_hospital(slug)

    post = await client.post(
        "/api/v1/financial-kernel/journals",
        headers=headers,
        json={
            "source_context": "manual",
            "source_document_id": "reject-001",
            "lines": [
                {"account_code": ctx["expense"], "debit": 100, "credit": 0},
                {"account_code": ctx["cash"], "debit": 0, "credit": 50},
            ],
        },
    )
    assert post.status_code == 400
    assert "validation" in post.json()["detail"].lower() or "journal" in post.json()["detail"].lower()


@pytest.mark.asyncio
async def test_validation_run_history_and_audit(client):
    slug = "val-audit"
    headers = await _auth_headers(client, slug)
    ctx = await _provision_hospital(slug)

    resp = await client.post(
        "/api/v1/financial-kernel/validation/validate",
        headers=headers,
        json={
            "source_context": "manual",
            "source_document_id": "val-audit-1",
            "period_id": ctx["period_id"],
            "lines": [
                {"account_code": ctx["ar"], "debit": 50, "credit": 0},
                {"account_code": ctx["rev"], "debit": 0, "credit": 50},
            ],
        },
    )
    run_id = resp.json()["data"]["validation_run_id"]

    run = await client.get(
        f"/api/v1/financial-kernel/validation/runs/{run_id}",
        headers=headers,
    )
    assert run.status_code == 200
    assert run.json()["data"]["can_post"] is True

    audit = await client.get(
        f"/api/v1/financial-kernel/validation/runs/{run_id}/audit",
        headers=headers,
    )
    assert audit.status_code == 200
    assert audit.json()["data"][0]["action"] == "validated"

    listed = await client.get(
        "/api/v1/financial-kernel/validation/runs",
        headers=headers,
    )
    assert listed.status_code == 200
    assert len(listed.json()["data"]) >= 1


@pytest.mark.asyncio
async def test_dimension_rules_in_validation_report(client):
    slug = "val-dim"
    headers = await _auth_headers(client, slug)
    ctx = await _provision_hospital(slug)
    svc = get_financial_kernel_service()
    await svc.create_dimension_value(
        tenant_id=slug,
        dimension_type="cost_center",
        code="CC-VALID",
        name="Valid Center",
    )

    resp = await client.post(
        "/api/v1/financial-kernel/validation/validate",
        headers=headers,
        json={
            "source_context": "manual",
            "source_document_id": "val-dim-1",
            "period_id": ctx["period_id"],
            "lines": [
                {
                    "account_code": ctx["expense"],
                    "debit": 25,
                    "credit": 0,
                    "cost_center": "CC-BAD",
                },
                {"account_code": ctx["cash"], "debit": 0, "credit": 25},
            ],
        },
    )
    data = resp.json()["data"]
    assert data["report"]["can_post"] is False
    dim_check = next(c for c in data["report"]["checks"] if c["check"] == "dimension_rules")
    assert dim_check["passed"] is False
