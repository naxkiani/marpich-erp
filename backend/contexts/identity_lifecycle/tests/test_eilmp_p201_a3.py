"""P201-A3 — Credential lifecycle orchestration."""
from __future__ import annotations

import pytest

from contexts.identity.container import get_identity_service
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from contexts.identity_lifecycle.container import (
    get_registration_onboarding_service,
    reset_identity_lifecycle_service,
)
from contexts.authentication.container import reset_authentication_service


@pytest.fixture(autouse=True)
def _reset():
    reset_identity_lifecycle_service()
    reset_authentication_service()
    InMemoryStore.reset()
    yield
    reset_identity_lifecycle_service()
    reset_authentication_service()
    InMemoryStore.reset()


@pytest.mark.unit
@pytest.mark.asyncio
async def test_activation_orchestrates_credentials_via_identity():
    svc = get_registration_onboarding_service()
    registered = await svc.register_identity(
        "tenant-a",
        email="cred-a3@example.com",
        display_name="Cred A3",
        zt_context={"risk_score": 10, "device_trusted": True, "identity_evidence": True},
        auto_advance=True,
    )
    assert registered.succeeded, registered.error
    ref = registered.unwrap()["registration_ref"]
    await svc.initialize_profile("tenant-a", ref)
    await svc.start_onboarding("tenant-a", ref)
    prov = await svc.request_provisioning("tenant-a", ref)
    assert prov.succeeded, prov.error
    data = prov.unwrap()
    assert data["status"] == "activation_requested"
    creds = data["onboarding"].get("credentials") or {}
    assert creds.get("status") == "orchestrated"
    assert creds.get("password_must_change") is True
    assert creds.get("mfa_enrollment_required") is True
    user_id = str(data["onboarding"]["provisioning"]["user_id"])
    status = await get_identity_service().get_user_credential("tenant-a", user_id)
    assert status.succeeded
    assert status.unwrap()["password_must_change"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_orchestrate_credentials_is_idempotent():
    svc = get_registration_onboarding_service()
    registered = await svc.register_identity(
        "tenant-a",
        email="cred-idem@example.com",
        display_name="Cred Idem",
        zt_context={"risk_score": 10, "device_trusted": True, "identity_evidence": True},
        auto_advance=True,
    )
    ref = registered.unwrap()["registration_ref"]
    await svc.initialize_profile("tenant-a", ref)
    await svc.start_onboarding("tenant-a", ref)
    await svc.request_provisioning("tenant-a", ref)
    again = await svc.orchestrate_credentials("tenant-a", ref)
    assert again.succeeded, again.error
    assert again.unwrap()["onboarding"]["credentials"]["status"] == "orchestrated"
