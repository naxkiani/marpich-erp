"""Payroll DI container + HR event subscription."""
from __future__ import annotations

from contexts.payroll.application.service import PayrollApplicationService
from contexts.payroll.infrastructure.acl.hr_events import handle_employee_hired
from contexts.payroll.infrastructure.persistence.memory_store import (
    InMemoryPayrollEmployeeRepository,
    InMemoryPayrollRunRepository,
)
from contexts.payroll.infrastructure.persistence.postgres_store import (
    PostgresPayrollEmployeeRepository,
    PostgresPayrollRunRepository,
)
from shared.infrastructure.messaging.event_bus import InProcessEventBus
from shared.infrastructure.settings import use_postgres

_service: PayrollApplicationService | None = None
_registered = False


def get_payroll_service() -> PayrollApplicationService:
    global _service, _registered
    if _service is None:
        if use_postgres():
            _service = PayrollApplicationService(
                employees=PostgresPayrollEmployeeRepository(),
                runs=PostgresPayrollRunRepository(),
            )
        else:
            _service = PayrollApplicationService(
                employees=InMemoryPayrollEmployeeRepository(),
                runs=InMemoryPayrollRunRepository(),
            )
    if not _registered:
        InProcessEventBus.subscribe("human_resources.employee.hired", handle_employee_hired)
        _registered = True
    return _service


def reset_payroll_service() -> None:
    global _service, _registered
    _service = None
    _registered = False
