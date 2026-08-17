"""PostgreSQL repositories — Authorization PDP SoR."""
from __future__ import annotations

import uuid
from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select

from contexts.authorization.domain.aggregates.authorization_platform import (
    AbacPolicy,
    AccessDecision,
    AuthorizationProfile,
    RelationTuple,
)
from contexts.authorization.domain.ports.authorization_repositories import (
    IAbacPolicyRepository,
    IAccessDecisionRepository,
    IAuthorizationProfileRepository,
    IRelationTupleRepository,
)
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.database.engine import session_scope
from shared.infrastructure.database.orm import (
    AccessDecisionRow,
    AuthorizationAbacPolicyRow,
    AuthorizationProfileRow,
    AuthorizationRelationTupleRow,
)


def _uuid(value: UniqueId | str | UUID) -> UUID:
    if isinstance(value, UUID):
        return value
    return UUID(str(value))


def _principal_uuid(value: str) -> UUID:
    try:
        return UUID(str(value))
    except ValueError:
        return uuid.uuid5(uuid.NAMESPACE_URL, str(value))


class _RefCounterMixin:
    _local_counters: dict[str, int] = {}

    def _local_next(self, tenant_id: str, prefix: str) -> str:
        key = f"{tenant_id}:{prefix}"
        n = self._local_counters.get(key, 0) + 1
        self._local_counters[key] = n
        return f"{prefix}-{tenant_id[:4].upper()}-{n:05d}"

    @classmethod
    def reset_counters(cls) -> None:
        cls._local_counters = {}


def _profile_from_row(row: object) -> AuthorizationProfile:
    return AuthorizationProfile(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        profile_ref=row.profile_ref,
        rbac_enabled=bool(row.rbac_enabled),
        rebac_enabled=bool(row.rebac_enabled),
        abac_enabled=bool(row.abac_enabled),
        pbac_enabled=bool(row.pbac_enabled),
        default_decision=row.default_decision,
        decision_cache_ttl_seconds=int(row.decision_cache_ttl_seconds),
        created_at=row.created_at or datetime.now(UTC),
    )


def _policy_from_row(row: object) -> AbacPolicy:
    return AbacPolicy(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        policy_ref=row.policy_ref,
        name=row.name,
        effect=row.effect,
        permission_pattern=row.permission_pattern,
        conditions=list(row.conditions or []),
        priority=int(row.priority),
        active=bool(row.active),
        created_at=row.created_at or datetime.now(UTC),
    )


def _decision_from_row(row: object) -> AccessDecision:
    reason_codes = list(getattr(row, "reason_codes", None) or [])
    if not reason_codes and getattr(row, "reason", None):
        reason_codes = [row.reason]
    facts = dict(getattr(row, "facts", None) or getattr(row, "context", None) or {})
    return AccessDecision(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        decision_ref=row.decision_ref,
        principal_id=str(row.principal_id),
        permission_code=row.permission_code or "",
        resource=row.resource or "",
        action=row.action or "",
        decision=row.decision,
        model=getattr(row, "model", None) or "rbac",
        reason_codes=reason_codes,
        policy_keys=list(getattr(row, "policy_keys", None) or []),
        obligations=list(getattr(row, "obligations", None) or []),
        facts=facts,
        created_at=row.decided_at or datetime.now(UTC),
    )


def _tuple_from_row(row: object) -> RelationTuple:
    return RelationTuple(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        relation_ref=row.relation_ref,
        object_type=row.object_type,
        object_id=row.object_id,
        relation=row.relation,
        subject_type=row.subject_type,
        subject_id=row.subject_id,
        active=bool(row.active),
        created_at=row.created_at or datetime.now(UTC),
    )


