"""In-memory Authorization PDP persistence."""
from __future__ import annotations

from contexts.authorization.domain.aggregates.authorization_platform import (
    AbacPolicy,
    AccessDecision,
    AuthorizationProfile,
)
from contexts.authorization.domain.ports.authorization_repositories import (
    IAbacPolicyRepository,
    IAccessDecisionRepository,
    IAuthorizationProfileRepository,
)


class _RefCounter:
    _counters: dict[str, int] = {}

    @classmethod
    def reset(cls) -> None:
        cls._counters = {}

    @classmethod
    def next(cls, tenant_id: str, prefix: str) -> str:
        key = f"{tenant_id}:{prefix}"
        n = cls._counters.get(key, 0) + 1
        cls._counters[key] = n
        return f"{prefix}-{tenant_id[:4].upper()}-{n:05d}"


class InMemoryAuthorizationProfileRepository(IAuthorizationProfileRepository):
    _store: dict[str, AuthorizationProfile] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, profile: AuthorizationProfile) -> None:
        self._store[str(profile.id)] = profile

    async def find_by_tenant(self, tenant_id: str) -> AuthorizationProfile | None:
        for profile in self._store.values():
            if profile.tenant_id == tenant_id:
                return profile
        return None

    def next_profile_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-AUTH-PRF")


class InMemoryAbacPolicyRepository(IAbacPolicyRepository):
    _store: dict[str, AbacPolicy] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, policy: AbacPolicy) -> None:
        self._store[str(policy.id)] = policy

    async def list_by_tenant(self, tenant_id: str) -> list[AbacPolicy]:
        return [p for p in self._store.values() if p.tenant_id == tenant_id]

    def next_policy_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-AUTH-POL")


class InMemoryAccessDecisionRepository(IAccessDecisionRepository):
    _store: dict[str, AccessDecision] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, decision: AccessDecision) -> None:
        self._store[str(decision.id)] = decision

    async def list_by_tenant(self, tenant_id: str, *, limit: int = 50) -> list[AccessDecision]:
        items = [d for d in self._store.values() if d.tenant_id == tenant_id]
        return sorted(items, key=lambda d: d.created_at, reverse=True)[:limit]

    def next_decision_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-AUTH-DEC")
