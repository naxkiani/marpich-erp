"""Identity Intelligence DI container."""
from __future__ import annotations

from contexts.identity_intelligence.application.service import (
    IdentityIntelligenceApplicationService,
)

_service: IdentityIntelligenceApplicationService | None = None


def get_identity_intelligence_service() -> IdentityIntelligenceApplicationService:
    global _service
    if _service is None:
        _service = IdentityIntelligenceApplicationService()
    return _service


def reset_identity_intelligence_service() -> None:
    global _service
    _service = None
