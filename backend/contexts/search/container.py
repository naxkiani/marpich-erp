"""Search DI + event subscriptions."""
from __future__ import annotations

from contexts.search.application.service import SearchApplicationService
from contexts.search.infrastructure.persistence.memory_store import (
    InMemoryIndexDocumentRepository,
    InMemorySearchIndexRepository,
    InMemorySearchQueryRepository,
)
from contexts.search.infrastructure.persistence.postgres_store import (
    PostgresIndexDocumentRepository,
    PostgresSearchIndexRepository,
    PostgresSearchQueryRepository,
)
from shared.infrastructure.messaging.event_bus import InProcessEventBus
from shared.infrastructure.settings import use_postgres

_service: SearchApplicationService | None = None
_registered = False


def get_search_service() -> SearchApplicationService:
    global _service, _registered
    if _service is None:
        if use_postgres():
            _service = SearchApplicationService(
                indices=PostgresSearchIndexRepository(),
                documents=PostgresIndexDocumentRepository(),
                queries=PostgresSearchQueryRepository(),
            )
        else:
            _service = SearchApplicationService(
                indices=InMemorySearchIndexRepository(),
                documents=InMemoryIndexDocumentRepository(),
                queries=InMemorySearchQueryRepository(),
            )
    if not _registered:
        InProcessEventBus.subscribe("*", _service.handle_integration_event)
        InProcessEventBus.subscribe(
            "platform.tenant.provisioned",
            _service.handle_tenant_provisioned,
        )
        InProcessEventBus.subscribe(
            "platform.module.activated",
            _service.handle_module_activated,
        )
        _registered = True
    return _service


def reset_search_service() -> None:
    global _service, _registered
    _service = None
    _registered = False