class PostgresAuthorizationProfileRepository(IAuthorizationProfileRepository, _RefCounterMixin):
    async def save(self, profile: AuthorizationProfile) -> None:
        async with session_scope(tenant_id=profile.tenant_id) as session:
            row = await session.get(
                AuthorizationProfileRow, (profile.tenant_id, _uuid(profile.id))
            )
            if row is None:
                session.add(
                    AuthorizationProfileRow(
                        tenant_id=profile.tenant_id,
                        id=_uuid(profile.id),
                        profile_ref=profile.profile_ref,
                        rbac_enabled=profile.rbac_enabled,
                        rebac_enabled=profile.rebac_enabled,
                        abac_enabled=profile.abac_enabled,
                        pbac_enabled=profile.pbac_enabled,
                        default_decision=profile.default_decision,
                        decision_cache_ttl_seconds=profile.decision_cache_ttl_seconds,
                        created_at=profile.created_at,
                    )
                )
            else:
                row.profile_ref = profile.profile_ref
                row.rbac_enabled = profile.rbac_enabled
                row.rebac_enabled = profile.rebac_enabled
                row.abac_enabled = profile.abac_enabled
                row.pbac_enabled = profile.pbac_enabled
                row.default_decision = profile.default_decision
                row.decision_cache_ttl_seconds = profile.decision_cache_ttl_seconds

    async def find_by_tenant(self, tenant_id: str) -> AuthorizationProfile | None:
        async with session_scope(tenant_id=tenant_id) as session:
            row = await session.scalar(
                select(AuthorizationProfileRow).where(
                    AuthorizationProfileRow.tenant_id == tenant_id
                )
            )
            return _profile_from_row(row) if row else None

    def next_profile_ref(self, tenant_id: str) -> str:
        return self._local_next(tenant_id, "ERP-AUTH-PRF")


class PostgresAbacPolicyRepository(IAbacPolicyRepository, _RefCounterMixin):
    async def save(self, policy: AbacPolicy) -> None:
        async with session_scope(tenant_id=policy.tenant_id) as session:
            row = await session.get(
                AuthorizationAbacPolicyRow, (policy.tenant_id, _uuid(policy.id))
            )
            if row is None:
                session.add(
                    AuthorizationAbacPolicyRow(
                        tenant_id=policy.tenant_id,
                        id=_uuid(policy.id),
                        policy_ref=policy.policy_ref,
                        name=policy.name,
                        effect=policy.effect,
                        permission_pattern=policy.permission_pattern,
                        conditions=list(policy.conditions or []),
                        priority=policy.priority,
                        active=policy.active,
                        created_at=policy.created_at,
                    )
                )
            else:
                row.policy_ref = policy.policy_ref
                row.name = policy.name
                row.effect = policy.effect
                row.permission_pattern = policy.permission_pattern
                row.conditions = list(policy.conditions or [])
                row.priority = policy.priority
                row.active = policy.active

    async def list_by_tenant(self, tenant_id: str) -> list[AbacPolicy]:
        async with session_scope(tenant_id=tenant_id) as session:
            rows = (
                await session.scalars(
                    select(AuthorizationAbacPolicyRow).where(
                        AuthorizationAbacPolicyRow.tenant_id == tenant_id
                    )
                )
            ).all()
        return [_policy_from_row(r) for r in rows]

    def next_policy_ref(self, tenant_id: str) -> str:
        return self._local_next(tenant_id, "ERP-AUTH-POL")


class PostgresAccessDecisionRepository(IAccessDecisionRepository, _RefCounterMixin):
    async def save(self, decision: AccessDecision) -> None:
        decided_at = decision.created_at or datetime.now(UTC)
        reason = ";".join(decision.reason_codes) if decision.reason_codes else None
        async with session_scope(tenant_id=decision.tenant_id) as session:
            row = await session.scalar(
                select(AccessDecisionRow).where(
                    AccessDecisionRow.tenant_id == decision.tenant_id,
                    AccessDecisionRow.id == _uuid(decision.id),
                )
            )
            if row is None:
                session.add(
                    AccessDecisionRow(
                        tenant_id=decision.tenant_id,
                        id=_uuid(decision.id),
                        decided_at=decided_at,
                        decision_ref=decision.decision_ref,
                        principal_id=_principal_uuid(decision.principal_id),
                        resource=decision.resource,
                        action=decision.action,
                        permission_code=decision.permission_code or None,
                        decision=decision.decision,
                        reason=reason,
                        context=dict(decision.facts or {}),
                        model=decision.model,
                        reason_codes=list(decision.reason_codes or []),
                        policy_keys=list(decision.policy_keys or []),
                        obligations=list(decision.obligations or []),
                        facts=dict(decision.facts or {}),
                    )
                )
            else:
                row.decision_ref = decision.decision_ref
                row.principal_id = _principal_uuid(decision.principal_id)
                row.resource = decision.resource
                row.action = decision.action
                row.permission_code = decision.permission_code or None
                row.decision = decision.decision
                row.reason = reason
                row.context = dict(decision.facts or {})
                row.model = decision.model
                row.reason_codes = list(decision.reason_codes or [])
                row.policy_keys = list(decision.policy_keys or [])
                row.obligations = list(decision.obligations or [])
                row.facts = dict(decision.facts or {})

    async def list_by_tenant(self, tenant_id: str, *, limit: int = 50) -> list[AccessDecision]:
        async with session_scope(tenant_id=tenant_id) as session:
            rows = (
                await session.scalars(
                    select(AccessDecisionRow)
                    .where(AccessDecisionRow.tenant_id == tenant_id)
                    .order_by(AccessDecisionRow.decided_at.desc())
                    .limit(limit)
                )
            ).all()
        return [_decision_from_row(r) for r in rows]

    def next_decision_ref(self, tenant_id: str) -> str:
        return self._local_next(tenant_id, "ERP-AUTH-DEC")


