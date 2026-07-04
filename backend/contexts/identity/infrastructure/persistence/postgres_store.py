"""PostgreSQL repositories — Identity bounded context."""
from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select, update

from contexts.identity.domain.aggregates.role import Role
from contexts.identity.domain.aggregates.user import User, UserStatus
from contexts.identity.domain.ports.repositories import (
    IPermissionCatalog,
    IRoleRepository,
    ISessionRepository,
    IUserRepository,
)
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.database.engine import session_scope
from shared.infrastructure.database.orm import RoleRow, SessionRow, UserRow


def _uuid(value: UniqueId | str | UUID) -> UUID:
    if isinstance(value, UUID):
        return value
    return UUID(str(value))


class PostgresUserRepository(IUserRepository):
    async def find_by_email(self, tenant_id: str, email: str) -> User | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(UserRow).where(
                    UserRow.tenant_id == tenant_id,
                    UserRow.email == email.lower(),
                )
            )
            return _user_from_row(row) if row else None

    async def find_by_id(self, tenant_id: str, user_id: UniqueId) -> User | None:
        async with session_scope() as session:
            row = await session.get(UserRow, _uuid(user_id))
            if row and row.tenant_id == tenant_id:
                return _user_from_row(row)
            return None

    async def save(self, user: User) -> None:
        async with session_scope() as session:
            row = await session.get(UserRow, _uuid(user.id))
            if row is None:
                row = UserRow(id=_uuid(user.id), tenant_id=user.tenant_id, email=user.email)
                session.add(row)
            row.tenant_id = user.tenant_id
            row.email = user.email
            row.password_hash = user.password_hash
            row.display_name = user.display_name
            row.status = user.status.value
            row.locale = user.locale
            row.mfa_enabled = user.mfa_enabled
            row.mfa_secret = user.mfa_secret
            row.backup_codes = list(user.backup_codes)
            row.role_ids = list(user.role_ids)
            row.failed_login_attempts = user.failed_login_attempts
            row.locked_until = user.locked_until
            row.last_login_at = user.last_login_at
            row.updated_at = user.updated_at

    async def exists_by_email(self, tenant_id: str, email: str) -> bool:
        user = await self.find_by_email(tenant_id, email)
        return user is not None

    async def list_users(
        self,
        tenant_id: str,
        *,
        search: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[User]:
        async with session_scope() as session:
            stmt = select(UserRow).where(UserRow.tenant_id == tenant_id)
            rows = (await session.scalars(stmt)).all()
        users = [_user_from_row(r) for r in rows]
        if search:
            q = search.lower()
            users = [u for u in users if q in u.email or q in u.display_name.lower()]
        return users[offset : offset + limit]


class PostgresRoleRepository(IRoleRepository):
    async def find_by_id(self, tenant_id: str, role_id: UniqueId) -> Role | None:
        async with session_scope() as session:
            row = await session.get(RoleRow, _uuid(role_id))
            if row and row.tenant_id == tenant_id:
                return _role_from_row(row)
            return None

    async def find_by_code(self, tenant_id: str, code: str) -> Role | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(RoleRow).where(RoleRow.tenant_id == tenant_id, RoleRow.code == code.lower())
            )
            return _role_from_row(row) if row else None

    async def save(self, role: Role) -> None:
        async with session_scope() as session:
            row = await session.get(RoleRow, _uuid(role.id))
            if row is None:
                row = RoleRow(
                    id=_uuid(role.id),
                    tenant_id=role.tenant_id,
                    code=role.code,
                    name=role.name,
                )
                session.add(row)
            row.code = role.code
            row.name = role.name
            row.description = role.description
            row.is_system = role.is_system
            row.permission_ids = list(role.permission_ids)
            row.updated_at = role.updated_at

    async def list_roles(self, tenant_id: str) -> list[Role]:
        async with session_scope() as session:
            rows = (await session.scalars(select(RoleRow).where(RoleRow.tenant_id == tenant_id))).all()
        return [_role_from_row(r) for r in rows]


class PostgresSessionRepository(ISessionRepository):
    async def create(
        self,
        *,
        session_id: str,
        tenant_id: str,
        user_id: str,
        refresh_hash: str,
        expires_at: datetime,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> None:
        async with session_scope() as session:
            session.add(
                SessionRow(
                    id=UUID(session_id),
                    tenant_id=tenant_id,
                    user_id=UUID(user_id),
                    refresh_token_hash=refresh_hash,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    expires_at=expires_at,
                )
            )

    async def find_by_refresh_hash(self, refresh_hash: str) -> dict | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(SessionRow).where(
                    SessionRow.refresh_token_hash == refresh_hash,
                    SessionRow.revoked_at.is_(None),
                )
            )
            if not row or row.expires_at < datetime.now(UTC):
                return None
            return {
                "id": str(row.id),
                "tenant_id": row.tenant_id,
                "user_id": str(row.user_id),
                "refresh_hash": row.refresh_token_hash,
                "expires_at": row.expires_at,
                "ip_address": row.ip_address,
                "user_agent": row.user_agent,
                "revoked": False,
            }

    async def revoke(self, session_id: str) -> None:
        async with session_scope() as session:
            await session.execute(
                update(SessionRow)
                .where(SessionRow.id == UUID(session_id))
                .values(revoked_at=datetime.now(UTC))
            )

    async def revoke_all_for_user(self, tenant_id: str, user_id: str) -> None:
        async with session_scope() as session:
            await session.execute(
                update(SessionRow)
                .where(
                    SessionRow.tenant_id == tenant_id,
                    SessionRow.user_id == UUID(user_id),
                    SessionRow.revoked_at.is_(None),
                )
                .values(revoked_at=datetime.now(UTC))
            )


class PostgresPermissionCatalog(IPermissionCatalog):
    def __init__(self, roles: IRoleRepository) -> None:
        self._roles = roles

    async def resolve_permissions(self, tenant_id: str, role_ids: list[str]) -> list[str]:
        perms: set[str] = set()
        for rid in role_ids:
            role = await self._roles.find_by_id(tenant_id, UniqueId.from_string(rid))
            if not role:
                continue
            if "*" in role.permission_ids or role.code == "admin":
                return ["*"]
            perms.update(role.permission_ids)
        return sorted(perms)


def _user_from_row(row: UserRow) -> User:
    return User(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        email=row.email,
        password_hash=row.password_hash,
        display_name=row.display_name,
        status=UserStatus(row.status),
        locale=row.locale,
        mfa_enabled=row.mfa_enabled,
        mfa_secret=row.mfa_secret,
        backup_codes=list(row.backup_codes or []),
        role_ids=list(row.role_ids or []),
        failed_login_attempts=row.failed_login_attempts,
        locked_until=row.locked_until,
        last_login_at=row.last_login_at,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def _role_from_row(row: RoleRow) -> Role:
    return Role(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        code=row.code,
        name=row.name,
        description=row.description,
        is_system=row.is_system,
        permission_ids=list(row.permission_ids or []),
        created_at=row.created_at,
        updated_at=row.updated_at,
    )
