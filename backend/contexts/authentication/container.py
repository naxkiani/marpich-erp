"""Authentication DI container."""
from __future__ import annotations

from contexts.authentication.application.service import AuthenticationApplicationService
from contexts.authentication.infrastructure.adapters.identity_token_adapter import IdentityTokenAdapter
from contexts.authentication.infrastructure.persistence.authentication_memory_store import (
    InMemoryAuthenticationProfileRepository,
    InMemoryAuthenticationStore,
    InMemoryOidcProviderRepository,
    InMemoryOidcStateStore,
    InMemoryWebAuthnChallengeStore,
    InMemoryWebAuthnCredentialRepository,
)
from contexts.policy.container import get_policy_evaluator
from shared.infrastructure.messaging.event_bus import InProcessEventBus

_service: AuthenticationApplicationService | None = None
_registered = False


def get_authentication_service() -> AuthenticationApplicationService:
    global _service, _registered
    if _service is None:
        _service = AuthenticationApplicationService(
            profiles=InMemoryAuthenticationProfileRepository(),
            credentials=InMemoryWebAuthnCredentialRepository(),
            providers=InMemoryOidcProviderRepository(),
            challenges=InMemoryWebAuthnChallengeStore(),
            oidc_states=InMemoryOidcStateStore(),
            identity=IdentityTokenAdapter(),
            policy_evaluator=get_policy_evaluator(),
        )
    if not _registered:
        InProcessEventBus.subscribe("platform.tenant.provisioned", _service.handle_tenant_provisioned)
        _registered = True
    return _service


def reset_authentication_service() -> None:
    global _service, _registered
    _service = None
    _registered = False
    InMemoryAuthenticationStore.reset()
