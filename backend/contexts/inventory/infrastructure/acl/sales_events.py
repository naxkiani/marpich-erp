"""Inventory ACL — sales order placed → stock reservation (no peer domain imports)."""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


async def handle_sales_order_placed(envelope: dict) -> None:
    if str(envelope.get("event_name") or "") != "sales.order.placed":
        return
    tenant_id = str(envelope.get("tenant_id") or "")
    payload = envelope.get("payload") if isinstance(envelope.get("payload"), dict) else {}
    order_id = str(payload.get("order_id") or "")
    lines = list(payload.get("lines") or [])
    if not tenant_id or not order_id:
        logger.warning("inventory sales acl skipped — missing tenant/order_id")
        return
    if not lines:
        logger.info("inventory sales acl — order %s has no lines; skip", order_id)
        return

    from contexts.inventory.container import get_inventory_service

    result = await get_inventory_service().apply_sales_order_reservation(
        tenant_id=tenant_id,
        order_id=order_id,
        lines=lines,
        correlation_id=str(envelope.get("correlation_id") or envelope.get("event_id") or ""),
    )
    if not result.succeeded:
        logger.error("inventory sales acl failed: %s", result.error)
        raise RuntimeError(result.error)
