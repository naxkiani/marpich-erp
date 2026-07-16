"""P201-A Registration & Onboarding foundation + runtime tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.identity_lifecycle.container import (
    get_registration_onboarding_service,
    reset_identity_lifecycle_service,
)
from contexts.identity_lifecycle.domain.services.eilmp_registration_onboarding import (
    validate_registration_onboarding_foundation,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_identity_lifecycle_service()
    yield
    reset_identity_lifecycle_service()


@pytest.mark.unit
def test_p201a_foundation_passes():
    result = validate_registration_onboarding_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["foundation_for"] == "P201-A2"
    assert result["forbidden_sibling_present"] is False
    assert result["registry"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_register_validate_approve_onboard_provision():
    svc = get_registration_onboarding_service()
    registered = await svc.register_identity(
        "tenant-a",
        email="alice@example.com",
        display_name="Alice Example",
        identity_type="employee",
        channel="rest_api",
        zt_context={"risk_score": 10, "device_trusted": True, "identity_evidence": True},
        auto_advance=True,
    )
    assert registered.succeeded, registered.error
    data = registered.unwrap()
    assert data["status"] == "approved"
    assert data["case_ref"]
    ref = data["registration_ref"]

    profile = await svc.initialize_profile("tenant-a", ref)
    assert profile.succeeded
    assert profile.unwrap()["profile"]["personal"]["email"] == "alice@example.com"

    onb = await svc.start_onboarding("tenant-a", ref)
    assert onb.succeeded
    assert onb.unwrap()["status"] == "onboarding"

    prov = await svc.request_provisioning("tenant-a", ref)
    assert prov.succeeded
    assert prov.unwrap()["status"] == "activation_requested"
    assert prov.unwrap()["onboarding"]["provisioning"]["delegate_to"] == [
        "identity",
        "directory",
    ]


@pytest.mark.unit
@pytest.mark.asyncio
async def test_zero_trust_and_duplicate_gates():
    svc = get_registration_onboarding_service()
    blocked = await svc.register_identity(
        "tenant-a",
        email="bob@example.com",
        display_name="Bob",
        zt_context={"risk_score": 95},
        auto_advance=False,
    )
    assert blocked.succeeded is False
    assert "zero_trust" in (blocked.error or "")

    first = await svc.register_identity(
        "tenant-a",
        email="dup@example.com",
        display_name="First",
        zt_context={"risk_score": 5},
        auto_advance=True,
    )
    assert first.succeeded
    second = await svc.register_identity(
        "tenant-a",
        email="dup@example.com",
        display_name="Second",
        zt_context={"risk_score": 5},
        auto_advance=True,
    )
    assert second.succeeded
    assert second.unwrap()["blocked_on"] == "duplicate_review"
    assert second.unwrap()["duplicate_matches"]
