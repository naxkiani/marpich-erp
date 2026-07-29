"""Cyber Security DI container."""
from __future__ import annotations

from contexts.cyber_security.application.service import (
    CyberSecurityApplicationService,
)

_service: CyberSecurityApplicationService | None = None


def get_cyber_security_service() -> CyberSecurityApplicationService:
    global _service
    if _service is None:
        _service = CyberSecurityApplicationService()
    return _service


def reset_cyber_security_service() -> None:
    global _service
    _service = None
