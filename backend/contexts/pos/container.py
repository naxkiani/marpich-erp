"""POS DI container."""
from __future__ import annotations

from contexts.pos.application.service import PosApplicationService
from contexts.pos.infrastructure.persistence.memory_store import (
    InMemoryPosSaleRepository,
    InMemoryReceiptRepository,
    InMemoryShiftRepository,
    InMemoryTerminalRepository,
)
from contexts.pos.infrastructure.persistence.postgres_store import (
    PostgresPosSaleRepository,
    PostgresReceiptRepository,
    PostgresShiftRepository,
    PostgresTerminalRepository,
)
from shared.infrastructure.settings import use_postgres

_service: PosApplicationService | None = None


def get_pos_service() -> PosApplicationService:
    global _service
    if _service is None:
        if use_postgres():
            _service = PosApplicationService(
                terminals=PostgresTerminalRepository(),
                shifts=PostgresShiftRepository(),
                sales=PostgresPosSaleRepository(),
                receipts=PostgresReceiptRepository(),
            )
        else:
            _service = PosApplicationService(
                terminals=InMemoryTerminalRepository(),
                shifts=InMemoryShiftRepository(),
                sales=InMemoryPosSaleRepository(),
                receipts=InMemoryReceiptRepository(),
            )
    return _service


def reset_pos_service() -> None:
    global _service
    _service = None
