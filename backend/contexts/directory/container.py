"""Directory DI container."""
from __future__ import annotations

from contexts.directory.application.service import DirectoryApplicationService
from contexts.directory.infrastructure.adapters.identity_provisioning_adapter import IdentityProvisioningAdapter
from contexts.directory.infrastructure.persistence.directory_memory_store import (
    InMemoryDirectoryProfileRepository,
    InMemoryDirectoryStore,
    InMemoryDirectorySyncJobRepository,
    InMemoryLdapConnectorRepository,
    InMemorySamlProviderRepository,
    InMemorySamlRelayStateStore,
    InMemoryScimProviderRepository,
)
from contexts.directory.infrastructure.persistence.directory_postgres_store import (
    PostgresDirectoryProfileRepository,
    PostgresDirectorySyncJobRepository,
    PostgresLdapConnectorRepository,
    PostgresSamlProviderRepository,
    PostgresScimProviderRepository,
    _RefCounterMixin as _DirectoryPgRefCounter,
)
from contexts.directory.infrastructure.security.ldap_service import StubLdapDirectoryClient
from contexts.policy.container import get_policy_evaluator
from shared.infrastructure.messaging.event_bus import InProcessEventBus
from shared.infrastructure.settings import use_postgres

_service: DirectoryApplicationService | None = None
_registered = False


def get_directory_service() -> DirectoryApplicationService:
    global _service, _registered
    if _service is None:
        if use_postgres():
            profiles: object = PostgresDirectoryProfileRepository()
            saml_providers: object = PostgresSamlProviderRepository()
            ldap_connectors: object = PostgresLdapConnectorRepository()
            scim_providers: object = PostgresScimProviderRepository()
            sync_jobs: object = PostgresDirectorySyncJobRepository()
        else:
            profiles = InMemoryDirectoryProfileRepository()
            saml_providers = InMemorySamlProviderRepository()
            ldap_connectors = InMemoryLdapConnectorRepository()
            scim_providers = InMemoryScimProviderRepository()
            sync_jobs = InMemoryDirectorySyncJobRepository()
        _service = DirectoryApplicationService(
            profiles=profiles,
            saml_providers=saml_providers,
            ldap_connectors=ldap_connectors,
            scim_providers=scim_providers,
            sync_jobs=sync_jobs,
            relay_states=InMemorySamlRelayStateStore(),
            identity=IdentityProvisioningAdapter(),
            policy_evaluator=get_policy_evaluator(),
            ldap_client=StubLdapDirectoryClient(),
        )
    if not _registered:
        InProcessEventBus.subscribe("platform.tenant.provisioned", _service.handle_tenant_provisioned)
        _registered = True
    return _service


def reset_directory_service() -> None:
    global _service, _registered
    _service = None
    _registered = False
    InMemoryDirectoryStore.reset()
    _DirectoryPgRefCounter.reset_counters()
