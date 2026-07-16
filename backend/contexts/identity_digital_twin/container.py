from contexts.identity_digital_twin.application.service import IdentityDigitalTwinApplicationService
from contexts.identity_digital_twin.infrastructure.persistence.twin_memory_store import InMemoryTwinRepository, InMemorySnapshotRepository, InMemorySimulationRepository, InMemoryDriftAlertRepository, InMemoryTwinStore
from contexts.policy.container import get_policy_evaluator
from shared.infrastructure.messaging.event_bus import InProcessEventBus
_service = None
_registered = False
def get_identity_digital_twin_service() -> IdentityDigitalTwinApplicationService:
    global _service, _registered
    if _service is None: _service=IdentityDigitalTwinApplicationService(InMemoryTwinRepository(),InMemorySnapshotRepository(),InMemorySimulationRepository(),InMemoryDriftAlertRepository(),get_policy_evaluator())
    if not _registered:
        for topic in ("identity.user.created", "identity.role.assigned", "identity.login.succeeded", "federation.identity.linked", "lifecycle.state.changed", "identity_risk.score.updated"):
            InProcessEventBus.subscribe(topic, lambda event, topic=topic: _service.handle_source_event(event, source_event=topic))
        _registered = True
    return _service
def reset_identity_digital_twin_service() -> None:
    global _service, _registered
    _service=None; _registered=False; InMemoryTwinStore.reset()
