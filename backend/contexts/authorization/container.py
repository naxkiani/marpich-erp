"""Authorization PDP DI + event subscriptions."""
from __future__ import annotations

from contexts.authorization.application.service import AuthorizationApplicationService
from contexts.authorization.infrastructure.adapters.identity_principal_adapter import IdentityPrincipalAccessAdapter
from contexts.authorization.infrastructure.persistence.authorization_memory_store import (
    InMemoryAbacPolicyRepository,
    InMemoryAccessDecisionRepository,
    InMemoryAuthorizationProfileRepository,
)
from contexts.policy.container import get_policy_evaluator
from shared.infrastructure.messaging.event_bus import InProcessEventBus

_service: AuthorizationApplicationService | None = None
_registered = False


def get_authorization_service() -> AuthorizationApplicationService:
    global _service, _registered
    if _service is None:
        _service = AuthorizationApplicationService(
            profiles=InMemoryAuthorizationProfileRepository(),
            abac_policies=InMemoryAbacPolicyRepository(),
            decisions=InMemoryAccessDecisionRepository(),
            principals=IdentityPrincipalAccessAdapter(),
            policy_evaluator=get_policy_evaluator(),
        )
    if not _registered:
        InProcessEventBus.subscribe("platform.tenant.provisioned", _service.handle_tenant_provisioned)
        _registered = True
    return _service


def reset_authorization_service() -> None:
    global _service, _registered
    _service = None
    _registered = False
    InMemoryAuthorizationProfileRepository.reset()
    InMemoryAbacPolicyRepository.reset()
    InMemoryAccessDecisionRepository.reset()
