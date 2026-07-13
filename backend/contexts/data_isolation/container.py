"""Data isolation DI container."""
from __future__ import annotations

from contexts.data_isolation.application.service import DataIsolationApplicationService
from contexts.data_isolation.infrastructure.adapters.identity_principal_source import IdentityPrincipalSourceAdapter
from contexts.data_isolation.infrastructure.persistence.data_isolation_memory_store import (
    InMemoryDataIsolationStore,
    InMemoryIsolationProfileRepository,
    InMemoryPrincipalRepository,
)
from contexts.data_isolation.infrastructure.persistence.postgres_principal_store import PostgresPrincipalRepository
from contexts.policy.container import get_policy_evaluator
from shared.infrastructure.messaging.event_bus import InProcessEventBus
from shared.infrastructure.settings import use_postgres

_service: DataIsolationApplicationService | None = None
_registered = False


def get_data_isolation_service() -> DataIsolationApplicationService:
    global _service, _registered
    if _service is None:
        principals = PostgresPrincipalRepository() if use_postgres() else InMemoryPrincipalRepository()
        _service = DataIsolationApplicationService(
            profiles=InMemoryIsolationProfileRepository(),
            principals=principals,
            identity_source=IdentityPrincipalSourceAdapter(),
            policy_evaluator=get_policy_evaluator(),
        )
    if not _registered:
        InProcessEventBus.subscribe("platform.tenant.provisioned", _service.handle_tenant_provisioned)
        _registered = True
    return _service


def reset_data_isolation_service() -> None:
    global _service, _registered
    _service = None
    _registered = False
    InMemoryDataIsolationStore.reset()
