"""Data Governance DI container."""
from __future__ import annotations

from contexts.data_governance.application.service import (
    DataGovernanceApplicationService,
)

_service: DataGovernanceApplicationService | None = None


def get_data_governance_service() -> DataGovernanceApplicationService:
    global _service
    if _service is None:
        _service = DataGovernanceApplicationService()
    return _service


def reset_data_governance_service() -> None:
    global _service
    _service = None
