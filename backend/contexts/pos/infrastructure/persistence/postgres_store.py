"""PostgreSQL repositories — POS bounded context."""
from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from sqlalchemy import select

from contexts.pos.domain.aggregates.pos_sale import PosSale
from contexts.pos.domain.aggregates.receipt import Receipt
from contexts.pos.domain.aggregates.shift import Shift, ShiftStatus
from contexts.pos.domain.aggregates.terminal import Terminal, TerminalStatus
from contexts.pos.domain.ports.repositories import (
    IPosSaleRepository,
    IReceiptRepository,
    IShiftRepository,
    ITerminalRepository,
)
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.database.engine import session_scope
from shared.infrastructure.database.orm import PosReceiptRow, PosSaleRow, PosShiftRow, PosTerminalRow


class PostgresTerminalRepository(ITerminalRepository):
    async def save(self, terminal: Terminal) -> None:
        async with session_scope() as session:
            if await session.get(PosTerminalRow, UUID(str(terminal.id))) is None:
                session.add(
                    PosTerminalRow(
                        id=UUID(str(terminal.id)),
                        tenant_id=terminal.tenant_id,
                        terminal_code=terminal.terminal_code,
                        store_name=terminal.store_name,
                        status=terminal.status.value,
                    )
                )

    async def find_by_id(self, tenant_id: str, terminal_id: UniqueId) -> Terminal | None:
        async with session_scope() as session:
            row = await session.get(PosTerminalRow, UUID(str(terminal_id)))
            return _terminal_from_row(row) if row and row.tenant_id == tenant_id else None

    async def find_by_code(self, tenant_id: str, terminal_code: str) -> Terminal | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(PosTerminalRow).where(
                    PosTerminalRow.tenant_id == tenant_id,
                    PosTerminalRow.terminal_code == terminal_code.upper(),
                )
            )
            return _terminal_from_row(row) if row else None


class PostgresShiftRepository(IShiftRepository):
    async def save(self, shift: Shift) -> None:
        async with session_scope() as session:
            row = await session.get(PosShiftRow, UUID(str(shift.id)))
            if row is None:
                session.add(
                    PosShiftRow(
                        id=UUID(str(shift.id)),
                        tenant_id=shift.tenant_id,
                        terminal_id=UUID(str(shift.terminal_id)),
                        cashier_name=shift.cashier_name,
                        status=shift.status.value,
                        total_sales=str(shift.total_sales),
                        opened_at=shift.opened_at,
                        closed_at=shift.closed_at,
                    )
                )
            else:
                row.status = shift.status.value
                row.total_sales = str(shift.total_sales)
                row.closed_at = shift.closed_at

    async def find_by_id(self, tenant_id: str, shift_id: UniqueId) -> Shift | None:
        async with session_scope() as session:
            row = await session.get(PosShiftRow, UUID(str(shift_id)))
            return _shift_from_row(row) if row and row.tenant_id == tenant_id else None

    async def find_open_by_terminal(self, tenant_id: str, terminal_id: UniqueId) -> Shift | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(PosShiftRow).where(
                    PosShiftRow.tenant_id == tenant_id,
                    PosShiftRow.terminal_id == UUID(str(terminal_id)),
                    PosShiftRow.status == ShiftStatus.OPEN.value,
                )
            )
            return _shift_from_row(row) if row else None


class PostgresPosSaleRepository(IPosSaleRepository):
    async def save(self, sale: PosSale) -> None:
        async with session_scope() as session:
            if await session.get(PosSaleRow, UUID(str(sale.id))) is None:
                session.add(
                    PosSaleRow(
                        id=UUID(str(sale.id)),
                        tenant_id=sale.tenant_id,
                        shift_id=UUID(str(sale.shift_id)),
                        terminal_id=UUID(str(sale.terminal_id)),
                        items=sale.items,
                        subtotal=str(sale.subtotal),
                        tax=str(sale.tax),
                        total=str(sale.total),
                        payment_method=sale.payment_method,
                    )
                )

    async def find_by_id(self, tenant_id: str, sale_id: UniqueId) -> PosSale | None:
        async with session_scope() as session:
            row = await session.get(PosSaleRow, UUID(str(sale_id)))
            return _sale_from_row(row) if row and row.tenant_id == tenant_id else None


class PostgresReceiptRepository(IReceiptRepository):
    async def save(self, receipt: Receipt) -> None:
        async with session_scope() as session:
            if await session.get(PosReceiptRow, UUID(str(receipt.id))) is None:
                session.add(
                    PosReceiptRow(
                        id=UUID(str(receipt.id)),
                        tenant_id=receipt.tenant_id,
                        sale_id=UUID(str(receipt.sale_id)),
                        receipt_number=receipt.receipt_number,
                        payload=receipt.payload,
                        issued_at=receipt.issued_at,
                    )
                )

    async def find_by_sale(self, tenant_id: str, sale_id: UniqueId) -> Receipt | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(PosReceiptRow).where(
                    PosReceiptRow.tenant_id == tenant_id,
                    PosReceiptRow.sale_id == UUID(str(sale_id)),
                )
            )
            return _receipt_from_row(row) if row else None


def _terminal_from_row(row: PosTerminalRow) -> Terminal:
    return Terminal(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        terminal_code=row.terminal_code,
        store_name=row.store_name,
        status=TerminalStatus(row.status),
        created_at=row.created_at,
    )


def _shift_from_row(row: PosShiftRow) -> Shift:
    return Shift(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        terminal_id=UniqueId.from_string(str(row.terminal_id)),
        cashier_name=row.cashier_name,
        status=ShiftStatus(row.status),
        total_sales=Decimal(row.total_sales),
        opened_at=row.opened_at,
        closed_at=row.closed_at,
    )


def _sale_from_row(row: PosSaleRow) -> PosSale:
    return PosSale(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        shift_id=UniqueId.from_string(str(row.shift_id)),
        terminal_id=UniqueId.from_string(str(row.terminal_id)),
        items=list(row.items or []),
        subtotal=Decimal(row.subtotal),
        tax=Decimal(row.tax),
        total=Decimal(row.total),
        payment_method=row.payment_method,
        created_at=row.created_at,
    )


def _receipt_from_row(row: PosReceiptRow) -> Receipt:
    return Receipt(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        sale_id=UniqueId.from_string(str(row.sale_id)),
        receipt_number=row.receipt_number,
        payload=dict(row.payload or {}),
        issued_at=row.issued_at,
    )
