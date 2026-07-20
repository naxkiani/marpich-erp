"""Secrets Cryptographic Trust DI + event subscriptions."""
from __future__ import annotations

from contexts.secrets.application.service import SecretsApplicationService
from shared.infrastructure.messaging.event_bus import InProcessEventBus

_service: SecretsApplicationService | None = None
_registered = False


def get_secrets_service() -> SecretsApplicationService:
    global _service, _registered
    if _service is None:
        _service = SecretsApplicationService()
    if not _registered:
        InProcessEventBus.subscribe(
            "platform.tenant.provisioned",
            _service.handle_tenant_provisioned,
        )
        _registered = True
    return _service


def reset_secrets_service() -> None:
    global _service, _registered
    _service = None
    _registered = False
