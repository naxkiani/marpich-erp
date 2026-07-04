"""In-memory policy repositories."""
from __future__ import annotations

from datetime import datetime

from contexts.policy.domain.aggregates.policy import Policy
from contexts.policy.domain.aggregates.policy_version import PolicyStatus, PolicyVersion
from contexts.policy.domain.ports.repositories import IPolicyRepository, IPolicyVersionRepository
from shared.domain.value_objects.unique_id import UniqueId


class PolicyMemoryStore:
    policies: dict[str, Policy] = {}
    versions: list[PolicyVersion] = []

    @classmethod
    def reset(cls) -> None:
        cls.policies.clear()
        cls.versions.clear()


class InMemoryPolicyRepository(IPolicyRepository):
    async def save(self, policy: Policy) -> None:
        PolicyMemoryStore.policies[str(policy.id)] = policy

    async def find_by_id(self, tenant_id: str, policy_id: UniqueId) -> Policy | None:
        policy = PolicyMemoryStore.policies.get(str(policy_id))
        if policy and policy.tenant_id == tenant_id:
            return policy
        return None

    async def find_by_key(self, tenant_id: str, domain: str, key: str) -> Policy | None:
        domain = domain.strip().lower()
        key = key.strip().lower()
        for policy in PolicyMemoryStore.policies.values():
            if policy.tenant_id == tenant_id and policy.domain == domain and policy.key == key:
                return policy
        return None

    async def list_by_tenant(
        self, tenant_id: str, *, domain: str | None = None, status: str | None = None
    ) -> list[Policy]:
        results = [p for p in PolicyMemoryStore.policies.values() if p.tenant_id == tenant_id]
        if domain:
            results = [p for p in results if p.domain == domain.strip().lower()]
        if status:
            filtered = []
            for policy in results:
                versions = [
                    v
                    for v in PolicyMemoryStore.versions
                    if v.policy_id == str(policy.id) and v.tenant_id == tenant_id
                ]
                if any(v.status.value == status for v in versions):
                    filtered.append(policy)
            results = filtered
        return sorted(results, key=lambda p: (p.domain, p.key))

    async def list_policy_ids_by_tenant(self, tenant_id: str) -> list[str]:
        return [str(p.id) for p in PolicyMemoryStore.policies.values() if p.tenant_id == tenant_id]


class InMemoryPolicyVersionRepository(IPolicyVersionRepository):
    async def save(self, version: PolicyVersion) -> None:
        PolicyMemoryStore.versions = [
            v
            for v in PolicyMemoryStore.versions
            if not (v.policy_id == version.policy_id and v.version == version.version)
        ]
        PolicyMemoryStore.versions.append(version)

    async def find_by_policy_and_version(
        self, tenant_id: str, policy_id: str, version: int
    ) -> PolicyVersion | None:
        for ver in PolicyMemoryStore.versions:
            if ver.tenant_id == tenant_id and ver.policy_id == policy_id and ver.version == version:
                return ver
        return None

    async def list_by_policy(self, tenant_id: str, policy_id: str) -> list[PolicyVersion]:
        return [
            v
            for v in PolicyMemoryStore.versions
            if v.tenant_id == tenant_id and v.policy_id == policy_id
        ]

    async def find_active_for_key(
        self,
        tenant_id: str,
        domain: str,
        key: str,
        as_of: datetime,
    ) -> PolicyVersion | None:
        repo = InMemoryPolicyRepository()
        policy = await repo.find_by_key(tenant_id, domain, key)
        if not policy:
            return None
        candidates = [
            v
            for v in PolicyMemoryStore.versions
            if v.policy_id == str(policy.id) and v.is_effective_at(as_of)
        ]
        if not candidates:
            return None
        candidates.sort(key=lambda v: v.priority, reverse=True)
        return candidates[0]

    async def supersede_active(self, tenant_id: str, policy_id: str, except_version: int) -> None:
        for ver in PolicyMemoryStore.versions:
            if (
                ver.tenant_id == tenant_id
                and ver.policy_id == policy_id
                and ver.status == PolicyStatus.ACTIVE
                and ver.version != except_version
            ):
                ver.supersede()

    async def next_version_number(self, tenant_id: str, policy_id: str) -> int:
        versions = await self.list_by_policy(tenant_id, policy_id)
        if not versions:
            return 1
        return max(v.version for v in versions) + 1
