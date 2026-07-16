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
from contexts.directory.infrastructure.security.ldap_service import StubLdapDirectoryClient
from contexts.policy.container import get_policy_evaluator
from shared.infrastructure.messaging.event_bus import InProcessEventBus

_service: DirectoryApplicationService | None = None
_registered = False


def get_directory_service() -> DirectoryApplicationService:
    global _service, _registered
    if _service is None:
        _service = DirectoryApplicationService(
            profiles=InMemoryDirectoryProfileRepository(),
            saml_providers=InMemorySamlProviderRepository(),
            ldap_connectors=InMemoryLdapConnectorRepository(),
            scim_providers=InMemoryScimProviderRepository(),
            sync_jobs=InMemoryDirectorySyncJobRepository(),
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
