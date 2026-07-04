"""Settings DI + event subscriptions."""
from __future__ import annotations

from contexts.settings.application.service import SettingsApplicationService
from contexts.settings.infrastructure.acl.platform_events import PlatformSettingsAdapter
from contexts.settings.infrastructure.persistence.memory_store import InMemoryTenantSettingsRepository
from contexts.settings.infrastructure.persistence.postgres_store import PostgresTenantSettingsRepository
from shared.infrastructure.messaging.event_bus import InProcessEventBus
from shared.infrastructure.settings import use_postgres

_service: SettingsApplicationService | None = None
_registered = False


def get_settings_service() -> SettingsApplicationService:
    global _service, _registered
    if _service is None:
        repo = PostgresTenantSettingsRepository() if use_postgres() else InMemoryTenantSettingsRepository()
        _service = SettingsApplicationService(
            settings=repo,
            platform_events=PlatformSettingsAdapter(),
        )
    if not _registered:
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


def reset_settings_service() -> None:
    global _service, _registered
    _service = None
    _registered = False
