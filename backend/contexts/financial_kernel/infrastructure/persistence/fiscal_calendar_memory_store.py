"""In-memory fiscal calendar repositories."""
from __future__ import annotations

from contexts.financial_kernel.domain.aggregates.fiscal_calendar import (
    FiscalCalendar,
    FiscalCalendarAuditLog,
    FiscalCloseRequest,
)
from contexts.financial_kernel.domain.ports.fiscal_calendar_repositories import (
    IFiscalCalendarAuditRepository,
    IFiscalCalendarRepository,
    IFiscalCloseRequestRepository,
)


class InMemoryFiscalCalendarRepository(IFiscalCalendarRepository):
    _calendars: dict[str, FiscalCalendar] = {}

    @classmethod
    def reset(cls) -> None:
        cls._calendars = {}

    async def save(self, calendar: FiscalCalendar) -> None:
        self._calendars[str(calendar.id)] = calendar

    async def find_by_id(self, calendar_id: str) -> FiscalCalendar | None:
        return self._calendars.get(calendar_id)

    async def list_by_tenant(self, tenant_id: str) -> list[FiscalCalendar]:
        return [c for c in self._calendars.values() if c.tenant_id == tenant_id]

    async def find_default(self, tenant_id: str, organization_id: str | None = None) -> FiscalCalendar | None:
        for cal in self._calendars.values():
            if cal.tenant_id != tenant_id or not cal.is_default:
                continue
            if organization_id is None or cal.organization_id == organization_id:
                return cal
        return None


class InMemoryFiscalCalendarAuditRepository(IFiscalCalendarAuditRepository):
    _entries: list[FiscalCalendarAuditLog] = []

    @classmethod
    def reset(cls) -> None:
        cls._entries = []

    async def save(self, entry: FiscalCalendarAuditLog) -> None:
        self._entries.append(entry)

    async def list_by_tenant(self, tenant_id: str, *, limit: int = 100) -> list[FiscalCalendarAuditLog]:
        items = [e for e in self._entries if e.tenant_id == tenant_id]
        return items[-limit:]


class InMemoryFiscalCloseRequestRepository(IFiscalCloseRequestRepository):
    _requests: dict[str, FiscalCloseRequest] = {}

    @classmethod
    def reset(cls) -> None:
        cls._requests = {}

    async def save(self, request: FiscalCloseRequest) -> None:
        self._requests[str(request.id)] = request

    async def find_by_id(self, request_id: str) -> FiscalCloseRequest | None:
        return self._requests.get(request_id)

    async def list_by_tenant(self, tenant_id: str) -> list[FiscalCloseRequest]:
        return [r for r in self._requests.values() if r.tenant_id == tenant_id]
