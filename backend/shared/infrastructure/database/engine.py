"""Async SQLAlchemy engine and session factory."""
from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from shared.infrastructure.database.rls_context import get_current_principal_id, get_current_tenant_id
from shared.infrastructure.settings import settings, use_rls

_engine = None
_session_factory: async_sessionmaker[AsyncSession] | None = None


def get_engine():
    global _engine
    if _engine is None:
        _engine = create_async_engine(settings.database_url, echo=False, pool_pre_ping=True)
    return _engine


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    global _session_factory
    if _session_factory is None:
        _session_factory = async_sessionmaker(get_engine(), expire_on_commit=False)
    return _session_factory


async def _apply_rls_session_vars(session: AsyncSession, *, tenant_id: str | None, principal_id: str | None) -> None:
    if not use_rls():
        return
    active_tenant = tenant_id or get_current_tenant_id()
    if not active_tenant:
        return
    await session.execute(text("SELECT set_config('app.tenant_id', :tenant_id, true)"), {"tenant_id": active_tenant})
    active_principal = principal_id or get_current_principal_id()
    if active_principal:
        await session.execute(
            text("SELECT set_config('app.principal_id', :principal_id, true)"),
            {"principal_id": active_principal},
        )


@asynccontextmanager
async def session_scope(
    *,
    tenant_id: str | None = None,
    principal_id: str | None = None,
) -> AsyncIterator[AsyncSession]:
    factory = get_session_factory()
    async with factory() as session:
        try:
            await _apply_rls_session_vars(session, tenant_id=tenant_id, principal_id=principal_id)
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def dispose_engine() -> None:
    global _engine, _session_factory
    if _engine is not None:
        await _engine.dispose()
        _engine = None
        _session_factory = None
