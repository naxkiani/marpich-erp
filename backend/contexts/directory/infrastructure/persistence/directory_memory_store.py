"""In-memory directory persistence."""
from __future__ import annotations

import time

from contexts.directory.domain.aggregates.directory_platform import (
    DirectoryProfile,
    DirectorySyncJob,
    LdapConnector,
    SamlProvider,
    ScimProvider,
)
from contexts.directory.domain.ports.directory_repositories import (
    IDirectoryProfileRepository,
    IDirectorySyncJobRepository,
    ILdapConnectorRepository,
    ISamlProviderRepository,
    ISamlRelayStateStore,
    IScimProviderRepository,
)


class _TtlStore:
    _entries: dict[str, tuple[dict, float]] = {}

    @classmethod
    def reset(cls) -> None:
        cls._entries.clear()

    @classmethod
    def put(cls, key: str, payload: dict, ttl_seconds: int) -> None:
        cls._entries[key] = (payload, time.time() + ttl_seconds)

    @classmethod
    def pop(cls, key: str) -> dict | None:
        entry = cls._entries.pop(key, None)
        if not entry:
            return None
        payload, expires_at = entry
        if time.time() > expires_at:
            return None
        return payload


class InMemoryDirectoryStore:
    profiles: dict[str, DirectoryProfile] = {}
    saml_providers: dict[str, SamlProvider] = {}
    ldap_connectors: dict[str, LdapConnector] = {}
    scim_providers: dict[str, ScimProvider] = {}
    sync_jobs: dict[str, DirectorySyncJob] = {}
    ldap_seed_users: dict[str, list[dict]] = {}
    profile_counter: dict[str, int] = {}
    saml_counter: dict[str, int] = {}
    ldap_counter: dict[str, int] = {}
    scim_counter: dict[str, int] = {}
    job_counter: dict[str, int] = {}

    @classmethod
    def reset(cls) -> None:
        cls.profiles.clear()
        cls.saml_providers.clear()
        cls.ldap_connectors.clear()
        cls.scim_providers.clear()
        cls.sync_jobs.clear()
        cls.ldap_seed_users.clear()
        cls.profile_counter.clear()
        cls.saml_counter.clear()
        cls.ldap_counter.clear()
        cls.scim_counter.clear()
        cls.job_counter.clear()
        _TtlStore.reset()


class InMemoryDirectoryProfileRepository(IDirectoryProfileRepository):
    async def find_by_tenant(self, tenant_id: str) -> DirectoryProfile | None:
        return InMemoryDirectoryStore.profiles.get(tenant_id)

    async def save(self, profile: DirectoryProfile) -> None:
        InMemoryDirectoryStore.profiles[profile.tenant_id] = profile

    def next_profile_ref(self, tenant_id: str) -> str:
        n = InMemoryDirectoryStore.profile_counter.get(tenant_id, 0) + 1
        InMemoryDirectoryStore.profile_counter[tenant_id] = n
        return f"dir-profile-{tenant_id}-{n:04d}"


class InMemorySamlProviderRepository(ISamlProviderRepository):
    async def save(self, provider: SamlProvider) -> None:
        InMemoryDirectoryStore.saml_providers[provider.provider_ref] = provider

    async def list_by_tenant(self, tenant_id: str) -> list[SamlProvider]:
        return [p for p in InMemoryDirectoryStore.saml_providers.values() if p.tenant_id == tenant_id]

    async def find_by_ref(self, tenant_id: str, provider_ref: str) -> SamlProvider | None:
        provider = InMemoryDirectoryStore.saml_providers.get(provider_ref)
        if provider and provider.tenant_id == tenant_id:
            return provider
        return None

    def next_provider_ref(self, tenant_id: str) -> str:
        n = InMemoryDirectoryStore.saml_counter.get(tenant_id, 0) + 1
        InMemoryDirectoryStore.saml_counter[tenant_id] = n
        return f"saml-{tenant_id}-{n:04d}"


class InMemoryLdapConnectorRepository(ILdapConnectorRepository):
    async def save(self, connector: LdapConnector) -> None:
        InMemoryDirectoryStore.ldap_connectors[connector.connector_ref] = connector

    async def list_by_tenant(self, tenant_id: str) -> list[LdapConnector]:
        return [c for c in InMemoryDirectoryStore.ldap_connectors.values() if c.tenant_id == tenant_id]

    async def find_by_ref(self, tenant_id: str, connector_ref: str) -> LdapConnector | None:
        connector = InMemoryDirectoryStore.ldap_connectors.get(connector_ref)
        if connector and connector.tenant_id == tenant_id:
            return connector
        return None

    def next_connector_ref(self, tenant_id: str) -> str:
        n = InMemoryDirectoryStore.ldap_counter.get(tenant_id, 0) + 1
        InMemoryDirectoryStore.ldap_counter[tenant_id] = n
        return f"ldap-{tenant_id}-{n:04d}"


class InMemoryScimProviderRepository(IScimProviderRepository):
    async def save(self, provider: ScimProvider) -> None:
        InMemoryDirectoryStore.scim_providers[provider.provider_ref] = provider

    async def list_by_tenant(self, tenant_id: str) -> list[ScimProvider]:
        return [p for p in InMemoryDirectoryStore.scim_providers.values() if p.tenant_id == tenant_id]

    async def find_by_ref(self, tenant_id: str, provider_ref: str) -> ScimProvider | None:
        provider = InMemoryDirectoryStore.scim_providers.get(provider_ref)
        if provider and provider.tenant_id == tenant_id:
            return provider
        return None

    async def find_by_token(self, tenant_id: str, bearer_token: str) -> ScimProvider | None:
        for provider in InMemoryDirectoryStore.scim_providers.values():
            if provider.tenant_id == tenant_id and provider.bearer_token == bearer_token and provider.enabled:
                return provider
        return None

    def next_provider_ref(self, tenant_id: str) -> str:
        n = InMemoryDirectoryStore.scim_counter.get(tenant_id, 0) + 1
        InMemoryDirectoryStore.scim_counter[tenant_id] = n
        return f"scim-{tenant_id}-{n:04d}"


class InMemoryDirectorySyncJobRepository(IDirectorySyncJobRepository):
    async def save(self, job: DirectorySyncJob) -> None:
        InMemoryDirectoryStore.sync_jobs[job.job_ref] = job

    async def list_by_tenant(self, tenant_id: str) -> list[DirectorySyncJob]:
        return [j for j in InMemoryDirectoryStore.sync_jobs.values() if j.tenant_id == tenant_id]

    async def list_pending(self, tenant_id: str) -> list[DirectorySyncJob]:
        return [
            j
            for j in InMemoryDirectoryStore.sync_jobs.values()
            if j.tenant_id == tenant_id and j.status == "pending"
        ]

    async def find_by_ref(self, tenant_id: str, job_ref: str) -> DirectorySyncJob | None:
        job = InMemoryDirectoryStore.sync_jobs.get(job_ref)
        if job and job.tenant_id == tenant_id:
            return job
        return None

    def next_job_ref(self, tenant_id: str) -> str:
        n = InMemoryDirectoryStore.job_counter.get(tenant_id, 0) + 1
        InMemoryDirectoryStore.job_counter[tenant_id] = n
        return f"sync-{tenant_id}-{n:04d}"


class InMemorySamlRelayStateStore(ISamlRelayStateStore):
    async def put(self, relay_state: str, payload: dict, ttl_seconds: int) -> None:
        _TtlStore.put(f"saml:{relay_state}", payload, ttl_seconds)

    async def pop(self, relay_state: str) -> dict | None:
        return _TtlStore.pop(f"saml:{relay_state}")
