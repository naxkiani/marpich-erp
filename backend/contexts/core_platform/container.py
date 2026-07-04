"""Core Platform DI container."""
from __future__ import annotations

from contexts.core_platform.application.service import CorePlatformApplicationService
from contexts.core_platform.infrastructure.persistence.memory_store import InMemoryTenantRepository
from contexts.core_platform.infrastructure.persistence.postgres_store import PostgresTenantRepository
from shared.infrastructure.settings import use_postgres

_service: CorePlatformApplicationService | None = None


def get_platform_service() -> CorePlatformApplicationService:
    global _service
    if _service is None:
        tenants = PostgresTenantRepository() if use_postgres() else InMemoryTenantRepository()
        _service = CorePlatformApplicationService(tenants=tenants)
    return _service


def reset_platform_service() -> None:
    global _service
    _service = None
