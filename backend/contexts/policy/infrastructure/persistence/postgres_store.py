"""PostgreSQL policy repositories."""
from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import func, select

from contexts.policy.domain.aggregates.policy import Policy
from contexts.policy.domain.aggregates.policy_version import PolicyStatus, PolicyVersion
from contexts.policy.domain.ports.repositories import IPolicyRepository, IPolicyVersionRepository
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.database.engine import session_scope
from shared.infrastructure.database.orm import PolicyRow, PolicyVersionRow


class PostgresPolicyRepository(IPolicyRepository):
    async def save(self, policy: Policy) -> None:
        async with session_scope() as session:
            row = await session.get(PolicyRow, UUID(str(policy.id)))
            if row is None:
                session.add(
                    PolicyRow(
                        id=UUID(str(policy.id)),
                        tenant_id=policy.tenant_id,
                        domain=policy.domain,
                        key=policy.key,
                        name=policy.name,
                        description=policy.description,
                        organization_id=policy.organization_id,
                        created_at=policy.created_at,
                    )
                )
            else:
                row.name = policy.name
                row.description = policy.description
                row.organization_id = policy.organization_id

    async def find_by_id(self, tenant_id: str, policy_id: UniqueId) -> Policy | None:
        async with session_scope() as session:
            row = await session.get(PolicyRow, UUID(str(policy_id)))
            if row and row.tenant_id == tenant_id:
                return _policy_from_row(row)
        return None

    async def find_by_key(self, tenant_id: str, domain: str, key: str) -> Policy | None:
        domain = domain.strip().lower()
        key = key.strip().lower()
        async with session_scope() as session:
            row = await session.scalar(
                select(PolicyRow).where(
                    PolicyRow.tenant_id == tenant_id,
                    PolicyRow.domain == domain,
                    PolicyRow.key == key,
                )
            )
            if row:
                return _policy_from_row(row)
        return None

    async def list_by_tenant(
        self, tenant_id: str, *, domain: str | None = None, status: str | None = None
    ) -> list[Policy]:
        async with session_scope() as session:
            stmt = select(PolicyRow).where(PolicyRow.tenant_id == tenant_id)
            if domain:
                stmt = stmt.where(PolicyRow.domain == domain.strip().lower())
            rows = (await session.scalars(stmt.order_by(PolicyRow.domain, PolicyRow.key))).all()
        policies = [_policy_from_row(r) for r in rows]
        if not status:
            return policies
        filtered = []
        for policy in policies:
            async with session_scope() as session:
                ver = await session.scalar(
                    select(PolicyVersionRow).where(
                        PolicyVersionRow.policy_id == UUID(str(policy.id)),
                        PolicyVersionRow.status == status,
                    )
                )
                if ver:
                    filtered.append(policy)
        return filtered


class PostgresPolicyVersionRepository(IPolicyVersionRepository):
    async def save(self, version: PolicyVersion) -> None:
        async with session_scope() as session:
            row = await session.scalar(
                select(PolicyVersionRow).where(
                    PolicyVersionRow.policy_id == UUID(version.policy_id),
                    PolicyVersionRow.version == version.version,
                )
            )
            if row is None:
                session.add(
                    PolicyVersionRow(
                        id=UUID(str(version.id)),
                        policy_id=UUID(version.policy_id),
                        tenant_id=version.tenant_id,
                        version=version.version,
                        status=version.status.value,
                        effective_from=version.effective_from,
                        expires_at=version.expires_at,
                        priority=version.priority,
                        conditions=version.conditions,
                        rules=version.rules,
                        exceptions=version.exceptions,
                        approval_required=version.approval_required,
                        workflow_key=version.workflow_key,
                        require_passing_tests=version.require_passing_tests,
                        cache_allowed=version.cache_allowed,
                        version_metadata=version.metadata,
                        created_at=version.created_at,
                    )
                )
            else:
                row.status = version.status.value
                row.effective_from = version.effective_from
                row.expires_at = version.expires_at
                row.priority = version.priority
                row.conditions = version.conditions
                row.rules = version.rules
                row.exceptions = version.exceptions
                row.version_metadata = version.metadata

    async def find_by_policy_and_version(
        self, tenant_id: str, policy_id: str, version: int
    ) -> PolicyVersion | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(PolicyVersionRow).where(
                    PolicyVersionRow.tenant_id == tenant_id,
                    PolicyVersionRow.policy_id == UUID(policy_id),
                    PolicyVersionRow.version == version,
                )
            )
            if row:
                return _version_from_row(row)
        return None

    async def list_by_policy(self, tenant_id: str, policy_id: str) -> list[PolicyVersion]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(PolicyVersionRow)
                    .where(
                        PolicyVersionRow.tenant_id == tenant_id,
                        PolicyVersionRow.policy_id == UUID(policy_id),
                    )
                    .order_by(PolicyVersionRow.version)
                )
            ).all()
        return [_version_from_row(r) for r in rows]

    async def find_active_for_key(
        self,
        tenant_id: str,
        domain: str,
        key: str,
        as_of: datetime,
    ) -> PolicyVersion | None:
        repo = PostgresPolicyRepository()
        policy = await repo.find_by_key(tenant_id, domain, key)
        if not policy:
            return None
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(PolicyVersionRow).where(
                        PolicyVersionRow.policy_id == UUID(str(policy.id)),
                        PolicyVersionRow.tenant_id == tenant_id,
                        PolicyVersionRow.status == PolicyStatus.ACTIVE.value,
                        PolicyVersionRow.effective_from <= as_of,
                    )
                )
            ).all()
        candidates = []
        for row in rows:
            ver = _version_from_row(row)
            if ver.is_effective_at(as_of):
                candidates.append(ver)
        if not candidates:
            return None
        candidates.sort(key=lambda v: v.priority, reverse=True)
        return candidates[0]

    async def supersede_active(self, tenant_id: str, policy_id: str, except_version: int) -> None:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(PolicyVersionRow).where(
                        PolicyVersionRow.tenant_id == tenant_id,
                        PolicyVersionRow.policy_id == UUID(policy_id),
                        PolicyVersionRow.status == PolicyStatus.ACTIVE.value,
                        PolicyVersionRow.version != except_version,
                    )
                )
            ).all()
            for row in rows:
                row.status = PolicyStatus.SUPERSEDED.value

    async def next_version_number(self, tenant_id: str, policy_id: str) -> int:
        async with session_scope() as session:
            current = await session.scalar(
                select(func.max(PolicyVersionRow.version)).where(
                    PolicyVersionRow.tenant_id == tenant_id,
                    PolicyVersionRow.policy_id == UUID(policy_id),
                )
            )
        return (current or 0) + 1


def _policy_from_row(row: PolicyRow) -> Policy:
    return Policy(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        domain=row.domain,
        key=row.key,
        name=row.name,
        description=row.description,
        organization_id=row.organization_id,
        created_at=row.created_at,
    )


def _version_from_row(row: PolicyVersionRow) -> PolicyVersion:
    return PolicyVersion(
        id=UniqueId.from_string(str(row.id)),
        policy_id=str(row.policy_id),
        tenant_id=row.tenant_id,
        version=row.version,
        status=PolicyStatus(row.status),
        effective_from=row.effective_from,
        expires_at=row.expires_at,
        priority=row.priority,
        conditions=row.conditions or [],
        rules=row.rules or [],
        exceptions=row.exceptions or [],
        approval_required=row.approval_required,
        workflow_key=row.workflow_key,
        require_passing_tests=row.require_passing_tests,
        cache_allowed=row.cache_allowed,
        metadata=row.version_metadata or {},
        created_at=row.created_at,
    )
