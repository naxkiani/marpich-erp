"""Authorization PDP DI + event subscriptions."""
from __future__ import annotations

from contexts.authorization.application.service import AuthorizationApplicationService
from contexts.authorization.domain.services.decision_cache import (
    InMemoryDecisionCache,
    create_decision_cache,
)
from contexts.authorization.infrastructure.adapters.identity_principal_adapter import IdentityPrincipalAccessAdapter
from contexts.authorization.infrastructure.persistence.authorization_memory_store import (
    InMemoryAbacPolicyRepository,
    InMemoryAccessDecisionRepository,
    InMemoryAuthorizationProfileRepository,
    InMemoryRelationTupleRepository,
    _RefCounter,
)
from contexts.policy.container import get_policy_evaluator
from shared.infrastructure.messaging.event_bus import InProcessEventBus
from shared.infrastructure.settings import settings

_service: AuthorizationApplicationService | None = None
_registered = False
_cache = None


def get_authorization_service() -> AuthorizationApplicationService:
    global _service, _registered, _cache
    if _service is None:
        _cache = create_decision_cache(
            backend=settings.authz_decision_cache_backend,
            redis_url=settings.redis_url,
        )
        _service = AuthorizationApplicationService(
            profiles=InMemoryAuthorizationProfileRepository(),
            abac_policies=InMemoryAbacPolicyRepository(),
            decisions=InMemoryAccessDecisionRepository(),
            principals=IdentityPrincipalAccessAdapter(),
            policy_evaluator=get_policy_evaluator(),
            relations=InMemoryRelationTupleRepository(),
            decision_cache=_cache,
        )
    if not _registered:
        InProcessEventBus.subscribe("platform.tenant.provisioned", _service.handle_tenant_provisioned)
        _registered = True
    return _service


def get_authorization_evaluator() -> AuthorizationApplicationService:
    """PEP alias — Documents and peers depend on IAuthorizationEvaluator."""
    return get_authorization_service()


def reset_authorization_service() -> None:
    global _service, _registered, _cache
    _service = None
    _registered = False
    _cache = None
    InMemoryAuthorizationProfileRepository.reset()
    InMemoryAbacPolicyRepository.reset()
    InMemoryAccessDecisionRepository.reset()
    InMemoryRelationTupleRepository.reset()
    InMemoryDecisionCache.reset()
    _RefCounter.reset()
