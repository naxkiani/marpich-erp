"""Request-scoped tenant/principal context for PostgreSQL RLS."""
from __future__ import annotations

from contextvars import ContextVar, Token

_tenant_id: ContextVar[str | None] = ContextVar("marpich_tenant_id", default=None)
_principal_id: ContextVar[str | None] = ContextVar("marpich_principal_id", default=None)


def get_current_tenant_id() -> str | None:
    return _tenant_id.get()


def get_current_principal_id() -> str | None:
    return _principal_id.get()


def bind_tenant_context(*, tenant_id: str | None, principal_id: str | None = None) -> tuple[Token, Token | None]:
    tenant_token = _tenant_id.set(tenant_id.lower() if tenant_id else None)
    principal_token = _principal_id.set(principal_id) if principal_id else None
    return tenant_token, principal_token


def reset_tenant_context(tenant_token: Token, principal_token: Token | None = None) -> None:
    _tenant_id.reset(tenant_token)
    if principal_token is not None:
        _principal_id.reset(principal_token)
