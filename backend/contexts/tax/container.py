"""Tax DI container + payroll event subscription."""
from __future__ import annotations

from contexts.tax.application.service import TaxApplicationService
from contexts.tax.infrastructure.acl.payroll_events import handle_payroll_run_completed
from contexts.tax.infrastructure.persistence.memory_store import (
    InMemoryTaxLiabilityRepository,
    InMemoryTaxReturnRepository,
)
from contexts.tax.infrastructure.persistence.postgres_store import (
    PostgresTaxLiabilityRepository,
    PostgresTaxReturnRepository,
)
from shared.infrastructure.messaging.event_bus import InProcessEventBus
from shared.infrastructure.settings import use_postgres

_service: TaxApplicationService | None = None
_registered = False


def get_tax_service() -> TaxApplicationService:
    global _service, _registered
    if _service is None:
        if use_postgres():
            _service = TaxApplicationService(
                liabilities=PostgresTaxLiabilityRepository(),
                returns=PostgresTaxReturnRepository(),
            )
        else:
            _service = TaxApplicationService(
                liabilities=InMemoryTaxLiabilityRepository(),
                returns=InMemoryTaxReturnRepository(),
            )
    if not _registered:
        InProcessEventBus.subscribe("payroll.run.completed", handle_payroll_run_completed)
        _registered = True
    return _service


def reset_tax_service() -> None:
    global _service, _registered
    _service = None
    _registered = False
