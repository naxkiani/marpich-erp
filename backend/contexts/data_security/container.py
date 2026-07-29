"""Data Security DI container."""
from __future__ import annotations

from contexts.data_security.application.service import (
    DataSecurityApplicationService,
)

_service: DataSecurityApplicationService | None = None


def get_data_security_service() -> DataSecurityApplicationService:
    global _service
    if _service is None:
        _service = DataSecurityApplicationService()
    return _service


def reset_data_security_service() -> None:
    global _service
    _service = None
