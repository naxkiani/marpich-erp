"""Enterprise reconciliation engine tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.financial_kernel.container import get_financial_kernel_service, reset_financial_kernel_service
from contexts.financial_kernel.domain.services.reconciliation_engine import (
    RECONCILIATION_CATALOG,
    automatic_match_items,
    build_difference_analysis,
    build_exception_queue,
    generate_ai_suggestions,
    validate_approval_action,
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
        json={"email": "rec@kernel.dev", "password": "SecurePass123!", "display_name": "Recon Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "rec@kernel.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


def test_reconciliation_catalog_has_all_types():
    assert len(RECONCILIATION_CATALOG) == 5
    types = set(RECONCILIATION_CATALOG.keys())
    assert types == {"bank", "cash", "intercompany", "subledger", "general_ledger"}


def test_automatic_match_by_reference_and_amount():
    left = [
        {"reference": "TXN-001", "amount": 100.0},
        {"reference": "TXN-002", "amount": 50.0},
    ]
    right = [
        {"reference": "TXN-001", "amount": 100.0},
        {"reference": "TXN-999", "amount": 25.0},
    ]
    matched, unmatched_left, unmatched_right = automatic_match_items(left, right)
    assert len(matched) == 1
    assert matched[0]["left"]["reference"] == "TXN-001"
    assert len(unmatched_left) == 1
    assert unmatched_left[0]["reference"] == "TXN-002"
    assert len(unmatched_right) == 1


def test_difference_analysis_and_exceptions():
    matched = [{"left": {"amount": 100}, "right": {"amount": 100}}]
    unmatched_left = [{"amount": 50, "reference": "A"}]
    unmatched_right = [{"amount": 25, "reference": "B"}]
    analysis = build_difference_analysis(
        left_total=150.0,
        right_total=125.0,
        matched_pairs=matched,
        unmatched_left=unmatched_left,
        unmatched_right=unmatched_right,
    )
    assert analysis["variance"] == -25.0
    assert analysis["balanced"] is False
    exceptions = build_exception_queue(
        unmatched_left=unmatched_left,
        unmatched_right=unmatched_right,
        variance=analysis["variance"],
    )
    assert len(exceptions) == 3


def test_ai_suggestions_for_variance():
    analysis = {"variance": 10.0, "match_rate": 0.5}
    suggestions = generate_ai_suggestions(
        reconciliation_type="bank",
        difference_analysis=analysis,
        exceptions=[{"reason": "variance_detected"}],
        unmatched_left=[{"amount": 10}],
        unmatched_right=[],
    )
    assert any(s["category"] == "variance" for s in suggestions)


def test_approval_validation():
    ok, _ = validate_approval_action(current_status="matched", action="submit")
    assert ok is True
    ok, reason = validate_approval_action(current_status="matched", action="approve")
    assert ok is False
    assert reason == "not_pending_approval"


@pytest.mark.asyncio
async def test_bank_reconciliation_end_to_end(client):
    slug = "rec-bank"
    headers = await _auth_headers(client, slug)

    catalog = await client.get(
        "/api/v1/financial-kernel/reconciliation/catalog", headers=headers
    )
    assert catalog.status_code == 200
    assert len(catalog.json()["data"]) == 5

    create = await client.post(
        "/api/v1/financial-kernel/reconciliation/runs",
        headers=headers,
        json={
            "reconciliation_type": "bank",
            "reconciliation_date": "2025-06-30",
            "reference_label": "Main Operating Account",
            "left_items": [
                {"reference": "DEP-100", "amount": 1000.0},
                {"reference": "CHK-200", "amount": -200.0},
            ],
            "right_items": [
                {"reference": "DEP-100", "amount": 1000.0},
                {"reference": "FEE-001", "amount": -5.0},
            ],
        },
    )
    assert create.status_code == 201
    run = create.json()["data"]
    run_id = run["id"]
    assert run["reconciliation_type"] == "bank"
    assert len(run["matched_pairs"]) == 1
    assert len(run["exceptions"]) >= 2

    manual = await client.post(
        f"/api/v1/financial-kernel/reconciliation/runs/{run_id}/manual-match",
        headers=headers,
        json={
            "left_item": {"reference": "CHK-200", "amount": -200.0},
            "right_item": {"reference": "FEE-001", "amount": -5.0},
        },
    )
    assert manual.status_code == 200
    assert len(manual.json()["data"]["matched_pairs"]) == 2

    report = await client.get(
        f"/api/v1/financial-kernel/reconciliation/runs/{run_id}/report",
        headers=headers,
    )
    assert report.status_code == 200
    assert "summary" in report.json()["data"]

    submit = await client.post(
        f"/api/v1/financial-kernel/reconciliation/runs/{run_id}/submit",
        headers=headers,
    )
    assert submit.status_code == 200
    assert submit.json()["data"]["status"] == "pending_approval"

    approve = await client.post(
        f"/api/v1/financial-kernel/reconciliation/runs/{run_id}/approve",
        headers=headers,
    )
    assert approve.status_code == 200
    assert approve.json()["data"]["status"] == "approved"

    audit = await client.get(
        f"/api/v1/financial-kernel/reconciliation/runs/{run_id}/audit",
        headers=headers,
    )
    assert audit.status_code == 200
    actions = [e["action"] for e in audit.json()["data"]]
    assert "created" in actions
    assert "manual_match" in actions
    assert "submit" in actions
    assert "approve" in actions


@pytest.mark.asyncio
async def test_cash_reconciliation_auto_match_balanced(client):
    slug = "rec-cash"
    headers = await _auth_headers(client, slug)
    create = await client.post(
        "/api/v1/financial-kernel/reconciliation/runs",
        headers=headers,
        json={
            "reconciliation_type": "cash",
            "reconciliation_date": "2025-06-30",
            "reference_label": "Petty Cash Drawer",
            "left_items": [{"reference": "COUNT-1", "amount": 500.0}],
            "right_items": [{"reference": "BOOK-1", "amount": 500.0}],
        },
    )
    assert create.status_code == 201
    run = create.json()["data"]
    assert run["status"] == "matched"
    assert run["difference_analysis"]["balanced"] is True


@pytest.mark.asyncio
async def test_intercompany_reconciliation_ai_suggestions(client):
    slug = "rec-ic"
    headers = await _auth_headers(client, slug)
    create = await client.post(
        "/api/v1/financial-kernel/reconciliation/runs",
        headers=headers,
        json={
            "reconciliation_type": "intercompany",
            "reconciliation_date": "2025-06-30",
            "reference_label": "Entity A vs Entity B",
            "left_items": [{"reference": "IC-001", "amount": 10000.0}],
            "right_items": [{"reference": "IC-001", "amount": 9500.0}],
            "auto_match": False,
        },
    )
    assert create.status_code == 201
    run_id = create.json()["data"]["id"]

    auto = await client.post(
        f"/api/v1/financial-kernel/reconciliation/runs/{run_id}/auto-match",
        headers=headers,
    )
    assert auto.status_code == 200

    ai = await client.get(
        f"/api/v1/financial-kernel/reconciliation/runs/{run_id}/ai-suggestions",
        headers=headers,
    )
    assert ai.status_code == 200
    categories = {s["category"] for s in ai.json()["data"]}
    assert "variance" in categories or "near_match" in categories
