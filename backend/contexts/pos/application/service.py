"""POS application service."""
from __future__ import annotations

import json
from datetime import UTC, datetime
from decimal import Decimal

from contexts.pos.domain.aggregates.pos_sale import PosSale
from contexts.pos.domain.aggregates.receipt import Receipt
from contexts.pos.domain.aggregates.shift import Shift
from contexts.pos.domain.aggregates.terminal import Terminal
from contexts.pos.domain.ports.repositories import (
    IPosSaleRepository,
    IReceiptRepository,
    IShiftRepository,
    ITerminalRepository,
)
from shared.application.result import Result
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class ConsolePosAudit:
    async def log(self, **kwargs: object) -> None:
        entry = {"type": "audit", "context": "pos", **kwargs, "occurred_at": datetime.now(UTC).isoformat()}
        print(json.dumps(entry, default=str))


class PosApplicationService:
    def __init__(
        self,
        terminals: ITerminalRepository,
        shifts: IShiftRepository,
        sales: IPosSaleRepository,
        receipts: IReceiptRepository,
        audit: ConsolePosAudit | None = None,
    ) -> None:
        self._terminals = terminals
        self._shifts = shifts
        self._sales = sales
        self._receipts = receipts
        self._audit = audit or ConsolePosAudit()

    async def register_terminal(
        self, *, tenant_id: str, terminal_code: str, store_name: str, correlation_id: str
    ) -> Result[dict]:
        if await self._terminals.find_by_code(tenant_id, terminal_code):
            return Result.fail("pos.errors.terminal_exists")
        terminal = Terminal.register(
            tenant_id=tenant_id, terminal_code=terminal_code, store_name=store_name
        )
        await self._terminals.save(terminal)
        await self._audit.log(
            tenant_id=tenant_id,
            correlation_id=correlation_id,
            action="pos.terminal.registered",
            resource_type="terminal",
            resource_id=str(terminal.id),
        )
        return Result.ok(terminal.to_dict())

    async def open_shift(
        self, *, tenant_id: str, terminal_id: str, cashier_name: str, correlation_id: str
    ) -> Result[dict]:
        terminal = await self._terminals.find_by_id(tenant_id, UniqueId.from_string(terminal_id))
        if not terminal:
            return Result.fail("pos.errors.terminal_not_found")
        if await self._shifts.find_open_by_terminal(tenant_id, terminal.id):
            return Result.fail("pos.errors.shift_already_open")
        shift = Shift.open(tenant_id=tenant_id, terminal_id=terminal.id, cashier_name=cashier_name)
        await self._shifts.save(shift)
        return Result.ok(shift.to_dict())

    async def complete_sale(
        self,
        *,
        tenant_id: str,
        shift_id: str,
        items: list[dict],
        subtotal: Decimal,
        tax: Decimal,
        payment_method: str,
        correlation_id: str,
        issue_receipt: bool = True,
    ) -> Result[dict]:
        shift = await self._shifts.find_by_id(tenant_id, UniqueId.from_string(shift_id))
        if not shift:
            return Result.fail("pos.errors.shift_not_found")
        try:
            shift.add_sale(subtotal + tax)
        except ValueError as exc:
            return Result.fail(str(exc))

        sale, sale_event = PosSale.checkout(
            tenant_id=tenant_id,
            shift_id=shift.id,
            terminal_id=shift.terminal_id,
            items=items,
            subtotal=subtotal,
            tax=tax,
            payment_method=payment_method,
            correlation_id=correlation_id,
        )
        await self._sales.save(sale)
        await self._shifts.save(shift)
        await publish_integration_event(sale_event)

        result: dict = {"sale": sale.to_dict()}
        if issue_receipt:
            receipt_number = f"RCP-{str(sale.id)[:8].upper()}"
            receipt, receipt_event = Receipt.issue(
                tenant_id=tenant_id,
                sale_id=sale.id,
                receipt_number=receipt_number,
                payload=sale.to_dict(),
                correlation_id=correlation_id,
            )
            await self._receipts.save(receipt)
            await publish_integration_event(receipt_event)
            result["receipt"] = receipt.to_dict()

        await self._audit.log(
            tenant_id=tenant_id,
            correlation_id=correlation_id,
            action="pos.sale.completed",
            resource_type="sale",
            resource_id=str(sale.id),
        )
        return Result.ok(result)

    async def close_shift(self, *, tenant_id: str, shift_id: str, correlation_id: str) -> Result[dict]:
        shift = await self._shifts.find_by_id(tenant_id, UniqueId.from_string(shift_id))
        if not shift:
            return Result.fail("pos.errors.shift_not_found")
        try:
            event = shift.close(correlation_id=correlation_id)
        except ValueError as exc:
            return Result.fail(str(exc))
        await self._shifts.save(shift)
        await publish_integration_event(event)
        return Result.ok(shift.to_dict())
