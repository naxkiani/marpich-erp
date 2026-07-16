"""Repository ports — domain layer."""
from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Protocol

from contexts.identity.domain.aggregates.role import Role
from contexts.identity.domain.aggregates.user import User
from shared.domain.value_objects.unique_id import UniqueId


class IUserRepository(ABC):
    @abstractmethod
    async def find_by_email(self, tenant_id: str, email: str) -> User | None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, user_id: UniqueId) -> User | None: ...

    @abstractmethod
    async def save(self, user: User) -> None: ...

    @abstractmethod
    async def exists_by_email(self, tenant_id: str, email: str) -> bool: ...

    @abstractmethod
    async def list_users(
        self,
        tenant_id: str,
        *,
        search: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[User]: ...


class IRoleRepository(ABC):
    @abstractmethod
    async def find_by_id(self, tenant_id: str, role_id: UniqueId) -> Role | None: ...

    @abstractmethod
    async def find_by_code(self, tenant_id: str, code: str) -> Role | None: ...

    @abstractmethod
    async def save(self, role: Role) -> None: ...

    @abstractmethod
    async def list_roles(self, tenant_id: str) -> list[Role]: ...


class ISessionRepository(ABC):
    @abstractmethod
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
    ) -> None: ...

    @abstractmethod
    async def find_by_refresh_hash(self, refresh_hash: str) -> dict | None: ...

    @abstractmethod
    async def revoke(self, session_id: str) -> None: ...

    @abstractmethod
    async def revoke_all_for_user(self, tenant_id: str, user_id: str) -> None: ...

    @abstractmethod
    async def list_for_user(self, tenant_id: str, user_id: str) -> list[dict]: ...


class IPermissionCatalog(Protocol):
    async def resolve_permissions(self, tenant_id: str, role_ids: list[str]) -> list[str]: ...
