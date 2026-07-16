"""Inventory ACL — pharmacy dispense completed → stock decrement (drug_code as SKU)."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from contexts.inventory.application.service import InventoryApplicationService

logger = logging.getLogger(__name__)


def make_pharmacy_dispense_handler(
    get_service: Callable[[], "InventoryApplicationService"],
):
    async def handle_pharmacy_dispense_completed(envelope: dict) -> None:
        if str(envelope.get("event_name") or "") != "pharmacy.dispense.completed":
            return
        tenant_id = str(envelope.get("tenant_id") or "")
        payload = envelope.get("payload") if isinstance(envelope.get("payload"), dict) else {}
        dispense_id = str(payload.get("dispense_id") or "")
        drug_code = str(payload.get("drug_code") or "")
        quantity = payload.get("quantity_dispensed")
        if not tenant_id or not dispense_id:
            logger.warning("inventory pharmacy acl skipped — missing tenant/dispense_id")
            return

        result = await get_service().apply_pharmacy_dispense_decrement(
            tenant_id=tenant_id,
            dispense_id=dispense_id,
            drug_code=drug_code,
            quantity_dispensed=float(quantity or 0),
            correlation_id=str(envelope.get("correlation_id") or envelope.get("event_id") or ""),
        )
        if not result.succeeded:
            logger.error("inventory pharmacy acl failed: %s", result.error)
            raise RuntimeError(result.error)

    return handle_pharmacy_dispense_completed
