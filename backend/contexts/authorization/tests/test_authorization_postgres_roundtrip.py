"""Authorization Postgres wiring + row mappers (no live DB)."""
from __future__ import annotations

from datetime import UTC, datetime
from types import SimpleNamespace
from uuid import UUID, uuid4

import pytest

from contexts.authorization.container import get_authorization_service, reset_authorization_service
from contexts.authorization.domain.aggregates.authorization_platform import (
    AbacPolicy,
    AccessDecision,
    AuthorizationProfile,
    RelationTuple,
)
from contexts.authorization.infrastructure.persistence.authorization_memory_store import (
    InMemoryAbacPolicyRepository,
    InMemoryAccessDecisionRepository,
    InMemoryAuthorizationProfileRepository,
    InMemoryRelationTupleRepository,
)
from contexts.authorization.infrastructure.persistence.authorization_postgres_store import (
    PostgresAbacPolicyRepository,
    PostgresAccessDecisionRepository,
    PostgresAuthorizationProfileRepository,
    PostgresRelationTupleRepository,
    _decision_from_row,
    _policy_from_row,
    _profile_from_row,
    _tuple_from_row,
)


@pytest.fixture(autouse=True)
def _reset(monkeypatch):
    monkeypatch.setattr("contexts.authorization.container.use_postgres", lambda: False)
    reset_authorization_service()
    yield
    reset_authorization_service()


def test_authorization_container_defaults_to_memory():
    svc = get_authorization_service()
    assert isinstance(svc._profiles, InMemoryAuthorizationProfileRepository)
    assert isinstance(svc._abac_policies, InMemoryAbacPolicyRepository)
    assert isinstance(svc._decisions, InMemoryAccessDecisionRepository)
    assert isinstance(svc._relations, InMemoryRelationTupleRepository)


def test_authorization_container_wires_postgres(monkeypatch):
    monkeypatch.setattr("contexts.authorization.container.use_postgres", lambda: True)
    reset_authorization_service()
    svc = get_authorization_service()
    assert isinstance(svc._profiles, PostgresAuthorizationProfileRepository)
    assert isinstance(svc._abac_policies, PostgresAbacPolicyRepository)
    assert isinstance(svc._decisions, PostgresAccessDecisionRepository)
    assert isinstance(svc._relations, PostgresRelationTupleRepository)


def test_authorization_row_mappers_round_trip():
    profile = AuthorizationProfile.create(tenant_id="t1", profile_ref="ERP-AUTH-PRF-T1-00001")
    restored = _profile_from_row(
        SimpleNamespace(
            id=UUID(str(profile.id)),
            tenant_id=profile.tenant_id,
            profile_ref=profile.profile_ref,
            rbac_enabled=True,
            rebac_enabled=True,
            abac_enabled=True,
            pbac_enabled=True,
            default_decision="deny",
            decision_cache_ttl_seconds=30,
            created_at=profile.created_at,
        )
    )
    assert restored.profile_ref == profile.profile_ref
    assert restored.rbac_enabled is True

    policy = AbacPolicy.create(
        tenant_id="t1",
        policy_ref="ERP-AUTH-POL-T1-00001",
        name="deny-after-hours",
        effect="deny",
        permission_pattern="banking.*",
        conditions=[{"attribute": "hour_utc", "operator": "lt", "value": 8}],
        priority=10,
    )
    assert _policy_from_row(
        SimpleNamespace(
            id=UUID(str(policy.id)),
            tenant_id=policy.tenant_id,
            policy_ref=policy.policy_ref,
            name=policy.name,
            effect=policy.effect,
            permission_pattern=policy.permission_pattern,
            conditions=policy.conditions,
            priority=policy.priority,
            active=True,
            created_at=policy.created_at,
        )
    ).permission_pattern == "banking.*"

    principal = uuid4()
    decision = AccessDecision.record(
        tenant_id="t1",
        decision_ref="ERP-AUTH-DEC-T1-00001",
        principal_id=str(principal),
        permission_code="identity.users.read",
        resource="marpich://identity/users/me",
        action="read",
        decision="allow",
        model="rbac",
        reason_codes=["rbac.permission"],
        policy_keys=[],
        obligations=[],
        facts={"device_trust": "high"},
    )
    mapped = _decision_from_row(
        SimpleNamespace(
            id=UUID(str(decision.id)),
            tenant_id=decision.tenant_id,
            decision_ref=decision.decision_ref,
            principal_id=principal,
            permission_code=decision.permission_code,
            resource=decision.resource,
            action=decision.action,
            decision=decision.decision,
            reason="rbac.permission",
            context=decision.facts,
            model="rbac",
            reason_codes=decision.reason_codes,
            policy_keys=[],
            obligations=[],
            facts=decision.facts,
            decided_at=datetime.now(UTC),
        )
    )
    assert mapped.decision == "allow"
    assert mapped.reason_codes == ["rbac.permission"]

    tuple_ = RelationTuple.write(
        tenant_id="t1",
        relation_ref="ERP-AUTH-REL-T1-00001",
        object_type="account",
        object_id="acc-1",
        relation="viewer",
        subject_type="user",
        subject_id="u-1",
    )
    assert _tuple_from_row(
        SimpleNamespace(
            id=UUID(str(tuple_.id)),
            tenant_id=tuple_.tenant_id,
            relation_ref=tuple_.relation_ref,
            object_type=tuple_.object_type,
            object_id=tuple_.object_id,
            relation=tuple_.relation,
            subject_type=tuple_.subject_type,
            subject_id=tuple_.subject_id,
            active=True,
            created_at=tuple_.created_at,
        )
    ).relation == "viewer"


@pytest.mark.asyncio
async def test_authorization_seed_and_list_policies():
    svc = get_authorization_service()
    seeded = await svc.seed("authz-p1")
    assert seeded.succeeded
    policies = await svc.list_abac_policies("authz-p1")
    assert policies.succeeded
    assert len(policies.unwrap()) >= 1
