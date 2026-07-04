"""Treasury DI."""
from __future__ import annotations

from contexts.treasury.application.service import TreasuryApplicationService
from contexts.treasury.infrastructure.persistence.memory_store import (
    InMemoryBankReconciliationRepository,
    InMemoryCashForecastRepository,
    InMemoryTreasuryAccountRepository,
    InMemoryTreasuryTransferRepository,
)
from shared.infrastructure.messaging.event_bus import InProcessEventBus

_service: TreasuryApplicationService | None = None
_registered = False


def get_treasury_service() -> TreasuryApplicationService:
    global _service, _registered
    if _service is None:
        _service = TreasuryApplicationService(
            accounts=InMemoryTreasuryAccountRepository(),
            transfers=InMemoryTreasuryTransferRepository(),
            reconciliations=InMemoryBankReconciliationRepository(),
            forecasts=InMemoryCashForecastRepository(),
        )
    if not _registered:
        InProcessEventBus.subscribe(
            "platform.tenant.provisioned",
            _service.handle_tenant_provisioned,
        )
        _registered = True
    return _service


def reset_treasury_service() -> None:
    global _service, _registered
    _service = None
    _registered = False
    InMemoryTreasuryAccountRepository.reset()
    InMemoryTreasuryTransferRepository.reset()
    InMemoryBankReconciliationRepository.reset()
    InMemoryCashForecastRepository.reset()
