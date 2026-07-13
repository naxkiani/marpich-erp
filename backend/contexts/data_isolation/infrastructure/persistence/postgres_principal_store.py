"""Postgres principal repository (RLS-aware)."""
from __future__ import annotations

from uuid import UUID

from sqlalchemy import select

from contexts.data_isolation.domain.aggregates.data_isolation_platform import Principal
from contexts.data_isolation.domain.ports.data_isolation_repositories import IPrincipalRepository
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.database.engine import session_scope
from shared.infrastructure.database.orm import PrincipalRow


class PostgresPrincipalRepository(IPrincipalRepository):
    _ref_counter: dict[str, int] = {}

    def next_principal_ref(self, tenant_id: str) -> str:
        n = self._ref_counter.get(tenant_id, 0) + 1
        self._ref_counter[tenant_id] = n
        return f"principal-{tenant_id}-{n:04d}"

    async def save(self, principal: Principal) -> None:
        async with session_scope(tenant_id=principal.tenant_id) as session:
            row = await session.get(
                PrincipalRow,
                {"tenant_id": principal.tenant_id, "id": UUID(str(principal.id))},
            )
            if row is None:
                row = PrincipalRow(
                    tenant_id=principal.tenant_id,
                    id=UUID(str(principal.id)),
                    principal_ref=principal.principal_ref,
                    principal_type=principal.principal_type,
                )
                session.add(row)
            row.principal_ref = principal.principal_ref
            row.principal_type = principal.principal_type
            row.email = principal.email
            row.display_name = principal.display_name
            row.status = principal.status
            row.partition_bucket = principal.partition_bucket
            row.principal_metadata = {"source_user_id": principal.source_user_id}

    async def list_by_tenant(self, tenant_id: str) -> list[Principal]:
        async with session_scope(tenant_id=tenant_id) as session:
            rows = (await session.scalars(select(PrincipalRow).where(PrincipalRow.tenant_id == tenant_id))).all()
        return [_principal_from_row(row) for row in rows]

    async def find_by_ref(self, tenant_id: str, principal_ref: str) -> Principal | None:
        async with session_scope(tenant_id=tenant_id) as session:
            row = await session.scalar(
                select(PrincipalRow).where(
                    PrincipalRow.tenant_id == tenant_id,
                    PrincipalRow.principal_ref == principal_ref,
                )
            )
        return _principal_from_row(row) if row else None

    async def find_by_user_id(self, tenant_id: str, user_id: str) -> Principal | None:
        async with session_scope(tenant_id=tenant_id) as session:
            row = await session.scalar(
                select(PrincipalRow).where(
                    PrincipalRow.tenant_id == tenant_id,
                    PrincipalRow.id == UUID(user_id),
                )
            )
        return _principal_from_row(row) if row else None


def _principal_from_row(row: PrincipalRow) -> Principal:
    metadata = row.principal_metadata or {}
    return Principal(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        principal_ref=row.principal_ref,
        principal_type=row.principal_type,
        email=row.email,
        display_name=row.display_name,
        status=row.status,
        partition_bucket=row.partition_bucket,
        source_user_id=metadata.get("source_user_id"),
    )
