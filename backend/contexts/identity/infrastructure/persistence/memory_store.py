"""In-memory persistence — dev/test; swap for PostgreSQL in production."""
from __future__ import annotations

from datetime import UTC, datetime

from contexts.identity.domain.aggregates.role import Role
from contexts.identity.domain.aggregates.user import User
from contexts.identity.domain.ports.repositories import (
    IPermissionCatalog,
    IRoleRepository,
    ISessionRepository,
    IUserRepository,
)
from contexts.identity.domain.services.session_policy import session_expiry
from shared.domain.value_objects.unique_id import UniqueId

PERMISSION_CODES = [
    "identity.users.read",
    "identity.users.write",
    "identity.users.delete",
    "identity.roles.read",
    "identity.roles.write",
    "identity.mfa.manage",
    "identity.sessions.read",
    "identity.sessions.revoke",
    "identity.audit.read",
    "identity.policies.write",
]


class InMemoryStore:
    users: dict[str, User] = {}
    users_by_email: dict[str, str] = {}
    roles: dict[str, Role] = {}
    sessions: dict[str, dict] = {}

    @classmethod
    def reset(cls) -> None:
        cls.users.clear()
        cls.users_by_email.clear()
        cls.roles.clear()
        cls.sessions.clear()


class InMemoryUserRepository(IUserRepository):
    async def find_by_email(self, tenant_id: str, email: str) -> User | None:
        key = f"{tenant_id}:{email.lower()}"
        uid = InMemoryStore.users_by_email.get(key)
        return InMemoryStore.users.get(uid) if uid else None

    async def find_by_id(self, tenant_id: str, user_id: UniqueId) -> User | None:
        user = InMemoryStore.users.get(str(user_id))
        if user and user.tenant_id == tenant_id:
            return user
        return None

    async def save(self, user: User) -> None:
        InMemoryStore.users[str(user.id)] = user
        InMemoryStore.users_by_email[f"{user.tenant_id}:{user.email}"] = str(user.id)

    async def exists_by_email(self, tenant_id: str, email: str) -> bool:
        return f"{tenant_id}:{email.lower()}" in InMemoryStore.users_by_email

    async def list_users(
        self,
        tenant_id: str,
        *,
        search: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[User]:
        users = [u for u in InMemoryStore.users.values() if u.tenant_id == tenant_id]
        if search:
            q = search.lower()
            users = [u for u in users if q in u.email or q in u.display_name.lower()]
        return users[offset : offset + limit]


class InMemoryRoleRepository(IRoleRepository):
    async def find_by_id(self, tenant_id: str, role_id: UniqueId) -> Role | None:
        role = InMemoryStore.roles.get(str(role_id))
        if role and role.tenant_id == tenant_id:
            return role
        return None

    async def find_by_code(self, tenant_id: str, code: str) -> Role | None:
        for role in InMemoryStore.roles.values():
            if role.tenant_id == tenant_id and role.code == code.lower():
                return role
        return None

    async def save(self, role: Role) -> None:
        InMemoryStore.roles[str(role.id)] = role

    async def list_roles(self, tenant_id: str) -> list[Role]:
        return [r for r in InMemoryStore.roles.values() if r.tenant_id == tenant_id]


class InMemorySessionRepository(ISessionRepository):
    _by_refresh: dict[str, str] = {}

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
        InMemoryStore.sessions[session_id] = {
            "id": session_id,
            "tenant_id": tenant_id,
            "user_id": user_id,
            "refresh_hash": refresh_hash,
            "expires_at": expires_at,
            "ip_address": ip_address,
            "user_agent": user_agent,
            "revoked": False,
        }
        self._by_refresh[refresh_hash] = session_id

    async def find_by_refresh_hash(self, refresh_hash: str) -> dict | None:
        session_id = self._by_refresh.get(refresh_hash)
        if not session_id:
            return None
        session = InMemoryStore.sessions.get(session_id)
        if not session or session.get("revoked"):
            return None
        if session["expires_at"] < datetime.now(UTC):
            return None
        return session

    async def revoke(self, session_id: str) -> None:
        session = InMemoryStore.sessions.get(session_id)
        if session:
            session["revoked"] = True

    async def revoke_all_for_user(self, tenant_id: str, user_id: str) -> None:
        for session in InMemoryStore.sessions.values():
            if isinstance(session, dict) and session.get("tenant_id") == tenant_id:
                if session.get("user_id") == user_id:
                    session["revoked"] = True


class InMemoryPermissionCatalog(IPermissionCatalog):
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
