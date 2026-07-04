"""Localization DI + event subscriptions."""
from __future__ import annotations

from contexts.localization.application.service import LocalizationApplicationService
from contexts.localization.infrastructure.acl.platform_events import PlatformLocalizationAdapter
from contexts.localization.infrastructure.persistence.memory_store import (
    InMemoryLocaleRepository,
    InMemoryTranslationBundleRepository,
    InMemoryTranslationKeyRepository,
)
from contexts.localization.infrastructure.persistence.postgres_store import (
    PostgresLocaleRepository,
    PostgresTranslationBundleRepository,
    PostgresTranslationKeyRepository,
)
from shared.infrastructure.messaging.event_bus import InProcessEventBus
from shared.infrastructure.settings import use_postgres

_service: LocalizationApplicationService | None = None
_registered = False


def get_localization_service() -> LocalizationApplicationService:
    global _service, _registered
    if _service is None:
        if use_postgres():
            _service = LocalizationApplicationService(
                locales=PostgresLocaleRepository(),
                keys=PostgresTranslationKeyRepository(),
                bundles=PostgresTranslationBundleRepository(),
                platform_events=PlatformLocalizationAdapter(),
            )
        else:
            _service = LocalizationApplicationService(
                locales=InMemoryLocaleRepository(),
                keys=InMemoryTranslationKeyRepository(),
                bundles=InMemoryTranslationBundleRepository(),
                platform_events=PlatformLocalizationAdapter(),
            )
    if not _registered:
        InProcessEventBus.subscribe(
            "platform.tenant.provisioned",
            _service.handle_tenant_provisioned,
        )
        _registered = True
    return _service


def reset_localization_service() -> None:
    global _service, _registered
    _service = None
    _registered = False
