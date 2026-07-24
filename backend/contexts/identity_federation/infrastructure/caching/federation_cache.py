"""Tenant-scoped Redis strategy adapter for federation sessions/tokens (P200-B2)."""
from __future__ import annotations

from typing import Any, Protocol


class IFederationCache(Protocol):
    async def get(self, tenant_id: str, kind: str, key: str) -> Any | None: ...

    async def set(
        self,
        tenant_id: str,
        kind: str,
        key: str,
        value: Any,
        *,
        ttl_seconds: int = 300,
    ) -> None: ...

    async def delete(self, tenant_id: str, kind: str, key: str) -> None: ...


def cache_key(tenant_id: str, kind: str, key: str) -> str:
    return f"fed:{tenant_id}:{kind}:{key}"


class InMemoryFederationCache:
    """Dev/test cache matching Redis key pattern from ARCH_DATA_PLANE."""

    def __init__(self) -> None:
        self._store: dict[str, Any] = {}

    async def get(self, tenant_id: str, kind: str, key: str) -> Any | None:
        return self._store.get(cache_key(tenant_id, kind, key))

    async def set(
        self,
        tenant_id: str,
        kind: str,
        key: str,
        value: Any,
        *,
        ttl_seconds: int = 300,
    ) -> None:
        _ = ttl_seconds
        self._store[cache_key(tenant_id, kind, key)] = value

    async def delete(self, tenant_id: str, kind: str, key: str) -> None:
        self._store.pop(cache_key(tenant_id, kind, key), None)