class PostgresRelationTupleRepository(IRelationTupleRepository, _RefCounterMixin):
    async def save(self, tuple_: RelationTuple) -> None:
        async with session_scope(tenant_id=tuple_.tenant_id) as session:
            row = await session.get(
                AuthorizationRelationTupleRow, (tuple_.tenant_id, _uuid(tuple_.id))
            )
            if row is None:
                session.add(
                    AuthorizationRelationTupleRow(
                        tenant_id=tuple_.tenant_id,
                        id=_uuid(tuple_.id),
                        relation_ref=tuple_.relation_ref,
                        object_type=tuple_.object_type,
                        object_id=tuple_.object_id,
                        relation=tuple_.relation,
                        subject_type=tuple_.subject_type,
                        subject_id=tuple_.subject_id,
                        active=tuple_.active,
                        created_at=tuple_.created_at,
                    )
                )
            else:
                row.relation_ref = tuple_.relation_ref
                row.object_type = tuple_.object_type
                row.object_id = tuple_.object_id
                row.relation = tuple_.relation
                row.subject_type = tuple_.subject_type
                row.subject_id = tuple_.subject_id
                row.active = tuple_.active

    async def list_by_object(
        self, tenant_id: str, object_type: str, object_id: str
    ) -> list[RelationTuple]:
        async with session_scope(tenant_id=tenant_id) as session:
            rows = (
                await session.scalars(
                    select(AuthorizationRelationTupleRow).where(
                        AuthorizationRelationTupleRow.tenant_id == tenant_id,
                        AuthorizationRelationTupleRow.object_type == object_type.lower(),
                        AuthorizationRelationTupleRow.object_id == object_id,
                        AuthorizationRelationTupleRow.active.is_(True),
                    )
                )
            ).all()
        return [_tuple_from_row(r) for r in rows]

    async def list_by_subject(
        self, tenant_id: str, subject_type: str, subject_id: str
    ) -> list[RelationTuple]:
        async with session_scope(tenant_id=tenant_id) as session:
            rows = (
                await session.scalars(
                    select(AuthorizationRelationTupleRow).where(
                        AuthorizationRelationTupleRow.tenant_id == tenant_id,
                        AuthorizationRelationTupleRow.subject_type == subject_type.lower(),
                        AuthorizationRelationTupleRow.subject_id == subject_id,
                        AuthorizationRelationTupleRow.active.is_(True),
                    )
                )
            ).all()
        return [_tuple_from_row(r) for r in rows]

    async def find_exact(
        self,
        tenant_id: str,
        *,
        object_type: str,
        object_id: str,
        relation: str,
        subject_type: str,
        subject_id: str,
    ) -> RelationTuple | None:
        async with session_scope(tenant_id=tenant_id) as session:
            row = await session.scalar(
                select(AuthorizationRelationTupleRow).where(
                    AuthorizationRelationTupleRow.tenant_id == tenant_id,
                    AuthorizationRelationTupleRow.object_type == object_type.lower(),
                    AuthorizationRelationTupleRow.object_id == object_id,
                    AuthorizationRelationTupleRow.relation == relation.lower(),
                    AuthorizationRelationTupleRow.subject_type == subject_type.lower(),
                    AuthorizationRelationTupleRow.subject_id == subject_id,
                )
            )
            return _tuple_from_row(row) if row else None

    def next_relation_ref(self, tenant_id: str) -> str:
        return self._local_next(tenant_id, "ERP-AUTH-REL")
