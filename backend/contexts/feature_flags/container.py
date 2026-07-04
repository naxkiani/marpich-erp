"""Feature flags DI."""
from __future__ import annotations

from contexts.feature_flags.application.service import FeatureFlagApplicationService
from contexts.feature_flags.infrastructure.adapters.evaluator_client import FeatureFlagEvaluatorClient
from contexts.feature_flags.infrastructure.persistence.memory_store import InMemoryFeatureFlagRepository
from shared.application.ports.feature_flags import IFeatureFlagEvaluator
from shared.infrastructure.messaging.event_bus import InProcessEventBus

_service: FeatureFlagApplicationService | None = None
_evaluator: FeatureFlagEvaluatorClient | None = None
_registered = False


def get_feature_flag_service() -> FeatureFlagApplicationService:
    global _service, _evaluator, _registered
    if _service is None:
        _service = FeatureFlagApplicationService(flags=InMemoryFeatureFlagRepository())
        _evaluator = FeatureFlagEvaluatorClient(_service)
    if not _registered:
        InProcessEventBus.subscribe(
            "platform.tenant.provisioned",
            _service.handle_tenant_provisioned,
        )
        _registered = True
    return _service


def get_feature_flag_evaluator() -> IFeatureFlagEvaluator:
    get_feature_flag_service()
    assert _evaluator is not None
    return _evaluator


def reset_feature_flag_service() -> None:
    global _service, _evaluator, _registered
    _service = None
    _evaluator = None
    _registered = False
