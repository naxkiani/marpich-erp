"""Media DI + event subscriptions."""
from __future__ import annotations

from contexts.media.application.service import MediaApplicationService
from contexts.media.infrastructure.acl.document_events import DocumentEventAdapter
from contexts.media.infrastructure.persistence.memory_store import (
    InMemoryAssetRepository,
    InMemoryTranscodeJobRepository,
    InMemoryVariantRepository,
)
from contexts.media.infrastructure.persistence.postgres_store import (
    PostgresAssetRepository,
    PostgresTranscodeJobRepository,
    PostgresVariantRepository,
)
from shared.infrastructure.messaging.event_bus import InProcessEventBus
from shared.infrastructure.settings import use_postgres

_service: MediaApplicationService | None = None
_registered = False


def get_media_service() -> MediaApplicationService:
    global _service, _registered
    if _service is None:
        if use_postgres():
            _service = MediaApplicationService(
                assets=PostgresAssetRepository(),
                variants=PostgresVariantRepository(),
                jobs=PostgresTranscodeJobRepository(),
                document_events=DocumentEventAdapter(),
            )
        else:
            _service = MediaApplicationService(
                assets=InMemoryAssetRepository(),
                variants=InMemoryVariantRepository(),
                jobs=InMemoryTranscodeJobRepository(),
                document_events=DocumentEventAdapter(),
            )
    if not _registered:
        InProcessEventBus.subscribe(
            "documents.document.uploaded",
            _service.handle_document_uploaded,
        )
        _registered = True
    return _service


def reset_media_service() -> None:
    global _service, _registered
    _service = None
    _registered = False
