"""Documents DI + event subscriptions."""
from __future__ import annotations

from contexts.documents.application.service import DocumentsApplicationService
from contexts.documents.infrastructure.acl.platform_events import DocumentsPlatformAdapter
from contexts.documents.infrastructure.persistence.memory_store import (
    InMemoryDocumentRepository,
    InMemoryFolderRepository,
    InMemorySignatureRepository,
    InMemoryVersionRepository,
)
from contexts.documents.infrastructure.persistence.postgres_store import (
    PostgresDocumentRepository,
    PostgresFolderRepository,
    PostgresSignatureRepository,
    PostgresVersionRepository,
)
from shared.infrastructure.messaging.event_bus import InProcessEventBus
from shared.infrastructure.settings import use_postgres

_service: DocumentsApplicationService | None = None
_registered = False


def get_documents_service() -> DocumentsApplicationService:
    global _service, _registered
    if _service is None:
        from contexts.authorization.container import get_authorization_evaluator

        authz = get_authorization_evaluator()
        if use_postgres():
            _service = DocumentsApplicationService(
                folders=PostgresFolderRepository(),
                documents=PostgresDocumentRepository(),
                versions=PostgresVersionRepository(),
                signatures=PostgresSignatureRepository(),
                platform_events=DocumentsPlatformAdapter(),
                authz=authz,
            )
        else:
            _service = DocumentsApplicationService(
                folders=InMemoryFolderRepository(),
                documents=InMemoryDocumentRepository(),
                versions=InMemoryVersionRepository(),
                signatures=InMemorySignatureRepository(),
                platform_events=DocumentsPlatformAdapter(),
                authz=authz,
            )
    if not _registered:
        InProcessEventBus.subscribe(
            "platform.tenant.provisioned",
            _service.handle_tenant_provisioned,
        )
        _registered = True
    return _service


def reset_documents_service() -> None:
    global _service, _registered
    _service = None
    _registered = False
