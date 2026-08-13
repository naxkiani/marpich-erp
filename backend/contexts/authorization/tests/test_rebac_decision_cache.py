"""AuthZ ReBAC + decision cache foundation tests."""
from __future__ import annotations

import pytest

from contexts.authorization.container import get_authorization_service, reset_authorization_service
from contexts.authorization.domain.services import rebac_engine
from contexts.authorization.domain.services.decision_cache import (
    InMemoryDecisionCache,
    build_cache_key,
)


@pytest.fixture(autouse=True)
def _reset():
    reset_authorization_service()
    yield
    reset_authorization_service()


@pytest.mark.unit
def test_rebac_owner_implies_viewer():
    effect, reasons = rebac_engine.evaluate_rebac(
        tuples=[
            {
                "object_type": "document",
                "object_id": "d1",
                "relation": "owner",
                "subject_type": "user",
                "subject_id": "u1",
                "active": True,
            }
        ],
        subject_id="u1",
        object_type="document",
        object_id="d1",
        relation="viewer",
    )
    assert effect == "allow"
    assert any("owner_implies" in r for r in reasons)


@pytest.mark.unit
@pytest.mark.asyncio
async def test_write_relation_and_check_access():
    svc = get_authorization_service()
    await svc.seed("tenant-a")
    written = await svc.write_relation(
        "tenant-a",
        object_type="document",
        object_id="doc-1",
        relation="owner",
        subject_type="user",
        subject_id="user-1",
    )
    assert written.succeeded, written.error

    # Principal without RBAC permission still allowed via ReBAC on resource URI.
    class _FakePrincipals:
        async def resolve_permissions(self, tenant_id: str, principal_id: str) -> list[str]:
            return ["identity.users.read"]

        async def resolve_principal_attributes(self, tenant_id: str, principal_id: str) -> dict:
            return {"principal_id": principal_id}

    svc._principals = _FakePrincipals()  # type: ignore[method-assign]
    result = await svc.check_access(
        "tenant-a",
        principal_id="user-1",
        resource="marpich://document/doc-1",
        action="read",
        permission_code="documents.documents.read",
        context={},
        record=False,
    )
    assert result.succeeded, result.error
    assert result.unwrap()["decision"] == "allow"
    assert "rebac" in result.unwrap()["model"]


@pytest.mark.unit
@pytest.mark.asyncio
async def test_decision_cache_hit():
    svc = get_authorization_service()
    await svc.seed("tenant-a")

    class _FakePrincipals:
        async def resolve_permissions(self, tenant_id: str, principal_id: str) -> list[str]:
            return ["*"]

        async def resolve_principal_attributes(self, tenant_id: str, principal_id: str) -> dict:
            return {}

    svc._principals = _FakePrincipals()  # type: ignore[method-assign]
    first = await svc.check_access(
        "tenant-a",
        principal_id="admin-1",
        resource="marpich://banking/accounts/a1",
        action="read",
        permission_code="banking.accounts.read",
        record=True,
    )
    assert first.succeeded
    assert first.unwrap()["cache_hit"] is False
    second = await svc.check_access(
        "tenant-a",
        principal_id="admin-1",
        resource="marpich://banking/accounts/a1",
        action="read",
        permission_code="banking.accounts.read",
        record=True,
    )
    assert second.succeeded
    assert second.unwrap()["cache_hit"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_cache_invalidated_on_relation_write():
    cache = InMemoryDecisionCache()
    key = build_cache_key(
        tenant_id="tenant-a",
        principal_id="u1",
        permission_code="x.read",
        resource="r",
        action="read",
        facts={},
    )
    await cache.set(key, {"decision": "allow"}, 60)
    assert await cache.get(key) is not None
    await cache.invalidate_tenant("tenant-a")
    assert await cache.get(key) is None
