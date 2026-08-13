"""AuthZ decision cache — tenant-scoped TTL cache (memory default; Redis optional)."""
from __future__ import annotations

import hashlib
import json
import logging
import time
from typing import Protocol

logger = logging.getLogger(__name__)


class IDecisionCache(Protocol):
    async def get(self, key: str) -> dict | None: ...
    async def set(self, key: str, value: dict, ttl_seconds: int) -> None: ...
    async def invalidate_tenant(self, tenant_id: str) -> None: ...
    async def invalidate_prefix(self, prefix: str) -> None: ...


def build_cache_key(
    *,
    tenant_id: str,
    principal_id: str,
    permission_code: str,
    resource: str,
    action: str,
    facts: dict,
) -> str:
    fact_blob = json.dumps(facts or {}, sort_keys=True, default=str)
    digest = hashlib.sha256(fact_blob.encode()).hexdigest()[:16]
    return f"authz:{tenant_id}:{principal_id}:{permission_code}:{resource}:{action}:{digest}"


class InMemoryDecisionCache:
    """Process-local TTL cache. Keys always include tenant_id."""

    _entries: dict[str, tuple[float, dict]] = {}

    @classmethod
    def reset(cls) -> None:
        cls._entries = {}

    async def get(self, key: str) -> dict | None:
        item = self._entries.get(key)
        if not item:
            return None
        expires_at, value = item
        if time.monotonic() > expires_at:
            self._entries.pop(key, None)
            return None
        return dict(value)

    async def set(self, key: str, value: dict, ttl_seconds: int) -> None:
        ttl = max(1, int(ttl_seconds))
        self._entries[key] = (time.monotonic() + ttl, dict(value))

    async def invalidate_tenant(self, tenant_id: str) -> None:
        prefix = f"authz:{tenant_id}:"
        await self.invalidate_prefix(prefix)

    async def invalidate_prefix(self, prefix: str) -> None:
        doomed = [k for k in self._entries if k.startswith(prefix)]
        for k in doomed:
            self._entries.pop(k, None)


class RedisDecisionCache:
    """Redis-backed cache. Falls back to in-memory behavior if Redis unavailable."""

    def __init__(self, redis_url: str) -> None:
        self._url = redis_url
        self._client = None
        self._fallback = InMemoryDecisionCache()

    def _connect(self):
        if self._client is not None:
            return self._client
        try:
            import redis  # type: ignore

            self._client = redis.from_url(self._url, decode_responses=True)
            self._client.ping()
            return self._client
        except Exception:  # noqa: BLE001
            logger.warning("authz_redis_cache_unavailable_using_memory")
            self._client = False
            return None

    async def get(self, key: str) -> dict | None:
        client = self._connect()
        if not client:
            return await self._fallback.get(key)
        raw = client.get(key)
        if not raw:
            return None
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return None

    async def set(self, key: str, value: dict, ttl_seconds: int) -> None:
        client = self._connect()
        if not client:
            await self._fallback.set(key, value, ttl_seconds)
            return
        client.setex(key, max(1, int(ttl_seconds)), json.dumps(value, default=str))

    async def invalidate_tenant(self, tenant_id: str) -> None:
        await self.invalidate_prefix(f"authz:{tenant_id}:")

    async def invalidate_prefix(self, prefix: str) -> None:
        client = self._connect()
        if not client:
            await self._fallback.invalidate_prefix(prefix)
            return
        cursor = 0
        while True:
            cursor, keys = client.scan(cursor=cursor, match=f"{prefix}*", count=100)
            if keys:
                client.delete(*keys)
            if cursor == 0:
                break


def create_decision_cache(*, backend: str, redis_url: str = "") -> IDecisionCache:
    if backend.lower() == "redis" and redis_url:
        return RedisDecisionCache(redis_url)
    return InMemoryDecisionCache()
