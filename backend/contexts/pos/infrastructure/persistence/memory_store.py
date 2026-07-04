"""POS in-memory repositories."""
from __future__ import annotations

from contexts.pos.domain.aggregates.pos_sale import PosSale
from contexts.pos.domain.aggregates.receipt import Receipt
from contexts.pos.domain.aggregates.shift import Shift, ShiftStatus
from contexts.pos.domain.aggregates.terminal import Terminal
from contexts.pos.domain.ports.repositories import (
    IPosSaleRepository,
    IReceiptRepository,
    IShiftRepository,
    ITerminalRepository,
)
from shared.domain.value_objects.unique_id import UniqueId


class PosMemoryStore:
    terminals: dict[str, Terminal] = {}
    shifts: dict[str, Shift] = {}
    sales: dict[str, PosSale] = {}
    receipts: dict[str, Receipt] = {}

    @classmethod
    def reset(cls) -> None:
        cls.terminals.clear()
        cls.shifts.clear()
        cls.sales.clear()
        cls.receipts.clear()


class InMemoryTerminalRepository(ITerminalRepository):
    async def save(self, terminal: Terminal) -> None:
        PosMemoryStore.terminals[str(terminal.id)] = terminal

    async def find_by_id(self, tenant_id: str, terminal_id: UniqueId) -> Terminal | None:
        t = PosMemoryStore.terminals.get(str(terminal_id))
        return t if t and t.tenant_id == tenant_id else None

    async def find_by_code(self, tenant_id: str, terminal_code: str) -> Terminal | None:
        for t in PosMemoryStore.terminals.values():
            if t.tenant_id == tenant_id and t.terminal_code == terminal_code.upper():
                return t
        return None


class InMemoryShiftRepository(IShiftRepository):
    async def save(self, shift: Shift) -> None:
        PosMemoryStore.shifts[str(shift.id)] = shift

    async def find_by_id(self, tenant_id: str, shift_id: UniqueId) -> Shift | None:
        s = PosMemoryStore.shifts.get(str(shift_id))
        return s if s and s.tenant_id == tenant_id else None

    async def find_open_by_terminal(self, tenant_id: str, terminal_id: UniqueId) -> Shift | None:
        for s in PosMemoryStore.shifts.values():
            if (
                s.tenant_id == tenant_id
                and str(s.terminal_id) == str(terminal_id)
                and s.status == ShiftStatus.OPEN
            ):
                return s
        return None


class InMemoryPosSaleRepository(IPosSaleRepository):
    async def save(self, sale: PosSale) -> None:
        PosMemoryStore.sales[str(sale.id)] = sale

    async def find_by_id(self, tenant_id: str, sale_id: UniqueId) -> PosSale | None:
        s = PosMemoryStore.sales.get(str(sale_id))
        return s if s and s.tenant_id == tenant_id else None


class InMemoryReceiptRepository(IReceiptRepository):
    async def save(self, receipt: Receipt) -> None:
        PosMemoryStore.receipts[str(receipt.id)] = receipt

    async def find_by_sale(self, tenant_id: str, sale_id: UniqueId) -> Receipt | None:
        for r in PosMemoryStore.receipts.values():
            if r.tenant_id == tenant_id and str(r.sale_id) == str(sale_id):
                return r
        return None
