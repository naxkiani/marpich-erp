"""Dependency injection container — single instance per process."""
from __future__ import annotations

from contexts.identity.application.service import IdentityApplicationService
from contexts.identity.infrastructure.messaging.outbox import ConsoleAuditLogger, ConsoleOutboxPublisher
from contexts.identity.infrastructure.persistence.memory_store import (
    InMemoryPermissionCatalog,
    InMemoryRoleRepository,
    InMemorySessionRepository,
    InMemoryUserRepository,
)
from contexts.identity.infrastructure.persistence.postgres_store import (
    PostgresPermissionCatalog,
    PostgresRoleRepository,
    PostgresSessionRepository,
    PostgresUserRepository,
)
from contexts.identity.infrastructure.security.jwt import JwtTokenService
from contexts.identity.infrastructure.security.mfa import TotpMfaService
from contexts.identity.infrastructure.security.password import PasswordHasher
from shared.infrastructure.settings import use_postgres

_container: IdentityApplicationService | None = None


def get_identity_service() -> IdentityApplicationService:
    global _container
    if _container is None:
        if use_postgres():
            roles = PostgresRoleRepository()
            _container = IdentityApplicationService(
                users=PostgresUserRepository(),
                roles=roles,
                sessions=PostgresSessionRepository(),
                permissions=PostgresPermissionCatalog(roles),
                hasher=PasswordHasher(),
                tokens=JwtTokenService(),
                mfa=TotpMfaService(),
                audit=ConsoleAuditLogger(),
                outbox=ConsoleOutboxPublisher(),
            )
        else:
            roles = InMemoryRoleRepository()
            _container = IdentityApplicationService(
                users=InMemoryUserRepository(),
                roles=roles,
                sessions=InMemorySessionRepository(),
                permissions=InMemoryPermissionCatalog(roles),
                hasher=PasswordHasher(),
                tokens=JwtTokenService(),
                mfa=TotpMfaService(),
                audit=ConsoleAuditLogger(),
                outbox=ConsoleOutboxPublisher(),
            )
    return _container
